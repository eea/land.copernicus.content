from zope.interface import Interface
from zope.interface import Invalid
from zope.interface import implementer

from zope import schema

from z3c.form.interfaces import HIDDEN_MODE
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


class ITableRowSchema(Interface):
    name = schema.TextLine(title=u"Name", required=False)
    value = schema.TextLine(title=u"Value", required=False)


class IFormSchema(IPLandFile):
    orig_title = schema.TextLine(
        title=u'Original title',
        description=u'Used by the edit form to remember the title.'
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
        shortname=landfile.shortname,
        remoteUrl=landfile.remoteUrl,
        fileSize=landfile.fileSize,
        fileCategories=fileCategories,
    )


class AddLandFileForm(form.Form):
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
        categories.value = [{'name': col, 'value': u''} for col in columns]

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
        except (KeyError, OSError, AssertionError) as err:
            raise ActionExecutionError(Invalid(err.message))

        messages = IStatusMessage(self.request)
        messages.add(u'Added landfile: {}'.format(landfile.title))

        return self.request.RESPONSE.redirect(self.context.absolute_url())

    @button.buttonAndHandler(u'Cancel')
    def handle_cancel(self, action):
        return self.request.response.redirect(self.context.absolute_url())


class EditLandFileForm(form.Form):
    label = 'Edit land file'

    fields = field.Fields(IFormSchema).select(
        'orig_title',
        'title',
        'shortname',
        'description',
        'remoteUrl',
        'fileCategories',
    )
    fields['fileCategories'].widgetFactory = DataGridFieldFactory

    ignoreContext = False

    def updateWidgets(self, prefix=None):
        super(EditLandFileForm, self).updateWidgets(prefix)

        orig_title = self.widgets['orig_title']
        orig_title.mode = HIDDEN_MODE
        orig_title.value = self.request.get('form.widgets.orig_title')

        categories = self.widgets['fileCategories']
        categories.allow_insert = False
        categories.allow_delete = False
        categories.allow_reorder = False
        categories.auto_append = False

    def getContent(self):
        title = self.request.get('form.widgets.orig_title', None)
        content = dict()
        if title:
            lfa = LandFileApi(self.context.landfiles)
            categories = self.context.getFileCategories() or []
            landfile = lfa.get(title)
            if landfile:
                content = fields_landfile(categories, landfile)
            else:
                messages = IStatusMessage(self.request)
                messages.add(
                    u'No landfile with title {}!'.format(title),
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
            shortname=data['shortname'],
            description=data.get('description', ''),
            remoteUrl=data['remoteUrl'],
            fileCategories=tuple(
                tuple(x.values())
                for x in data['fileCategories']
            )
        )

        lfa = LandFileApi(self.context.landfiles)
        try:
            landfile = lfa.edit_with_filesize(
                data['orig_title'], **props)
        except (KeyError, OSError) as err:
            raise ActionExecutionError(Invalid(err.message))

        messages = IStatusMessage(self.request)
        messages.add(u'Edited landfile: {}'.format(landfile.title))

        return self.request.RESPONSE.redirect(self.context.absolute_url())

    @button.buttonAndHandler(u'Cancel')
    def handle_cancel(self, action):
        return self.request.response.redirect(self.context.absolute_url())


class DeleteLandFileForm(form.Form):

    ignoreContext = True

    def getContent(self):
        title = self.context.get('title', None)
        if title:
            lfa = LandFileApi(self.context.landfiles)
            landfile = lfa.get(title)
            return landfile
        else:
            self.request.response.redirect(self.context.absolute_url())

    @button.buttonAndHandler(u'Update')
    def handle_save(self, action):
        data, errors = self.extractData()
        if errors:
            return

        return self.request.RESPONSE.redirect(self.context.absolute_url())

    @button.buttonAndHandler(u'Cancel')
    def handle_cancel(self, action):
        return self.request.response.redirect(self.context.absolute_url())

    @property
    def label(self):
        return 'Edit land file - {}'.format('IDK!')


AddLandFileFormView = layout.wrap_form(AddLandFileForm)
EditLandFileFormView = layout.wrap_form(EditLandFileForm)
DeleteLandfileFormView = layout.wrap_form(DeleteLandFileForm)
