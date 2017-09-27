import json
from sha import sha
from datetime import datetime
from datetime import timedelta
from functools import partial
from collections import namedtuple
from operator import attrgetter
from itertools import dropwhile

from Products.Five.browser import BrowserView

import plone.api as api

from land.copernicus.content.browser.views import remoteUrl_exists
from land.copernicus.content.browser.views import is_EIONET_member

B = 1
KB = 1024
MB = KB ** 2
GB = KB ** 3

# nice and immutable
Units = namedtuple('Units', ('b', 'kb', 'mb', 'gb'))
UNITS = Units(B, KB, MB, GB)


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


class DownloadAsyncView(BrowserView):
    """ Async download preparation.
    """

    def __call__(self, selected=[]):
        selected = selected or self.request.get('selected', [])
        items = map(self.context.restrictedTraverse, selected)

        filenames = map(_filename_from_url, map(GET_REMOTE_URL, items))
        file_hash = sha('|'.join(sorted(filenames))).hexdigest()

        size = sum(map(_translate_size, map(GET_FILE_SIZE, items)))

        url = '{}/downloads/{}.zip'.format(
            api.portal.get().absolute_url(),
            file_hash
        )

        expiration = datetime.now() + timedelta(days=1)

        return self.index(
            filenames=filenames,
            email=self.request.get('email'),
            file_hash=file_hash,
            raw_sizes=size,
            size=_friendly_size(int(size)),
            url=url,
            expires=expiration.strftime('%H:%M %b %d, %Y')
        )
