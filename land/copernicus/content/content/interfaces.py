""" Content interfaces
"""
from zope.interface import Interface
from zope import schema


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


class IInProximity(Interface):
    """ In Proximity items are external links with description
    """
    email = schema.TextLine(
        title=u"External link",
        required=True,
        description=u"External link for this InProximity item."
    )
