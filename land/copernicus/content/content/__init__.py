""" Custom content
"""
from Products.ATContentTypes.content.base import registerATCT
from land.copernicus.content.config import PACKAGE
from land.copernicus.content.content import landfile
from land.copernicus.content.content import landitem
from land.copernicus.content.content import landsection

def register():
    """ Register custom content-types
    """
    registerATCT(landsection.LandSection, PACKAGE)
    registerATCT(landitem.LandItem, PACKAGE)
    registerATCT(landfile.LandFile, PACKAGE)
