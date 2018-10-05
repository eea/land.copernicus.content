from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from eea.meeting.interfaces.layer import IMeetingLayer


class ILandCopernicusContentLayer(IDefaultBrowserLayer, IMeetingLayer):
    """ Marker interface that defines a browser layer. """
