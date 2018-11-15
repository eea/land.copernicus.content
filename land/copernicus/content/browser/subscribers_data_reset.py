from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from datetime import datetime
from datetime import timedelta
from plone import api
import logging
import pytz
import transaction

logger = logging.getLogger('land.copernicus.content')


EXPIRE_AFTER_HOURS = 72


def clean_old_subscribers_data(site):
    logger.info('Subscribers data reseting... START.')
    catalog = api.portal.get_tool(name='portal_catalog')
    meetings = [b.getObject() for b in catalog(portal_type='eea.meeting')]

    for meeting in meetings:
        if datetime.now(pytz.UTC) > meeting.end + timedelta(
                hours=EXPIRE_AFTER_HOURS):
            logger.info('Reseting data for %s', meeting.absolute_url())
            for subscriber in meeting.subscribers.get_subscribers():
                logger.info('Reseting data for %s', subscriber.absolute_url())
                subscriber.date_of_birth = None
                subscriber.nationality = None
                subscriber.id_card_nbr = None
                subscriber.id_valid_date = None
                subscriber.parking = None
                subscriber.car_id = None
                transaction.commit()
    logger.info('Subscribers data reseting... DONE.')
    return True


class SubscribersDataResetView(BrowserView):
    index = ViewPageTemplateFile("templates/subscribers_data_reset.pt")

    def render(self):
        return self.index()

    def __call__(self):
        site = self.context.portal_url.getPortalObject()

        clean_old_subscribers_data(site)

        return self.render()
