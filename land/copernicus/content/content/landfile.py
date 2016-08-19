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

    def category_exists(self, category_name):
        """ Check if a given category name exists in file categories
        """
        for category in self.context.fileCategories:
            if category.get('name', '') == category_name:
                return True
        return False

    def add_file_category(self, category_name, category_value=u""):
        """ Save new category in file categories tuple
        """
        old_file_categories = self.context.fileCategories
        new_file_category = {
            'name': category_name,
            'value': category_value
        }

        list_categories = []
        for category in old_file_categories:
            list_categories.append(category)

        list_categories.append(new_file_category)
        self.context.fileCategories = tuple(list_categories)

    def getFields(self):
        columns = self.context.getFileCategories() or []

        # When a landfile is created it has file categories defined in context.
        # If a new category is added this is not added by default in landfile
        # item. On landfile edit we fix this problem. So user can save values
        # for old categories and new ones, too.

        file_categories = columns
        saved_file_categories = self.context.fileCategories

        if len(saved_file_categories) < len(file_categories):
            for category_name in file_categories:
                if self.category_exists(category_name) is False:
                    self.add_file_category(category_name=category_name)

        default_values = [{'name': col, 'value': u''} for col in columns]
        field = ExtendedDataGridField(
            'fileCategories',
            searchable=True,
            columns=('name', 'value'),
            default=default_values,
            allow_empty_rows=True,
            allow_delete=False,
            allow_insert=False,
            allow_reorder=False,
            widget=DataGridWidget(
                label="Categorization of this file",
                description="Enter, for each category, its value"
            ),
        )
        return [field]
