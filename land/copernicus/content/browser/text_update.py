from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import logging


logger = logging.getLogger('land.copernicus.content')


def replace_texts(site, old, new):
    logger.info("Replaced {0} with {1}".format(old, new))


class TextUpdateView(BrowserView):
    index = ViewPageTemplateFile("templates/text_update.pt")

    def render(self):
        return self.index()

    def __call__(self):
        site = self.context.portal_url.getPortalObject()
        replace_texts(site, "demo", "demo")

        return self.render()
