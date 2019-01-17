from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
import json
import transaction


def getvalue(value):
    if value:
        return value.strip()


class FilesLibraryItemView(BrowserView):
    """ Files Library Item view
    """
    index = ViewPageTemplateFile("templates/fileslibraryitem_view.pt")

    def render(self):
        return self.index()

    def __call__(self):
        return self.render()


class FilesLibraryItemAdminView(BrowserView):
    """ Administration view for Files Library Item
    """
    index = ViewPageTemplateFile("templates/fileslibraryitem_admin.pt")

    def render(self):
        return self.index()

    @property
    def existing_files_in_context(self):
        files_ids = [x.id for x in api.content.find(
            context=self.context, depth=1, portal_type="File")]

        return json.dumps(files_ids)

    def _create_file(self, uploaded_file):
        item = api.content.create(
            container=self.context,
            type="File",
            file=uploaded_file,
            id=getvalue(uploaded_file.filename),
            title=getvalue(uploaded_file.filename),
            safe_id=True
            )

        return item

    def __call__(self):
        if self.request.method == 'POST':
            data = self.request.form.get("exported-json", None)
            if data:
                self.context.json_data = data
                transaction.commit()

            uploaded_file = self.request.form.get("file", None)
            if uploaded_file:
                result = self._create_file(uploaded_file)
                return result.title

        return self.render()
