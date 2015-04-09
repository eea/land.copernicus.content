""" Land File: a shortcut to an FTP uploaded file
"""

from Products.ATContentTypes.content.link import ATLink
from land.copernicus.content.content import schema
from land.copernicus.content.content.interfaces import ILandFile
from zope.interface import implements


class LandFile(ATLink):
    """ Land Link for a Land Product
    """

    implements(ILandFile)

    meta_type = 'LandFile'
    portal_type = 'LandFile'
    archetype_name = 'LandFile'
    schema = schema.LANDFILE_SCHEMA

