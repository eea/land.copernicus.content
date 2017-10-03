from datetime import datetime

from plone.stringinterp.adapters import BaseSubstitution

import plone.api as api

from land.copernicus.content.config import EEAMessageFactory as _

from land.copernicus.content.browser.download import _friendly_date


class UserName(BaseSubstitution):
    category = _(u'Async download')
    description = _(u'User first name')

    def safe_call(self):
        user = api.user.get(userid=self.wrapper.userid)
        return user.getProperty('fullname') or u''


class UserEmail(BaseSubstitution):
    category = _(u'Async download')
    description = _(u'User email')

    def safe_call(self):
        user = api.user.get(userid=self.wrapper.userid)
        return user.getProperty('email') or u''


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
        joiner = '\n* '
        return joiner + joiner.join(self.wrapper.filenames)


class NumFiles(BaseSubstitution):
    category = _(u'Async download')
    description = _(u'Number of files')

    def safe_call(self):
        return len(self.wrapper.filenames)


class URL(BaseSubstitution):
    category = _(u'Async download')
    description = _(u'Download URL')

    def safe_call(self):
        return self.wrapper.done_url
