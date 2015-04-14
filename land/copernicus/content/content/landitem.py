""" Land content-types
"""

from Products.ATContentTypes.content.folder import ATFolder
from land.copernicus.content.config import IFRAME_WIDTH, IFRAME_HEIGHT
from land.copernicus.content.content import schema
from land.copernicus.content.content.interfaces import ILandItem
from lxml.html import fragments_fromstring, tostring
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

        html = ''
        html_elements = fragments_fromstring(value)

        for tag in html_elements:
            if tag.tag == 'iframe':
                #tag.set('width', IFRAME_WIDTH)
                tag.set('height', IFRAME_HEIGHT)
                tag.set('class', 'widen')
                tag.set('onload', "javascript:show_iframe();")
            html += tostring(tag)

        return html

    def has_iframe(self):
        field = self.getField('embed')
        value = field.getAccessor(self)()
        if not value:
            return False

        html_elements = fragments_fromstring(value)
        iframes = [iframe for iframe in html_elements
                    if iframe.tag == 'iframe']

        if iframes:
            return True

        return False

    def getLocationForCode(self, code):
        """ return location name for code
        """
        tool = getToolByName(self)
