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
    html_logs = ""

    logger.info("Pages: {0}".format(len(pages)))
    html_logs += "<h2>Pages: {0}</h2>".format(len(pages))

    logger.info("START > pages > REPLACE: {0} WITH {1}".format(old, new))
    html_logs += "<p>START > pages > REPLACE: {0} WITH {1}</p>".format(
            old, new)

    for page in pages:
        body_text = page.EditableBody()
        url = page.absolute_url()
        if old in body_text:
            ok_replace = True
            for text in old_not:
                if text in body_text:
                    ok_replace = False

            if(ok_replace is True):
                prefix = "[Safe]"
            else:
                prefix = "[????]"
            logger.info("{0} [Body text] Found text ({1}) in: {2}".format(
                prefix, old, url))
            html_logs += """<p>{0} [Body text] Found text ({1}) in:
            <a href='{2}'>{2}</a></p>""".format(prefix, old, url)

        summary = page.Description()
        if old in summary:
            ok_replace = True
            for text in old_not:
                if text in summary:
                    ok_replace = False

            if(ok_replace is True):
                prefix = "[Safe]"
            else:
                prefix = "[????]"
            logger.info("{0} [Summary] Found text ({1}) in: {2}".format(
                prefix, old, url))
            html_logs += """<p> {0} [Summary] Found text ({1}) in:
            <a href='{2}'>{2}</a></p>""".format(prefix, old, url)

        page_title = page.Title()
        if old in page_title:
            ok_replace = True
            for text in old_not:
                if text in page_title:
                    ok_replace = False

            if(ok_replace is True):
                prefix = "[Safe]"
            else:
                prefix = "[????]"
            logger.info("{0} [Title] Found text ({1}) in: {2}".format(
                prefix, old, url))
            html_logs += """<p>{0} [Title] Found text ({1}) in:
            <a href='{2}'>{2}</a></p>""".format(prefix, old, url)

    return html_logs


class TextUpdateView(BrowserView):
    index = ViewPageTemplateFile("templates/text_update.pt")

    def render(self):
        return self.index()

    def do_operations(self):
        site = self.context.portal_url.getPortalObject()
        logs = ""

        for change in TEXTS:
            logs += replace_texts(
                site, change['old'], change['old_not'], change['new'])

        return logs

    def __call__(self):

        return self.render()
