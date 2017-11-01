from datetime import datetime
from operator import methodcaller
from itertools import imap as map

from plone.stringinterp.adapters import BaseSubstitution

import plone.api as api

from land.copernicus.content.config import EEAMessageFactory as _

from land.copernicus.content.browser.download import _friendly_date


def _starlist(filenames):
    joiner = '\n* '
    return joiner + joiner.join(filenames)


class UserName(BaseSubstitution):
    category = _(u'Async download')
    description = _(u'User full name')

    def safe_call(self):
        # Need to get fullname as LDAP does not provide first/last names.
        user = api.user.get(userid=self.wrapper.userid)
        return user.getProperty('fullname') or u''


class UserEmail(BaseSubstitution):
    category = _(u'Async download')
    description = _(u'User email')

    def safe_call(self):
        user = api.user.get(self.wrapper.userid)
        return user.getProperty('email')


class ExpDate(BaseSubstitution):
    category = _(u'Async download')
    description = _(u'Download expiration date')

    def safe_call(self):
        expires = datetime.fromtimestamp(self.wrapper.exp_time)
        return _friendly_date(expires)


class FilesComma(BaseSubstitution):
    category = _(u'Async download')
    description = _(u'List of files, comma separated')

    def safe_call(self):
        return ', '.join(self.wrapper.filenames)


class FilesStar(BaseSubstitution):
    category = _(u'Async download')
    description = _(u'List of files, newline and leading *')

    def safe_call(self):
        return _starlist(self.wrapper.filenames)


class NumFiles(BaseSubstitution):
    category = _(u'Async download')
    description = _(u'Number of files')

    def safe_call(self):
        return len(self.wrapper.filenames)


def _missing_list(filenames):
    return (
        '\n'
        'The following {} files are missing '
        'and are not included in the archive: \n {}.'
        '\n'
    ).format(len(filenames), _starlist(filenames)) if filenames else ''


class MissingFiles(BaseSubstitution):
    category = _(u'Async download')
    description = _(u'Missing files block')

    def safe_call(self):
        return _missing_list(self.wrapper.missing_files) or u''


class URL(BaseSubstitution):
    category = _(u'Async download')
    description = _(u'Download URL')

    def safe_call(self):
        return self.wrapper.done_url
