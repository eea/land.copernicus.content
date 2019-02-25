from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from persistent.dict import PersistentDict
from plone import api
from smtplib import SMTPRecipientsRefused
from zope.annotation import IAnnotations
import base64
import datetime
import logging
import time
import transaction


logger = logging.getLogger('land.copernicus.content')

DATE_UNTIL = DateTime(2018, 5, 1)  # Notify accounts created after this date
ANNOT_EMAILS_KEY = "land.copernicus.content.users_emails_notifications"


def get_emails_log():
    emails_annot = IAnnotations(api.portal.get()).setdefault(
        ANNOT_EMAILS_KEY, PersistentDict({}))
    transaction.commit()

    return emails_annot


def delete_emails_log():
    annotations = IAnnotations(api.portal.get())
    del annotations[ANNOT_EMAILS_KEY]


def add_to_emails_log(user_ids=[], timestamp=None):
    emails_log = get_emails_log()
    for user_id in user_ids:
        emails_log[user_id] = timestamp
    transaction.commit()


def user_already_notified(user_id):
    emails_log = get_emails_log()
    if emails_log.get(user_id, None) is not None:
        return True
    return False


def encode(key, clear):

    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc))


def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc)
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)


def get_secret_key(site):
    return getattr(site, 'users_email_notifications_secret_key', 'missing')


def send_email(site, user_id, email):
    encoded = encode(get_secret_key(site), user_id)
    link = """{0}/set_email_notifications?user_id={1}&key={2}""".format(
        site.absolute_url(), user_id, encoded)

    email_from_name = site.getProperty(
        'email_from_name', 'Copernicus Land Monitoring Service at the \
        European Environment Agency')
    email_from_address = site.getProperty(
        'email_from_address', 'copernicus@eea.europa.eu')
    mfrom = "{0} <{1}>".format(email_from_name, email_from_address)
    subject = u"Receive updates and information from the Copernicus \
Land Monitoring Service"
    mail_text = u"""
Hello,

We are writing to you because you are a registered user on the
https://land.copernicus.eu, the website of the Copernicus Land Monitoring
Service.

We would like to inform you that we have revised our privacy policy and terms
of use (https://land.copernicus.eu/terms-of-use).

If you wish to be informed by e-mail about new and updated products of the
Copernicus Land Monitoring Service, events and training opportunities please
confirm this in the provided link:

{0}

If you have any questions please contact us at copernicus@eea.europa.eu.

Kind regards,

Copernicus Land Monitoring Team""".format(link)

    try:
        mail_host = api.portal.get_tool(name='MailHost')
        return mail_host.simple_send(
            mto=email, mfrom=mfrom, subject=subject,
            body=mail_text, immediate=True)
    except SMTPRecipientsRefused:
        pass
        # raise SMTPRecipientsRefused('Recipient rejected by server')


def notify_next_users(site, x):
    md = getToolByName(site, 'portal_memberdata')

    _members = md._members
    _properties = site['acl_users']['mutable_properties']._storage

    notified = 0
    users = []
    for idx, user_id in enumerate(_members.iterkeys()):
        user_properties = _properties.get(user_id, dict())
        user_member_data = _members.get(user_id)

        if user_member_data is not None:
            active_last = user_properties.get('last_login_time')
            active_from = user_member_data.bobobase_modification_time()
            email = user_properties.get('email', None)

            if (
                    active_from < DATE_UNTIL) and (
                    user_already_notified(user_id) is False) and (
                    user_properties.get('disclaimer_permission') is False):
                logger.info("Found {0}: {1} - [{2} - {3}] - email: {4}".format(
                    idx, user_id, active_from, active_last, email))
                send_email(site, user_id, email)
                users.append(user_id)
                notified += 1
                time.sleep(1)

            if notified == x:
                break

    timestamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
    add_to_emails_log(users, timestamp)


def send_email_notifications(site):
    """ In: /manage_propertiesForm set
        users_email_notifications_enabled Boolean checked
        users_email_notifications_secret_key String value_here
        users_email_notifications_secret_users_unit Int value_here
    """
    is_enabled = getattr(site, 'users_email_notifications_enabled', False)
    users_unit = getattr(site, 'users_email_notifications_users_unit', 100)

    if is_enabled is True:
        logger.info('Sending emails... START.')
        # delete_emails_log()
        notify_next_users(site, users_unit)
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


class UsersEmailNotificationsLogView(BrowserView):
    index = ViewPageTemplateFile("templates/users_email_notifications_log.pt")

    def render(self):
        return self.index()

    def get_logs_data(self):
        return get_emails_log()

    def number_of_sent_emails(self):
        return len(get_emails_log().keys())

    def __call__(self):

        return self.render()


class SetEmailNotificationsView(BrowserView):
    index = ViewPageTemplateFile("templates/set_email_notifications.pt")

    def render(self):
        return self.index()

    def set_email_notifications(self, user_id, key):
        site = api.portal.get()
        if encode(get_secret_key(site), user_id) == key:
            user = api.user.get(userid=user_id)
            if user is not None:
                user.setMemberProperties(
                    mapping={'disclaimer_permission': True})

    def __call__(self):
        user_id = self.request.get('user_id', None)
        key = self.request.get('key', None)
        self.set_email_notifications(user_id, key)

        return self.render()
