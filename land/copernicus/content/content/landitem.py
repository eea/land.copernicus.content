""" Land content-types
"""
from zope.interface import implements

from Products.ATContentTypes.content.folder import ATFolder

from land.copernicus.content.content import schema
from land.copernicus.content.content.interfaces import ILandItem
from land.copernicus.content.content.landfile import LandFileStore


class LandItem(ATFolder):
    """ Land Item
    """

    implements(ILandItem)

    meta_type = 'LandItem'
    portal_type = 'LandItem'
    archetype_name = 'LandItem'
    schema = schema.ITEM_SCHEMA

    _landfiles = None  # type: LandFileStore

    @property
    def landfiles(self):
        """ BTree land file storage for faster operation.
            Title and shortnames need to be unique, as they are used as keys!
        """
        if self._landfiles is None:
            self._landfiles = LandFileStore()
        return self._landfiles
