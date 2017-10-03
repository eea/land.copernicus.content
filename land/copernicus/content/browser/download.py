import os
import json
import zipfile
import time
from sha import sha
from datetime import datetime
from datetime import timedelta
from functools import partial
from collections import namedtuple
from collections import deque
from operator import attrgetter
from itertools import dropwhile
from itertools import imap as map

from zope.component import queryUtility
from zope.event import notify

from Products.Five.browser import BrowserView
import plone.api as api

from land.copernicus.content.config import ENV_DL_SRC_PATH as SRC_PATH
from land.copernicus.content.config import ENV_DL_DST_PATH as DST_PATH
from land.copernicus.content.config import ENV_DL_STATIC_PATH as ST_PATH

from land.copernicus.content.browser.views import remoteUrl_exists
from land.copernicus.content.browser.views import is_EIONET_member

from land.copernicus.content.async import IAsyncService
from land.copernicus.content.async.subscribers import NAME as Q_NAME

from land.copernicus.content.events.download import DownloadReady
from plone.stringinterp.interfaces import IContextWrapper

MINUTE = 60
HOUR = MINUTE ** 2

B = 1
KB = 1024
MB = KB ** 2
GB = KB ** 3


def _nt_to_json(nt):
    return json.dumps({
        name: attrgetter(name)(nt)
        for name in nt._fields
    })


UNITS = namedtuple('Units', ('b', 'kb', 'mb', 'gb'))(B, KB, MB, GB)


# instead of a for-loop, will entirely "consume" a generator
CONSUME = partial(deque, maxlen=0)

URL_FETCH = '{}/fetch-land-file?hash={}'


def jsonify(request, data):
    header = request.RESPONSE.setHeader
    header("Content-Type", "application/json")
    return json.dumps(data, indent=2, sort_keys=True)


def _translate_size(size):
    try:
        number, unit = size.strip().lower().split()
    except ValueError:
        # handle "N/A"
        return 0.0

    return float(number) * attrgetter(unit)(UNITS)


def _friendly_size(size):
    # generator that divides size by the unit value
    unitsize = (
        (size / attrgetter(name)(UNITS), name) for
        name in reversed(UNITS._fields)
    )

    # get and return the first non-zero result
    res, unit = next(dropwhile(lambda x: x[0] <= 0, unitsize))
    return '{} {}'.format(res, unit.upper())


def _get_field_value(name, item):
    return item.getField(name).getAccessor(item)()


def _filename_from_url(url):
    return url.split('/')[-1]


GET_REMOTE_URL = partial(_get_field_value, 'remoteUrl')
GET_FILE_SIZE = partial(_get_field_value, 'fileSize')


class DownloadLandFileView(BrowserView):
    """ Set Google Analytics custom params
    """

    def __call__(self):
        resp = partial(jsonify, self.request)
        if api.user.is_anonymous():
            self.request.response.setStatus(401)
            return resp({'err': 'Unauthorised!'})

        remote_url = GET_REMOTE_URL(self.context)
        if not remoteUrl_exists(remote_url):
            self.request.response.setStatus(404)
            return resp({'err': 'File does not exist!'})

        try:
            return resp({
                'ga': self.values,
                'url': remote_url,
            })
        except Exception as err:
            self.request.response.setStatus(500)
            return resp({'err': err.message})

    @property
    def values(self):
        user = api.user.get_current()

        return {
            'institutional_domain': user.getProperty('institutional_domain'),
            'thematic_domain': user.getProperty('thematic_domain'),
            'is_eionet_member': is_EIONET_member(user),
            'land_item_title': self.context.title_or_id(),
        }


def _append_ext(path, ext):
    return '{}.{}'.format(path, ext)


class JobPaths(namedtuple('_JobPaths', ['base_dst', 'hash'])):

    @property
    def dst(self):
        return os.path.join(self.base_dst, self.hash)

    @property
    def zip(self):
        return _append_ext(self.dst, 'zip')

    @property
    def done(self):
        return _append_ext(self.dst, 'done')

    @property
    def metadata(self):
        return _append_ext(self.dst, 'metadata')

    def has_zip(self):
        return os.path.isfile(self.zip)

    def has_metadata(self):
        return os.path.isfile(self.metadata)

    def has_done(self):
        return os.path.isfile(self.done)


def _endln(thing):
    return '{}\n'.format(thing)


def _make_zip(path, paths):
    def mk_zip(pth):
        return zipfile.ZipFile(pth, 'w', zipfile.ZIP_STORED, True)

    with mk_zip(path) as zip_file:
        CONSUME(map(zip_file.write, paths))


def _notify_ready(context, job):
    ctx_wrapper = IContextWrapper(context)(
        userid=job.meta.userid,
        exp_time=job.meta.exp_time,
        filenames=job.meta.filenames,
        done_url=job.done_url,
    )

    notify(DownloadReady(ctx_wrapper))


