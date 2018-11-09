from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


def clean_old_subscribers_data(site):
    print "DELETED WIP TODO"
    return True


class SubscribersDataResetView(BrowserView):
    index = ViewPageTemplateFile("templates/subscribers_data_reset.pt")

    def render(self):
        return self.index()

    def __call__(self):
        site = self.context.portal_url.getPortalObject()

        clean_old_subscribers_data(site)

        return self.render()
