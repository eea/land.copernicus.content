from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
import json
import transaction


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

    def __call__(self):
        if self.request.method == 'POST':
            data = self.request.form.get("exported-json", None)
            if data:
                self.context.json_data = data
                transaction.commit()

        return self.render()
