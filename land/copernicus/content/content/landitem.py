""" Land content-types
"""

from Products.ATContentTypes.content.folder import ATFolder
from land.copernicus.content.config import IFRAME_WIDTH, IFRAME_HEIGHT
from land.copernicus.content.content import schema
from land.copernicus.content.content.interfaces import ILandItem
from lxml.html import fragment_fromstring, tostring
from zope.interface import implements


class LandItem(ATFolder):
    """ Land Item
    """

    implements(ILandItem)

    meta_type = 'LandItem'
    portal_type = 'LandItem'
    archetype_name = 'LandItem'
    schema = schema.ITEM_SCHEMA

    def embed_iframe(self):
        field = self.getField('embed')
        value = field.getAccessor(self)()
        if not value:
            return ""

        iframe = fragment_fromstring(value)
        if iframe.tag == "iframe":
            #iframe.set('width', IFRAME_WIDTH)
            iframe.set('height', IFRAME_HEIGHT)
            iframe.set('class', 'widen')
            iframe.set('onload', "javascript:show_iframe();")

        return tostring(iframe)

    def has_iframe(self):
        field = self.getField('embed')
        value = field.getAccessor(self)()
        if not value:
            return False

        iframe = fragment_fromstring(value)
        if iframe.tag == "iframe":
            return True

        return False
