""" Land File: a shortcut to an FTP uploaded file
"""

from Products.ATContentTypes.content.link import ATLink
from Products.DataGridField import DataGridField
from Products.DataGridField import DataGridWidget
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender
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

class ExtendedDataGridField(ExtensionField, DataGridField):
    """ Extended datagridfield
    """


class SchemaExtender(object):
    implements(ISchemaExtender)

    def __init__(self, context):
        self.context = context

    def getFields(self):
        columns = self.context.getFileCategories() or []
        default_values = [{'name':col, 'value':u''} for col in columns]
        field = ExtendedDataGridField(
            'fileCategories',
            searchable = True,
            columns=('name', 'value'),
            default=default_values,
            allow_empty_rows=True,
            allow_delete=False,
            allow_insert=False,
            allow_reorder=False,
            widget = DataGridWidget(
                label="Categorization of this file",
                description="Enter, for each category, its value"
                #columns=column_defs,
            ),
        )
        return [field]
