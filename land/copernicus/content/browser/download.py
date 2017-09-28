import os
import json
import zipfile
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

from Products.Five.browser import BrowserView

import plone.api as api

from land.copernicus.content.config import ENV_DL_SRC_PATH as SRC_PATH
from land.copernicus.content.config import ENV_DL_DST_PATH as DST_PATH
from land.copernicus.content.config import ENV_DL_STATIC_PATH as ST_PATH

from land.copernicus.content.browser.views import remoteUrl_exists
from land.copernicus.content.browser.views import is_EIONET_member

from land.copernicus.content.async import IAsyncService
from land.copernicus.content.async.subscribers import NAME as Q_NAME

B = 1
KB = 1024
MB = KB ** 2
GB = KB ** 3

# nice and immutable
Units = namedtuple('Units', ('b', 'kb', 'mb', 'gb'))
UNITS = Units(B, KB, MB, GB)


CONSUME = partial(deque, maxlen=0)


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


def _make_zip(path, paths):
    def mk_zip(pth):
        return zipfile.ZipFile(pth, 'w', zipfile.ZIP_STORED, True)

    with mk_zip(path) as zip_file:
        CONSUME(map(zip_file.write, paths))


def _download_executor(context, job):
    paths = JobPaths(job.dst, job.hash)

    with open(paths.metadata, 'w') as metadata_file:
        metadata_file.writelines([name + '\n' for name in job.filenames])
        metadata_file.write(job.expiration.isoformat())

    if not paths.has_zip() or not paths.has_done():
        src_paths = [os.path.join(job.src, name) for name in job.filenames]
        _make_zip(paths.zip, src_paths)

        # mark zip as complete
        open(paths.done, 'a').close()

    return paths.zip


Job = namedtuple('Job', ('filenames', 'hash', 'expiration', 'dst', 'src'))


def _queue_download(context, filenames, file_hash, expiration):
    job = Job(filenames, file_hash, expiration, DST_PATH, SRC_PATH)

    worker = queryUtility(IAsyncService)
    queue = worker.getQueues()['']

    worker.queueJobInQueue(queue, (Q_NAME,), _download_executor, context, job)


class DownloadAsyncView(BrowserView):
    """ Async download preparation.
    """

    def __call__(self, selected=[]):
        selected = selected or self.request.get('selected', [])
        items = tuple(map(self.context.restrictedTraverse, selected))

        filenames = tuple(map(_filename_from_url, map(GET_REMOTE_URL, items)))
        file_hash = sha('|'.join(sorted(filenames))).hexdigest()

        size = sum(map(_translate_size, map(GET_FILE_SIZE, items)))

        url = '{}/fetch-land-file?hash={}'.format(
            api.portal.get().absolute_url(),
            file_hash
        )

        expiration = datetime.now() + timedelta(days=1)

        _queue_download(self.context, filenames, file_hash, expiration)

        return self.index(
            num_files=len(filenames),
            email=self.request.get('email'),
            file_hash=file_hash,
            raw_sizes=size,
            size=_friendly_size(int(size)),
            url=url,
            expires=expiration.strftime('%H:%M %b %d, %Y')
        )


class FetchLandFileView(BrowserView):
    """ Track download and redirect to Apache-served file.
    """

    file_hash = None

    def __call__(self):
        self.file_hash = self.request.get('hash', None)
        paths = JobPaths(DST_PATH, self.file_hash)

        with open(paths.metadata, 'r') as metadata_file:
            metadata_content = metadata_file.read().split()
            filenames, date = metadata_content[:-1], metadata_content[-1]
            size = os.path.getsize(paths.zip)

        return self.index(
            num_files=len(filenames),
            email='to@do.me',
            size=_friendly_size(int(size)),
            filename=os.path.basename(paths.zip),
        )

    def url(self):
        if self.file_hash:
            portal_url = api.portal.get().absolute_url()
            return '{}/{}/{}.zip'.format(
                portal_url.rstrip('/'),
                ST_PATH.lstrip('/').rstrip('/'),
                self.file_hash,
            )
