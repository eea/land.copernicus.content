from zope.interface import Interface
from zope import schema
from zope.component import adapter

from z3c.form import form
from z3c.form import field
from z3c.form import button

from plone.z3cform import layout

from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow

from land.copernicus.content.content.landfile import PLandFile
from land.copernicus.content.content.api import LandFileApi
from land.copernicus.content.content.interfaces import IPLandFile


class ITableRowSchema(Interface):
    name = schema.TextLine(title=u"Name", required=False)
    value = schema.TextLine(title=u"Value", required=False)


class IFormSchema(IPLandFile):
    fileCategories = schema.List(
        title=u'Categorization of this file',
        description=u'Enter, for each category, its value',
        value_type=DictRow(title=u"tablerow", schema=ITableRowSchema),
        required=False,
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
        import pdb; pdb.set_trace()
        if errors:
            return

        return self.request.RESPONSE.redirect(self.context.absolute_url())

    @button.buttonAndHandler(u'Cancel')
    def handle_cancel(self, action):
        return self.request.response.redirect(self.context.absolute_url())


class EditLandFileForm(form.Form):

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

        return self.request.RESPONSE.redirect(incident.absolute_url())

    @button.buttonAndHandler(u'Cancel')
    def handle_cancel(self, action):
        return self.request.response.redirect(self.context.absolute_url())

    @property
    def label(self):
        return 'Edit land file - {}'.format('IDK!')













AddLandFileFormView = layout.wrap_form(AddLandFileForm)
EditLandFileFormView = layout.wrap_form(EditLandFileForm)
