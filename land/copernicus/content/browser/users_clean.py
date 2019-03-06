from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
import logging


logger = logging.getLogger('land.copernicus.content')


def users_clean(site, emails):
    html_logs = ""

    for email in emails:
        logger.info("{0}".format(emails))
        html_logs += "<p>{0}</p>".format(email)

    return html_logs


class UsersCleanView(BrowserView):
    index = ViewPageTemplateFile("templates/users_clean.pt")

    def render(self):
        return self.index()

    def do_operations(self, emails):
        site = self.context.portal_url.getPortalObject()

        logs = users_clean(site, emails)

        return logs

    @property
    def ajax_url(self):
        return api.portal.get(
                ).absolute_url() + '/users_clean?do_operations=true'

    def __call__(self):
        """ /users_clean?do_operations=true - AJAX usage
        """
        if 'do_operations' in self.request.form:
            emails = self.request.get('emails', "").split("\n")
            return self.do_operations(emails)

        """ /users_clean - the template that includes the AJAX call """
        return self.render()
