""" Init
"""
from Products.CMFCore import utils
from Products.Archetypes import atapi
from land.copernicus.content.config import PACKAGE, ADD_PERMISSION
from land.copernicus.content import content

def initialize(context):
    """ Initialize product (called by zope2)
    """
    content.register()

    #Initialize portal content
    content_types, constructors, ftis = atapi.process_types(
        atapi.listTypes(PACKAGE),
        PACKAGE)

    utils.ContentInit(PACKAGE,
        content_types=content_types,
        permission=ADD_PERMISSION,
        extra_constructors=constructors, fti=ftis).initialize(context)
