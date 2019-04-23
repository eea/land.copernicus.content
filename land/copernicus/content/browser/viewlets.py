from contextlib import closing
from eea.cache import cache
from eventlet.green import urllib2
from plone import api
from plone.app.layout.viewlets import ViewletBase
import logging
import os
import re
import socket


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

    def get_sentry_user(self):
        return api.user.get_current().getUserName()

    @cache(lambda *args: "version", lifetime=86400)
    def get_sentry_release(self):
        return os.environ.get(
            'EEA_APP_VERSION',
            os.environ.get('EEA_KGS_VERSION', ''))

    @cache(lambda *args: "version", lifetime=86400)
    def get_sentry_server_name(self):
        try:
            return socket.gethostname()
        except Exception as err:
            logger.exception(err)
            return ""

    @cache(lambda *args: "version", lifetime=86400)
    def get_sentry_environment(self):
        environment = os.environ.get(
            'ENVIRONMENT', os.environ.get('SENTRY_ENVIRONMENT', ''))
        if not environment:
            url1 = RANCHER_METADATA + '/self/stack/environment_name'
            url2 = RANCHER_METADATA + '/self/stack/name'
            try:
                with closing(urllib2.urlopen(url1, timeout=TIMEOUT)) as con:
                    environment_a = con.read()
                with closing(urllib2.urlopen(url2, timeout=TIMEOUT)) as con:
                    environment_b = con.read()
                environment = "{0} - {1}".format(environment_a, environment_b)
            except Exception as err:
                logger.exception(err)
                environment = 'devel'
        return environment

    def get_sentry_url(self):
        try:
            return self.context.absolute_url()
        except Exception:
            return api.portal.get().absolute_url()
