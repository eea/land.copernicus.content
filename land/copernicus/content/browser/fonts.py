from Products.Five.browser import BrowserView
from pkg_resources import resource_filename
import os


class ResourceResponseHeadersFixerView(BrowserView):
    """ With /resource_rhf?resource=FontAwesome.eot&params=oavxt5#iefix
        - get the resource font from
        /++resource++land.copernicus.theme/fonts/FontAwesome.eot?oavxt5#iefix
        - return it with fixed response headers:

            Get rid of Pragma cache
            Fix Cache-Control to be not no-cache

        instead of not working
            - Pragma: no-cache
            - Cache-Control: no-cache, max-age=0, must-revalidate

        in order to fix bug on IE [refs #95088]
    """
    def __call__(self):
        FONT_NAME = "FontAwesome"
        FONTS_PATH = "browser/theme/fonts/"

        if FONT_NAME not in self.request.QUERY_STRING:
            return None

        font = self.request.get('resource', None)

        if font is None:
            return None

        font_path = "{0}{1}".format(FONTS_PATH, font)

        font_file = resource_filename('land.copernicus.theme', font_path)

        if 'ttf' in font:
            content_type = "font/truetype"
        elif 'woff' in font:
            content_type = "font/woff2"
        elif 'eot' in font:
            content_type = "font/eot"
        elif 'svg' in font:
            content_type = "image/svg+xml"
        else:
            content_type = "font"

        RESPONSE = self.request.RESPONSE
        RESPONSE.setHeader('content-type', content_type)
        RESPONSE.setHeader('content-length', str(os.stat(font_file)[6]))
        RESPONSE.setHeader('Cache-Control', "max-age=3600, must-revalidate")

        with open(font_file, 'rb') as f:
            data = f.read()
            if data:
                RESPONSE.write(data)

        return