def _download_executor(context, job):
    paths = JobPaths(job.dst, job.meta.hash)

    with open(paths.metadata, 'w') as metadata_file:
        metadata_file.write(_endln(_nt_to_json(job.meta)))

    if not paths.has_zip() or not paths.has_done():
        _joiner = partial(os.path.join, job.src)
        src_paths = map(_joiner, job.meta.filenames)
        _make_zip(paths.zip, src_paths)

        # mark zip as complete
        open(paths.done, 'a').close()

    _notify_ready(context, job)
    return paths.zip


Job = namedtuple('Job', ('meta', 'dst', 'src', 'done_url'))
Metadata = namedtuple('Metadata', ('hash', 'filenames', 'exp_time', 'userid'))


def _queue_download(context, metadata):
    done_url = URL_FETCH.format(context.absolute_url(), metadata.hash)
    job = Job(metadata, DST_PATH, SRC_PATH, done_url)

    worker = queryUtility(IAsyncService)
    queue = worker.getQueues()['']

    worker.queueJobInQueue(queue, (Q_NAME,), _download_executor, context, job)


def _time_from_date(date):
    return time.mktime(date.timetuple()) + date.microsecond / 1E6


def _grammar(base, val, suf='s'):
    suffix = '' if val == 1 else suf
    return '{val} {base}{suffix}'.format(val=val, base=base, suffix=suffix)


def _friendly_hours(delta):
    if delta.seconds < HOUR:
        return _grammar('minute', delta.seconds / MINUTE)
    return _grammar('hour', delta.seconds / HOUR)


def _friendly_date(date):
    return date.strftime('%H:%M %b %d, %Y')


def _view_params(meta, user, size):
    expiration = datetime.fromtimestamp(meta.exp_time)
    return dict(
        num_files=_grammar('file', len(meta.filenames)),
        email=user.getProperty('email'),
        file_hash=meta.hash,
        size=_friendly_size(int(size)),
        hours=_friendly_hours(expiration - datetime.now()),
        expires=_friendly_date(expiration)
    )


class DownloadAsyncView(BrowserView):
    """ Async download preparation.
    """

    def __call__(self, selected=[]):
        # fetch items
        selected = selected or self.request.get('selected', [])
        items = tuple(map(self.context.restrictedTraverse, selected))

        # extract files and calculate hash
        filenames = tuple(map(_filename_from_url, map(GET_REMOTE_URL, items)))
        file_hash = sha('|'.join(sorted(filenames))).hexdigest()

        # premare metadata
        user = api.user.get_current()
        exp_time = _time_from_date(datetime.now() + timedelta(days=1))
        metadata = Metadata(file_hash, filenames, exp_time, user.getId())

        # Start async job
        _queue_download(self.context, metadata)

        # prepare view params
        size = sum(map(_translate_size, map(GET_FILE_SIZE, items)))
        params = _view_params(metadata, user, size)

        # url that will track and redirect to download
        url = URL_FETCH.format(self.context.absolute_url(), file_hash)

        return self.index(url=url, **params)

    def estimate(self):
        file_hash = self.request.get('hash', None)
        paths = JobPaths(DST_PATH, file_hash)

        try:
            with open(paths.metadata, 'r') as metadata_file:
                metadata = Metadata(**(json.load(metadata_file)))
        except IOError:
            return json.dumps(dict(target=0, cur=0, proc=0))

        _joiner = partial(os.path.join, SRC_PATH)
        src_paths = map(_joiner, metadata.filenames)
        target = sum(map(os.path.getsize, src_paths))
        size = os.path.getsize(paths.zip)

        result = dict(
            target=target,
            cur=size,
            proc=100 if paths.has_done() else size * 100 / target
        )

        return json.dumps(result)


class FetchLandFileView(BrowserView):
    """ Track download and redirect to Apache-served file.
    """

    file_hash = None

    def __call__(self):
        self.file_hash = self.request.get('hash', None)
        paths = JobPaths(DST_PATH, self.file_hash)

        if not paths.has_done():
            return self.index(pending=True)

        with open(paths.metadata, 'r') as metadata_file:
            metadata = Metadata(**(json.load(metadata_file)))

        user = api.user.get_current()

        size = os.path.getsize(paths.zip)
        params = _view_params(metadata, user, size)
        same_user = user.getId() == metadata.userid
        filename = os.path.basename(paths.zip)

        return self.index(same_user=same_user, filename=filename, **params)

    def url(self):
        if self.file_hash:
            portal_url = api.portal.get().absolute_url()
            return '{}/{}/{}.zip'.format(
                portal_url.rstrip('/'),
                ST_PATH.lstrip('/').rstrip('/'),
                self.file_hash,
            )
