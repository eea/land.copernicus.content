""" Custom schema
"""
from Products.ATContentTypes.content.folder import ATFolder
from Products.Archetypes import atapi

SCHEMA = atapi.Schema((
))

SECTION_SCHEMA = ATFolder.schema.copy() + SCHEMA.copy()
ITEM_SCHEMA = ATFolder.schema.copy() + SCHEMA.copy()
