from zope.interface import implementer
from plone.dexterity.content import Container
from land.copernicus.content.interfaces import IFilesLibraryItem


@implementer(IFilesLibraryItem)
class FilesLibraryItem(Container):
    """ FilesLibraryItem content type"""
