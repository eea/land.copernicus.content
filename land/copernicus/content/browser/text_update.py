from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
import logging


logger = logging.getLogger('land.copernicus.content')

""" The list of texts to be updated. Usage:
{
    'old': "the text to be replaced",
    'old_not': ["don't update if this is found", "or this"],
    'new': "the new text"
},"""

TEXTS = [
    {
        'old': "Czech Republic",
        'old_not': [],
        'new': "Czechia"
    },
    {
        'old': "the former Yugoslavian Republic of Macedonia",
        'old_not': [],
        'new': "North Macedonia"
    },
    {
        'old': "Macedonia",
        'old_not': [
            'North Macedonia',
            'Republic of Macedonia',
            'Macedonia the former'
            ],
        'new': "North Macedonia"
    },
    {
        'old': "FYROM",
        'old_not': [],
        'new': "North Macedonia"
    },
    {
        'old': "Macedonia the former Yugoslavian Republic of",
        'old_not': [],
        'new': "North Macedonia"
    },
]


def find_pages():
    catalog = api.portal.get_tool(name='portal_catalog')
    pages = [b.getObject() for b in catalog(portal_type='Document')]

    return pages


def replace_texts(site, old, old_not, new):
    pages = find_pages()
    import pdb; pdb.set_trace()

    logger.info("Replaced {0} WITH {1} if NOT found: {2}".format(
        old, new, " OR ".join(old_not)))


class TextUpdateView(BrowserView):
    index = ViewPageTemplateFile("templates/text_update.pt")

    def render(self):
        return self.index()

    def __call__(self):
        site = self.context.portal_url.getPortalObject()
        for change in TEXTS:
            replace_texts(
                site, change['old'], change['old_not'], change['new'])

        return self.render()
