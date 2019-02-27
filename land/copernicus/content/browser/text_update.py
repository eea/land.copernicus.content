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
    logger.info("Pages: {0}".format(len(pages)))
    logger.info("START > pages > REPLACE: {0} WITH {1}".format(old, new))

    for page in pages:
        body_text = page.EditableBody()
        url = page.absolute_url()
        if old in body_text:
            logger.info("Found text ({0}) in: {1}".format(old, url))


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
