""" Content interfaces
"""
from zope import schema
from zope.interface import Interface


class ILandContent(Interface):
    """ Abstract
    """


class ILandSection(ILandContent):
    """ Folderish sections
    """


class ILandItem(ILandContent):
    """ Bottom items
    """


class ILandProduct(Interface):
    """ LandProducts are similar to a Dataset from eea.dataservice
    """


class ILandFile(Interface):
    """ LandFile are links to files on FTP
    """


class IPLandFile(Interface):
    """ Lightweight implementation of LandFile,
        inheriting only from persistent.Persistent,
        the bare-minimum requirement for ZODB storage.
    """
    title = schema.TextLine(title=u'Title', required=True)
    shortname = schema.TextLine(
        title=u'Short name',
        required=True
    )
    description = schema.Text(title=u'Description', required=False)
    remoteUrl = schema.URI(title=u'URL', required=True)
    fileSize = schema.TextLine(
        title=u'Download file size',
        description=u'Leave this field empty. It is automatically extracted.',
        default=u'N/A',
        required=False
    )
    fileCategories = schema.Tuple(
        title=u'Categorization of this file',
        description=u'Enter, for each category, its value',
        required=False
    )
