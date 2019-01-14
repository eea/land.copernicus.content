from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
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
    index = ViewPageTemplateFile("templates/fileslibraryitem_edit.pt")

    def render(self):
        return self.index()

    @property
    def existing_files_in_context(self):
        return json.dumps(['existingfile1', 'existingfile2'])

    def __call__(self):
        if self.request.method == 'POST':
            data = self.request.form.get("exported-json", None)
            if data:
                self.context.json_data = data
                transaction.commit()

        return self.render()
