from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from datetime import datetime
from datetime import timedelta
from plone import api
import pytz


EXPIRE_AFTER_HOURS = 72


def clean_old_subscribers_data(site):
    catalog = api.portal.get_tool(name='portal_catalog')
    meetings = [b.getObject() for b in catalog(portal_type='eea.meeting')]

    for meeting in meetings:
        if datetime.now(pytz.UTC) > meeting.end + timedelta(
                hours=EXPIRE_AFTER_HOURS):
            print "DELETED WIP TODO"
            print meeting
    return True


class SubscribersDataResetView(BrowserView):
    index = ViewPageTemplateFile("templates/subscribers_data_reset.pt")

    def render(self):
        return self.index()

    def __call__(self):
        site = self.context.portal_url.getPortalObject()

        clean_old_subscribers_data(site)

        return self.render()
