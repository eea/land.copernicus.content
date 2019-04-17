from contextlib import closing
from eea.cache import cache
from eventlet.green import urllib2
from plone import api
from plone.app.layout.viewlets import ViewletBase
import logging
import os
import re


logger = logging.getLogger("land.copernicus.content")

RANCHER_METADATA = 'http://rancher-metadata/latest'
TIMEOUT = 15


class SentryViewlet(ViewletBase):
    """Sentry script viewlet"""

    def render(self):
        return super(ViewletBase, self).render()

    def get_dsn(self):
        dsn = os.environ.get("SENTRY_DSN")
        if dsn:
            passwd = re.search(r'.*(:.*?)@.*', dsn).group(1)
            return dsn.replace(passwd, '')

    @cache(lambda *args: "version", lifetime=86400)
    def get_sentry_release(self):
        return os.environ.get(
            'EEA_APP_VERSION',
            os.environ.get('EEA_KGS_VERSION', ''))

    @cache(lambda *args: "version", lifetime=86400)
    def get_sentry_server_name(self):
        return os.environ.get('SERVER_NAME', '')

    @cache(lambda *args: "version", lifetime=86400)
    def get_sentry_environment(self):
        environment = os.environ.get(
            'ENVIRONMENT', os.environ.get('SENTRY_ENVIRONMENT', ''))
        if not environment:
            url = RANCHER_METADATA + '/self/stack/environment_name'
            try:
                with closing(urllib2.urlopen(url, timeout=TIMEOUT)) as con:
                    environment = con.read()
            except Exception as err:
                logger.exception(err)
                environment = 'devel'
        return environment

    def get_sentry_url(self):
        try:
            return self.context.absolute_url()
        except Exception:
            return api.portal.get().absolute_url()
