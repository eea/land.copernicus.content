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
    print "Searching for user_id " + user_id
    all_subscribers = get_all_subscribers(site)
    for subscriber in all_subscribers:
        if subscriber.userid == user_id:
            subscriber.aq_parent.manage_delObjects([subscriber.getId()])
            transaction.commit()
            print "Deleting subscriber " + user_id


def delete_local_account(user_id, site):
    """ Delete the local website account for given user id
    """
    api.user.delete(username=user_id)
    print "Deleted account" + user_id


def remove_account_and_data(user_id, site):
    """ Remove data for given account
    """
    print "Removing account and data for " + user_id
    delete_subscribers_for_account_with_id(user_id, site)
    delete_local_account(user_id, site)


def clean_old_subscribers_data(site):
    logger.info('Subscribers data reseting... START.')
    catalog = api.portal.get_tool(name='portal_catalog')
    meetings = [b.getObject() for b in catalog(portal_type='eea.meeting')]

    remove_account_and_data("Test2019012902", site)

    for meeting in meetings:
        if datetime.now(pytz.UTC) > meeting.end + timedelta(
                hours=EXPIRE_AFTER_HOURS):
            logger.info('Reseting data for %s', meeting.absolute_url())
            for subscriber in meeting.subscribers.get_subscribers():
                # Check request_data_deletion field
                # if yes: delete all subscribers created by this account
                # and delete the account

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
