""" Land Product: a type of dataset
"""

from Products.ATContentTypes.content.folder import ATFolder
from land.copernicus.content.content import schema
from land.copernicus.content.content.interfaces import ILandProduct
from zope.interface import implements


class LandProduct(ATFolder):
    """ Land Item
    """

    implements(ILandProduct)

    meta_type = 'LandProduct'
    portal_type = 'LandProduct'
    archetype_name = 'LandProduct'
    schema = schema.PRODUCT_SCHEMA
