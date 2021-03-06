from zope.interface import Interface
from zope.interface import Invalid

from zope import schema

from z3c.form.interfaces import HIDDEN_MODE
from z3c.form.interfaces import DISPLAY_MODE
from z3c.form.interfaces import ActionExecutionError

from z3c.form import form
from z3c.form import field
from z3c.form import button

from plone.z3cform import layout

from Products.statusmessages.interfaces import IStatusMessage

from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow

from land.copernicus.content.content.api import LandFileApi
from land.copernicus.content.content.interfaces import IPLandFile


LANDFILE_LISTING = '{}/landfiles_content'


class ITableRowSchema(Interface):
    name = schema.TextLine(title=u"Name", required=False)
    value = schema.TextLine(title=u"Value", required=False)


class IFormSchema(IPLandFile):
    shortname = schema.TextLine(
        title=u'Shortname',
        description=u'Used by the edit form to identify the land file.'
    )
    fileCategories = schema.List(
        title=u'Categorization of this file',
        description=u'Enter, for each category, its value',
        value_type=DictRow(title=u"tablerow", schema=ITableRowSchema),
        required=False,
    )


def fields_landfile(categories, landfile):
    landfile_categories = dict(landfile.fileCategories)
    fileCategories = [
        {'name': name, 'value': landfile_categories.get(name, u'')}
        for name in categories
    ]
    return dict(
        title=landfile.title,
        description=landfile.description,
        remoteUrl=landfile.remoteUrl,
        fileSize=landfile.fileSize,
        fileCategories=fileCategories,
    )


class BaseForm(form.Form):
    def redirect_to_listing(self):
        return self.request.RESPONSE.redirect(
            LANDFILE_LISTING.format(self.context.absolute_url())
        )


class AddLandFileForm(BaseForm):
    label = 'Add land file'

    fields = field.Fields(IFormSchema).select(
        'title',
        'description',
        'remoteUrl',
        'fileCategories',
    )
    fields['fileCategories'].widgetFactory = DataGridFieldFactory

    ignoreContext = True

    def updateWidgets(self, prefix=None):
        super(AddLandFileForm, self).updateWidgets(prefix)

        categories = self.widgets['fileCategories']
        categories.allow_insert = False
        categories.allow_delete = False
        categories.allow_reorder = False
        categories.auto_append = False

        columns = self.context.getFileCategories() or []
        categories.value = categories.value or [
            {'name': col, 'value': u''}
            for col in columns
        ]

    @button.buttonAndHandler(u'Save')
    def handle_save(self, action):
        data, errors = self.extractData()
        if errors:
            return

        props = dict(
            title=data['title'],
            description=data.get('description', ''),
            remoteUrl=data['remoteUrl'],
            fileCategories=tuple(
                tuple(x.values())
                for x in data['fileCategories']
            )
        )

        lfa = LandFileApi(self.context.landfiles)
        try:
            landfile = lfa.add_with_filesize(**props)
        except (KeyError, OSError) as err:
            raise ActionExecutionError(Invalid(err.message))

        messages = IStatusMessage(self.request)
        messages.add(u'Added landfile: {}'.format(landfile.title))

        self.redirect_to_listing()

    @button.buttonAndHandler(u'Cancel')
    def handle_cancel(self, action):
        self.redirect_to_listing()


class EditLandFileForm(BaseForm):
    label = 'Edit land file'

    fields = field.Fields(IFormSchema).select(
        'shortname',
        'title',
        'description',
        'remoteUrl',
        'fileCategories',
    )
    fields['fileCategories'].widgetFactory = DataGridFieldFactory

    ignoreContext = False

    def updateWidgets(self, prefix=None):
        super(EditLandFileForm, self).updateWidgets(prefix)

        # Needed to preserve the title of the landfile that will be modified.
        shortname = self.widgets['shortname']
        shortname.mode = HIDDEN_MODE
        shortname.value = self.request.get('form.widgets.shortname')

        categories = self.widgets['fileCategories']
        categories.allow_insert = False
        categories.allow_delete = False
        categories.allow_reorder = False
        categories.auto_append = False

    def getContent(self):
        shortname = self.request.get('form.widgets.shortname', None)
        content = dict()
        if shortname:
            lfa = LandFileApi(self.context.landfiles)
            categories = self.context.getFileCategories() or []
            landfile = lfa.get_by_shortname(shortname)
            if landfile:
                content = fields_landfile(categories, landfile)
            else:
                messages = IStatusMessage(self.request)
                messages.add(
                    u'No landfile with shortname {}!'.format(shortname),
                    type='error'
                )
        return content

    @button.buttonAndHandler(u'Update')
    def handle_save(self, action):
        data, errors = self.extractData()
        if errors:
            return

        props = dict(
            title=data['title'],
            description=data.get('description', ''),
            remoteUrl=data['remoteUrl'],
            fileCategories=tuple(
                tuple(x.values())
                for x in data['fileCategories']
            )
        )

        lfa = LandFileApi(self.context.landfiles)
        orig = lfa.get_by_shortname(data['shortname'])
        try:
            landfile = lfa.edit_with_filesize(orig.title, **props)
        except (KeyError, OSError) as err:
            raise ActionExecutionError(Invalid(err.message))

        messages = IStatusMessage(self.request)
        messages.add(u'Edited landfile: {}'.format(landfile.title))

        self.redirect_to_listing()

    @button.buttonAndHandler(u'Cancel')
    def handle_cancel(self, action):
        self.redirect_to_listing()


class DeleteLandFileForm(EditLandFileForm):
    label = 'Delete land file'
    mode = DISPLAY_MODE

    def updateWidgets(self, prefix=None):
        super(DeleteLandFileForm, self).updateWidgets(prefix)

        # Needed to preserve the title of the landfile that will be deleted.
        shortname = self.widgets['shortname']
        shortname.mode = HIDDEN_MODE
        shortname.value = self.request.get('form.widgets.shortname')

    @button.buttonAndHandler(u'Delete')
    def handle_delete(self, action):
        data, errors = self.extractData()
        if errors:
            return

        lfa = LandFileApi(self.context.landfiles)
        orig = lfa.get_by_shortname(data['shortname'])
        title = orig.title
        try:
            lfa.delete(title)
        except KeyError as err:
            raise ActionExecutionError(Invalid(err.message))

        messages = IStatusMessage(self.request)
        messages.add(u'Deleted landfile: {}'.format(title))

        self.redirect_to_listing()

    @button.buttonAndHandler(u'Cancel')
    def handle_cancel(self, action):
        self.redirect_to_listing()


AddLandFileFormView = layout.wrap_form(AddLandFileForm)
EditLandFileFormView = layout.wrap_form(EditLandFileForm)
DeleteLandfileFormView = layout.wrap_form(DeleteLandFileForm)
