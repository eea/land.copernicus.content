""" Schema extender
"""
from zope.interface import implements
from Products.Archetypes import atapi
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from land.copernicus.content.config import EEAMessageFactory as _


class BooleanField(ExtensionField, atapi.BooleanField):
    """ Boolean field."""


class StringField(ExtensionField, atapi.StringField):
    """ String field """


class TextField(ExtensionField, atapi.TextField):
    """ Text field """


class ImageField(ExtensionField, atapi.ImageField):
    """ Image field """


class Extender(object):
    """ Extender
    """
    implements(ISchemaExtender)

    fields = [
        BooleanField("frozen",
                     schemata="default",
                     widget=atapi.BooleanWidget(
                         label=_("Freze this item"),
                         description=_(
                             "Freeze this item and make it unclickable"))
                     ),
        ImageField("image",
                   schemata="default",
                   sizes=None,
                   widget=atapi.ImageWidget(
                       label=_("Thumbnail"),
                       description=_("Image for thumbnail"))
                   ),
        StringField("url",
                    schemata="default",
                    widget=atapi.StringWidget(
                        label=_("More details URL"),
                        description=_("Provide an external link, if any"))
                    ),
        TextField("text",
                  schemata="default",
                  primary=True,
                  allowable_content_types=('text/html',),
                  default_content_type='text/html',
                  default_output_type='text/html',
                  widget=atapi.RichWidget(
                      label=_("Rich text"),
                      description=_("Detailed body for this item"))
                  ),
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields


class LandItemExtender(object):
    """ Extender for LandItem
    """
    implements(ISchemaExtender)

    fields = [
        TextField("text",
                  schemata="default",
                  primary=True,
                  allowable_content_types=('text/html',),
                  default_content_type='text/html',
                  default_output_type='text/html',
                  widget=atapi.RichWidget(
                      label=_("Metadata"),
                      description=_("Metadata for this item"))
                  ),
        StringField("embed",
                    schemata="default",
                    widget=atapi.TextAreaWidget(
                        label=_("Map View"),
                        description=_("Paste here the code provided "
                                      "by your webservice (iframe, jscode)"))
                    ),
        TextField("webservices",
                  schemata="default",
                  primary=False,
                  allowable_content_types=('text/html',),
                  default_content_type='text/html',
                  default_output_type='text/html',
                  widget=atapi.RichWidget(
                      label=_("Web Map Services"),
                      description=_(
                          "Web Map Services available for this data"))
                  ),
        TextField("download",
                  schemata="default",
                  primary=False,
                  allowable_content_types=('text/html',),
                  default_content_type='text/html',
                  default_output_type='text/html',
                  widget=atapi.RichWidget(
                      label=_("Download"),
                      description=_("Download information"))
                  ),
        ImageField("legend",
                   schemata="default",
                   sizes=None,
                   widget=atapi.ImageWidget(
                       label=_("Legend"),
                       description=_("Image for Legend"))
                   ),
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields


class ATBlobModifier(object):
    """ SchemaModifier for ATBlob
    """
    implements(ISchemaModifier)

    def fiddle(self, schema):
        schema['auto_cover'] = BooleanField(
            "auto_cover",
            schemata="default",
            widget=atapi.BooleanWidget(
                label=_("Generate cover automatically."),
                description=_(
                     "Select this to create a cover image based "
                     "on the uplodaded file. Only available for "
                     "PDF files."
                )
            )
        )
        if not schema.get('image'):
            schema['image'] = ImageField("image",
                                         schemata="default",
                                         sizes=None,
                                         widget=atapi.ImageWidget(
                                             label=_("Cover"),
                                             description=_(
                                                 "Cover for Publication"))
                                         )

    def __init__(self, context):
        self.context = context
