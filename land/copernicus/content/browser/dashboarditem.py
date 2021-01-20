from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class DashboardItemView(BrowserView):
    """ Dashboard Item view
    """
    index = ViewPageTemplateFile("templates/dashboarditem_view.pt")

    def render(self):
        return self.index()

    def __call__(self):
        return self.render()
