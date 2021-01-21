""" Content interfaces
"""
from plone.app.textfield import RichText
from plone.namedfile import field as namedfile
from plone.supermodel import model
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


class IFilesLibraryItem(model.Schema):
    """ Files Library Item (as used for Technical Library)
    """
    text = RichText(
        title=u"Body text",
        required=False,
    )

    search_filters = schema.Text(
        title=u"Search filters",
        description=u"""One per line.""",
        required=False,
    )

    json_data = schema.Text(
        title=u"Data",
        required=False,
        description=u"Ignore it. It's automatically filled in edit mode."
    )


class IDashboardItem(model.Schema):
    """ Dashboard Item
    """
    text = RichText(
        title=u"Body text",
        required=False,
    )

    iframe_data = schema.Text(
        title=u"Iframe Data",
        required=False,
        description=u"The embed code for dashboard iframe."
    )

    logo = namedfile.NamedBlobImage(
        title=u'Logo',
        required=True,
    )
