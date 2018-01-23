""" Land content-types
"""
import BTrees

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

    _landfiles = None

    @property
    def landfiles(self):
        """ OOBTree land file storage for faster operation.
            Land file titles need to be unique, as they are used as keys.
        """
        if self._landfiles is None:
            self._landfiles = BTrees.OOBTree.BTree()
        return self._landfiles
