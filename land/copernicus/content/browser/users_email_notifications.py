from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import logging

logger = logging.getLogger('land.copernicus.content')


def send_email_notifications(site):
    logger.info('Sending emails... START.')
    logger.info('Sending emails... STOP.')
    return True


class UsersEmailNotificationsView(BrowserView):
    index = ViewPageTemplateFile("templates/users_email_notifications.pt")

    def render(self):
        return self.index()

    def __call__(self):
        site = self.context.portal_url.getPortalObject()

        send_email_notifications(site)

        return self.render()
