""" Custom content
"""
from Products.ATContentTypes.content.base import registerATCT
from land.copernicus.content.config import PACKAGE_NAME
from land.copernicus.content.content import landfile
from land.copernicus.content.content import landitem
from land.copernicus.content.content import landsection


def register():
    """ Register custom content-types
    """
    registerATCT(landsection.LandSection, PACKAGE_NAME)
    registerATCT(landitem.LandItem, PACKAGE_NAME)
    registerATCT(landfile.LandFile, PACKAGE_NAME)
