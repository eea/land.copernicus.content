""" Custom content
"""
from Products.ATContentTypes.content.base import registerATCT
from land.copernicus.content.content import landsection
from land.copernicus.content.content import landitem
from land.copernicus.content.config import PACKAGE

def register():
    """ Register custom content-types
    """
    registerATCT(landsection.LandSection, PACKAGE)
    registerATCT(landitem.LandItem, PACKAGE)
