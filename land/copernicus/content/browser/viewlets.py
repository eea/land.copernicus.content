import os
import re
from plone.app.layout.viewlets import ViewletBase


class SentryViewlet(ViewletBase):
    """Sentry script viewlet"""

    def render(self):
        return super(ViewletBase, self).render()

    def get_dsn(self):
        dsn = os.environ["SENTRY_DSN"]
        passwd = re.search(r'.*(:.*?)@.*', dsn).group(1)
        return dsn.replace(passwd, '')
