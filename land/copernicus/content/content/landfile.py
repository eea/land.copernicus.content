""" Land File: a shortcut to an FTP uploaded file
"""

from hashlib import sha256

import persistent

from zope.interface import implementer
from zope.component import queryUtility

import BTrees

from plone.i18n.normalizer.interfaces import IURLNormalizer

from Products.ATContentTypes.content.link import ATLink
from Products.DataGridField import DataGridField
from Products.DataGridField import DataGridWidget

from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender

from land.copernicus.content.content import schema
from land.copernicus.content.content.interfaces import ILandFile
from land.copernicus.content.content.interfaces import IPLandFile


MOD_64 = 18446744073709551616  # 2**64
SHIFT_63 = 9223372036854775808  # 2**63


def _long_hash(hashable):
    """ Convert string to 64bit signed int.
        May create collisions some time after the universe dies.
    """
    return (int(sha256(hashable).hexdigest(), 16) % MOD_64) - SHIFT_63


class LandFileStore(persistent.Persistent):
    tree = None  # type: BTree.LOBTree.BTree((long(title), PLandFile))
    ids = None   # type: BTree.LLBTree.BTree((long(shortname), long(title))

    def __init__(self):
        self.tree = BTrees.LOBTree.BTree()
        self.ids = BTrees.LLBTree.BTree()

    def add(self, landfile):
        tree, ids = self.tree, self.ids

        hash_title = _long_hash(landfile.title)
        hash_shortname = _long_hash(landfile.shortname)

        if tree.get(hash_title):
            raise KeyError('Land file with same title exists!')
        if ids.get(hash_shortname):
            raise KeyError('Land file with same shortname exists!')
        else:
            tree[hash_title] = landfile
            ids[hash_shortname] = hash_title

        return landfile

    def edit(self, old_title, landfile):
        self.delete(old_title)
        self.add(landfile)

    def delete(self, title):
        hash_title = _long_hash(title)
        landfile = _long_hash(hash_title)

        hash_shortname = _long_hash(landfile.shortname)

        del self.tree[hash_title]
        del self.ids[hash_shortname]

    def get_by_title(self, title):
        hash_title = _long_hash(title)
        return self.tree.get(hash_title)

    def get_by_shortname(self, shortname):
        hash_shortname = _long_hash(shortname)
        hash_title = self.ids.get(hash_shortname)
        return self.tree.get(hash_title)

    def get_by_prop(self, propname, propvalue):
        for landfile in self.tree.values():
            if getattr(landfile, propname) == propvalue:
                yield landfile


@implementer(IPLandFile)
class PLandFile(persistent.Persistent):
    """ Lightweight implementation of LandFile,
        inheriting only from persistent.Persistent,
        the bare-minimum requirement for ZODB storage.
    """
    title = ''
    description = ''
    shortname = ''
    remoteUrl = ''
    _fileSize = 'N/A'
    fileCategories = tuple()

    def __init__(self, **fields):
        for name, value in fields.items():
            setattr(self, name, value)
        if not self.shortname:
            self.shortname = queryUtility(IURLNormalizer).normalize(self.title)

    @property
    def fileSize(self):
        return getattr(self, '_fileSize', 'N/A')

    def int_hash_title(self):
        return _long_hash(self.title)

    def int_hash_shortname(self):
        return _long_hash(self.shortname)


@implementer(ILandFile)
class LandFile(ATLink):
    """ Land Link for a Land Product
    """

    meta_type = 'LandFile'
    portal_type = 'LandFile'
    archetype_name = 'LandFile'
    schema = schema.LANDFILE_SCHEMA


class ExtendedDataGridField(ExtensionField, DataGridField):
    """ Extended datagridfield
    """


@implementer(ISchemaExtender)
class SchemaExtender(object):

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
