""" Land content-types
"""

from Products.ATContentTypes.content.folder import ATFolder
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
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


class LandProductSchemaExtender(object):
    implements(IOrderableSchemaExtender)

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return []

    def getOrder(self, fields):
        print self.context, "getOrder"
        fields = fields.copy()
        creators = fields['creators']
        if 'rights' in creators:
            i = creators.index('rights')
            del creators[i]
            fields['default'].append('rights')
        return fields
