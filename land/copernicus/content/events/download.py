from zope.interface import implementer
from zope.component.interfaces import IObjectEvent


class IDownloadReady(IObjectEvent):
    """ Land download package is ready.
    """


@implementer(IDownloadReady)
class DownloadReady(object):
    def __init__(self, context, **kwargs):
        self.object = context
