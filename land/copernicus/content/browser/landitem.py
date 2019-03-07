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
        return self.context.landfiles.get_all()

    def has_landfiles(self):
        if len(self.landfiles()) > 0:
            return True
        return False

    def extra_class(self, tab):
        hidden_tab = "hide-me"

        if (tab == "download" and not self.has_landfiles()):
            return hidden_tab

        if (tab == "mapview" and not self.has_iframe()):
            return hidden_tab

        return ""

    @staticmethod
    def translate_size(landfile):
        return _translate_size(landfile.fileSize)

    def tab(self):
        if self.has_iframe() is True:
            return self.request.get('tab', 'mapview')

        if self.has_landfiles() is True:
            return self.request.get('tab', 'download')

        return self.request.get('tab', 'metadata')

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
        res = [
            countries.get(t, t)
            for t in self.context.getGeographicCoverage()]

        result = []
        for x in res:
            t = x
            if (t == "Czech Republic") or ("Czech R" in t):
                t = u"Czechia"
            if (t == "Macedonia the former Yugoslavian Republic of") or \
                    ("Macedonia" in t) or ("FYROM" in t):
                t = u"North Macedonia"
            result.append(t)

        return u', '.join(result)

    def get_geotags(self):
        """ Return geotags
        """
        field = self.context.getField('geographicCoverageGT')
        value = field.getAccessor(self.context)()
        return u", ".join(x.decode('utf-8') for x in value)
