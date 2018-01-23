import os
import re
from ZPublisher import HTTPResponse
from plone.app.layout.viewlets import ViewletBase


class SentryViewlet(ViewletBase):
    """Sentry script viewlet"""

    def render(self):
        return super(ViewletBase, self).render()

    def get_dsn(self):
        dsn = os.environ.get("SENTRY_DSN")
        if not dsn or dsn=='':
            return False
        passwd = re.search(r'.*(:.*?)@.*', dsn).group(1)
        return dsn.replace(passwd, '')
