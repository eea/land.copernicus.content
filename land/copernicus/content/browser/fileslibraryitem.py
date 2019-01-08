from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


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

    def __call__(self):
        if self.request.method == 'POST':
            import pdb; pdb.set_trace()

        return self.render()
