""" Land File: a shortcut to an FTP uploaded file
"""

from Products.ATContentTypes.content.link import ATLink
from Products.DataGridField import DataGridField    #, DataGridWidget
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
        field = ExtendedDataGridField('fileCategories',
                searchable = True,
                columns=columns,
                # widget = DataGridWidget(
                #     # columns={
                #     #     'column1' : Column("Toholampi city rox"),
                #     #     'column2' : Column("My friendly name"),
                #     #     'select_sample' : SelectColumn("Friendly name", vocabulary="getSampleVocabulary")
                #     # },
                #     ),
            )
        return [field]
