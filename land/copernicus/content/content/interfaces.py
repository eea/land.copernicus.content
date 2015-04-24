""" Content interfaces
"""
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
