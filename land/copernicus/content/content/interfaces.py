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
