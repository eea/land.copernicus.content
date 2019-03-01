from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
import json
import logging


logger = logging.getLogger('land.copernicus.content')

""" The list of texts to be updated. Usage:
{
    'old': "the text to be replaced",
    'old_not': ["don't update if this is found", "or this"],
    'new': "the new text"
},

Example:

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
"""


def replace_texts(site, old, old_not, new):
    html_logs = ""
    catalog = api.portal.get_tool(name='portal_catalog')

    # --- PAGES ---------------------------------------------------------------
    items = [b.getObject() for b in catalog(portal_type='Document')]

    logger.info("Pages: {0}".format(len(items)))
    html_logs += "<h3>Pages: {0}</h3>".format(len(items))

    logger.info("START > pages > REPLACE: {0} WITH {1}".format(old, new))
    html_logs += "<p>START > pages > REPLACE: {0} WITH {1}</p>".format(
            old, new)

    for item in items:
        body_text = item.EditableBody()
        url = item.absolute_url()
        if old in body_text:
            ok_replace = True
            for text in old_not:
                if str(text) in body_text:
                    ok_replace = False

            if(ok_replace is True):
                prefix = "[Safe]"
            else:
                prefix = "[????]"
            logger.info("{0} [Body text] Found text ({1}) in: {2}".format(
                prefix, old, url))
            html_logs += """<p>{0} [Body text] Found text ({1}) in:
            <a href='{2}'>{2}</a></p>""".format(prefix, old, url)

        summary = item.Description()
        if old in summary:
            ok_replace = True
            for text in old_not:
                if str(text) in summary:
                    ok_replace = False

            if(ok_replace is True):
                prefix = "[Safe]"
            else:
                prefix = "[????]"
            logger.info("{0} [Summary] Found text ({1}) in: {2}".format(
                prefix, old, url))
            html_logs += """<p> {0} [Summary] Found text ({1}) in:
            <a href='{2}'>{2}</a></p>""".format(prefix, old, url)

        item_title = item.Title()
        if old in item_title:
            ok_replace = True
            for text in old_not:
                if str(text) in item_title:
                    ok_replace = False

            if(ok_replace is True):
                prefix = "[Safe]"
            else:
                prefix = "[????]"
            logger.info("{0} [Title] Found text ({1}) in: {2}".format(
                prefix, old, url))
            html_logs += """<p>{0} [Title] Found text ({1}) in:
            <a href='{2}'>{2}</a></p>""".format(prefix, old, url)

    # --- FOLDERS -------------------------------------------------------------
    items = [b.getObject() for b in catalog(portal_type='Folder')]

    logger.info("Folders: {0}".format(len(items)))
    html_logs += "<h3>Folders: {0}</h3>".format(len(items))

    logger.info("START > folders > REPLACE: {0} WITH {1}".format(old, new))
    html_logs += "<p>START > folders > REPLACE: {0} WITH {1}</p>".format(
            old, new)

    for item in items:
        summary = item.Description()
        if old in summary:
            ok_replace = True
            for text in old_not:
                if str(text) in summary:
                    ok_replace = False

            if(ok_replace is True):
                prefix = "[Safe]"
            else:
                prefix = "[????]"
            logger.info("{0} [Summary] Found text ({1}) in: {2}".format(
                prefix, old, url))
            html_logs += """<p> {0} [Summary] Found text ({1}) in:
            <a href='{2}'>{2}</a></p>""".format(prefix, old, url)

        item_title = item.Title()
        if old in item_title:
            ok_replace = True
            for text in old_not:
                if str(text) in item_title:
                    ok_replace = False

            if(ok_replace is True):
                prefix = "[Safe]"
            else:
                prefix = "[????]"
            logger.info("{0} [Title] Found text ({1}) in: {2}".format(
                prefix, old, url))
            html_logs += """<p>{0} [Title] Found text ({1}) in:
            <a href='{2}'>{2}</a></p>""".format(prefix, old, url)

    # --- NEWS ITEMS ----------------------------------------------------------
    items = [b.getObject() for b in catalog(portal_type='News Item')]

    logger.info("News Items: {0}".format(len(items)))
    html_logs += "<h3>News Items: {0}</h3>".format(len(items))

    logger.info("START > news > REPLACE: {0} WITH {1}".format(old, new))
    html_logs += "<p>START > news > REPLACE: {0} WITH {1}</p>".format(
            old, new)

    for item in items:
        body_text = item.EditableBody()
        url = item.absolute_url()
        if old in body_text:
            ok_replace = True
            for text in old_not:
                if str(text) in body_text:
                    ok_replace = False

            if(ok_replace is True):
                prefix = "[Safe]"
            else:
                prefix = "[????]"
            logger.info("{0} [Body text] Found text ({1}) in: {2}".format(
                prefix, old, url))
            html_logs += """<p>{0} [Body text] Found text ({1}) in:
            <a href='{2}'>{2}</a></p>""".format(prefix, old, url)

        summary = item.Description()
        if old in summary:
            ok_replace = True
            for text in old_not:
                if str(text) in summary:
                    ok_replace = False

            if(ok_replace is True):
                prefix = "[Safe]"
            else:
                prefix = "[????]"
            logger.info("{0} [Summary] Found text ({1}) in: {2}".format(
                prefix, old, url))
            html_logs += """<p> {0} [Summary] Found text ({1}) in:
            <a href='{2}'>{2}</a></p>""".format(prefix, old, url)

        item_title = item.Title()
        if old in item_title:
            ok_replace = True
            for text in old_not:
                if str(text) in item_title:
                    ok_replace = False

            if(ok_replace is True):
                prefix = "[Safe]"
            else:
                prefix = "[????]"
            logger.info("{0} [Title] Found text ({1}) in: {2}".format(
                prefix, old, url))
            html_logs += """<p>{0} [Title] Found text ({1}) in:
            <a href='{2}'>{2}</a></p>""".format(prefix, old, url)

    # --- EVENTS --------------------------------------------------------------
    items = [b.getObject() for b in catalog(portal_type='Event')]

    logger.info("Events: {0}".format(len(items)))
    html_logs += "<h3>Events: {0}</h3>".format(len(items))

    logger.info("START > events > REPLACE: {0} WITH {1}".format(old, new))
    html_logs += "<p>START > events > REPLACE: {0} WITH {1}</p>".format(
            old, new)

    for item in items:
        body_text = item.getField('text').getAccessor(item)()
        url = item.absolute_url()
        if old in body_text:
            ok_replace = True
            for text in old_not:
                if str(text) in body_text:
                    ok_replace = False

            if(ok_replace is True):
                prefix = "[Safe]"
            else:
                prefix = "[????]"
            logger.info("{0} [Body text] Found text ({1}) in: {2}".format(
                prefix, old, url))
            html_logs += """<p>{0} [Body text] Found text ({1}) in:
            <a href='{2}'>{2}</a></p>""".format(prefix, old, url)

        summary = item.Description()
        if old in summary:
            ok_replace = True
            for text in old_not:
                if str(text) in summary:
                    ok_replace = False

            if(ok_replace is True):
                prefix = "[Safe]"
            else:
                prefix = "[????]"
            logger.info("{0} [Summary] Found text ({1}) in: {2}".format(
                prefix, old, url))
            html_logs += """<p> {0} [Summary] Found text ({1}) in:
            <a href='{2}'>{2}</a></p>""".format(prefix, old, url)

        item_title = item.Title()
        if old in item_title:
            ok_replace = True
            for text in old_not:
                if str(text) in item_title:
                    ok_replace = False

            if(ok_replace is True):
                prefix = "[Safe]"
            else:
                prefix = "[????]"
            logger.info("{0} [Title] Found text ({1}) in: {2}".format(
                prefix, old, url))
            html_logs += """<p>{0} [Title] Found text ({1}) in:
            <a href='{2}'>{2}</a></p>""".format(prefix, old, url)

    # --- IMAGES --------------------------------------------------------------
    items = [b.getObject() for b in catalog(portal_type='Image')]

    logger.info("Images: {0}".format(len(items)))
    html_logs += "<h3>Images: {0}</h3>".format(len(items))

    logger.info("START > images > REPLACE: {0} WITH {1}".format(old, new))
    html_logs += "<p>START > images > REPLACE: {0} WITH {1}</p>".format(
            old, new)

    for item in items:
        summary = item.Description()
        if old in summary:
            ok_replace = True
            for text in old_not:
                if str(text) in summary:
                    ok_replace = False

            if(ok_replace is True):
                prefix = "[Safe]"
            else:
                prefix = "[????]"
            logger.info("{0} [Summary] Found text ({1}) in: {2}".format(
                prefix, old, url))
            html_logs += """<p> {0} [Summary] Found text ({1}) in:
            <a href='{2}'>{2}</a></p>""".format(prefix, old, url)

        item_title = item.getField('title').getAccessor(item)()
        if old in item_title:
            ok_replace = True
            for text in old_not:
                if str(text) in item_title:
                    ok_replace = False

            if(ok_replace is True):
                prefix = "[Safe]"
            else:
                prefix = "[????]"
            logger.info("{0} [Title] Found text ({1}) in: {2}".format(
                prefix, old, url))
            html_logs += """<p>{0} [Title] Found text ({1}) in:
            <a href='{2}'>{2}</a></p>""".format(prefix, old, url)

    # --- FILES ---------------------------------------------------------------
    items = [b.getObject() for b in catalog(portal_type='File')]

    logger.info("Files: {0}".format(len(items)))
    html_logs += "<h3>Files: {0}</h3>".format(len(items))

    logger.info("START > files > REPLACE: {0} WITH {1}".format(old, new))
    html_logs += "<p>START > files > REPLACE: {0} WITH {1}</p>".format(
            old, new)

    for item in items:
        summary = item.Description()
        if old in summary:
            ok_replace = True
            for text in old_not:
                if str(text) in summary:
                    ok_replace = False

            if(ok_replace is True):
                prefix = "[Safe]"
            else:
                prefix = "[????]"
            logger.info("{0} [Summary] Found text ({1}) in: {2}".format(
                prefix, old, url))
            html_logs += """<p> {0} [Summary] Found text ({1}) in:
            <a href='{2}'>{2}</a></p>""".format(prefix, old, url)

        item_title = item.getField('title').getAccessor(item)()
        if old in item_title:
            ok_replace = True
            for text in old_not:
                if str(text) in item_title:
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

    def do_operations(self, TEXTS):
        site = self.context.portal_url.getPortalObject()
        logs = ""

        for change in TEXTS:
            logs += "<h2>" + change['old'] + "</h2>"
            logs += replace_texts(
                site, str(change['old']), change['old_not'], change['new'])

        return logs

    @property
    def ajax_url(self):
        return api.portal.get(
                ).absolute_url() + '/text_update?do_operations=true'

    def __call__(self):
        """ /text_update?do_operations=true - AJAX usage

            TODO: (nice to have) unicode support, get rid of str(text)
        """
        if 'do_operations' in self.request.form:
            TEXTS = json.loads(self.request.get('TEXTS', []))
            return self.do_operations(TEXTS)

        """ /text_update - the template that includes the AJAX call """
        return self.render()
