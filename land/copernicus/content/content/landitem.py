""" Land content-types
"""

from Products.ATContentTypes.content.folder import ATFolder
from land.copernicus.content.content import schema
from land.copernicus.content.content.interfaces import ILandItem
from zope.interface import implements


class LandItem(ATFolder):
    """ Land Item
    """

    implements(ILandItem)

    meta_type = 'LandItem'
    portal_type = 'LandItem'
    archetype_name = 'LandItem'
    schema = schema.ITEM_SCHEMA
