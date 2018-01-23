import os
import re
from plone.app.layout.viewlets import ViewletBase


class SentryViewlet(ViewletBase):
    """Sentry script viewlet"""

    def render(self):
        return super(ViewletBase, self).render()

    def has_dsn(self):
        if 'SENTRY_DSN' in os.environ.keys() and os.environ['SENTRY_DSN'] != '':
            return True
        return False

    def get_dsn(self):
        dsn = os.environ["SENTRY_DSN"]
        passwd = re.search(r'.*(:.*?)@.*', dsn).group(1)
        return dsn.replace(passwd, '')
