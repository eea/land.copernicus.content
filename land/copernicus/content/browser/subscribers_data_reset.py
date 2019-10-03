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


def get_all_subscribers(site):
    """ Return the list of all meetings subscribers
    """
    all_subscribers = []
    catalog = api.portal.get_tool(name='portal_catalog')
    meetings = [b.getObject() for b in catalog(portal_type='eea.meeting')]

    for meeting in meetings:
        for subscriber in meeting.subscribers.get_subscribers():
            if subscriber not in all_subscribers:
                all_subscribers.append(subscriber)
    return all_subscribers


def delete_subscribers_for_account_with_id(user_id, site):
    """ Delete all subscribers items created using given account
    """
    logger.info('Searching subscribers items for %s', user_id)
    all_subscribers = get_all_subscribers(site)
    for subscriber in all_subscribers:
        if subscriber.userid == user_id:
            subscriber.aq_parent.manage_delObjects([subscriber.getId()])
            transaction.commit()
            logger.info('Deleted subscriber %s', user_id)


def delete_local_account(user_id, site):
    """ Delete the local website account for given user id
    """
    api.user.delete(username=user_id)
    logger.info('Deleted local account %s', user_id)


def remove_account_and_data(user_id, site):
    """ Remove data for given account
    """
    logger.info('Removing account and data for %s', user_id)
    delete_subscribers_for_account_with_id(user_id, site)
    delete_local_account(user_id, site)


def clean_old_subscribers_data(site):
    logger.info('Subscribers data reseting... START.')
    catalog = api.portal.get_tool(name='portal_catalog')
    meetings = [b.getObject() for b in catalog(portal_type='eea.meeting')]

    for meeting in meetings:
        if datetime.now(pytz.UTC) > meeting.end + timedelta(
                hours=EXPIRE_AFTER_HOURS):
            logger.info('Reseting data for %s', meeting.absolute_url())
            for subscriber in meeting.subscribers.get_subscribers():
                if subscriber.request_data_deletion is True:
                    remove_account_and_data(subscriber.userid, site)

                else:
                    logger.info(
                            'Reseting data for %s', subscriber.absolute_url())
                    subscriber.date_of_birth = None
                    subscriber.nationality = None
                    subscriber.id_card_nbr = None
                    subscriber.id_valid_date = None
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
