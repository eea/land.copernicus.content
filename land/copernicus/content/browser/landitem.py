from Products.Five.browser import BrowserView

import plone.api as api

from lxml.html import fragments_fromstring, tostring

from land.copernicus.content.config import IFRAME_HEIGHT
from land.copernicus.content.browser.download import _translate_size


class LandItemView(BrowserView):

    def embed_iframe(self):
        field = self.context.getField('embed')
        value = field.getAccessor(self.context)()
        if not value:
            return ""

        html = ''
        html_elements = fragments_fromstring(value)

        for tag in html_elements:
            if tag.tag == 'iframe':
                tag.set('height', IFRAME_HEIGHT)
                tag.set('class', 'widen')
                tag.set('data-role', 'iframe')
                tag.set('data-src', tag.get('src'))
                tag.set('src', '')
            html += tostring(tag)

        return html

    def has_iframe(self):
        field = self.context.getField('embed')
        value = field.getAccessor(self.context)()
        if not value:
            return False

        html_elements = fragments_fromstring(value)
        iframes = [iframe for iframe in html_elements
                   if iframe.tag == 'iframe']

        if iframes:
            return True

        return False

    def landfiles(self):
        return self.context.landfiles.values()

    @staticmethod
    def translate_size(landfile):
        return _translate_size(landfile.fileSize)

    def tab(self):
        return self.request.get('tab', 'mapview')

    def is_validated(self):
        field = self.context.getField('isValidatedDataset')
        return field.getAccessor(self.context)()

    def not_validated_text(self):
        field = self.context.getField('notValidatedCustomText')
        return field.getAccessor(self.context)()


class ProductInlineView(BrowserView):

    def get_countries_coverage(self):
        """ return countries for the geographical coverage
        """
        tool = api.portal.get_tool('portal_languages')
        countries = dict(tool.listAvailableCountries())
        return u', '.join([
            countries.get(t, t)
            for t in self.context.getGeographicCoverage()
        ])
