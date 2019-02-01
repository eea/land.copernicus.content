from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from persistent.dict import PersistentDict
from plone import api
from zope.annotation import IAnnotations
import base64
import datetime
import logging
import transaction

logger = logging.getLogger('land.copernicus.content')

SECRET_KEY_DEMO = "aaabbbccc"  # TODO Set a key as env var
ANNOT_EMAILS_KEY = "land.copernicus.content.users_emails_notifications"
# TODO
# select only users in given timeperiod
# select only users that have not the disclaimer already accepted
# add email template
# send emails
# what happens if an email fails?
# env vars
# enable / disable solution
# tests


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


def send_email(site, user_id, email):
    encoded = encode(SECRET_KEY_DEMO, user_id)
    link = """{0}/set_email_notifications?user_id={1}&key={2}""".format(
        site.absolute_url(), user_id, encoded)
    print "TODO send email " + user_id + " :: " + link


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

            if user_already_notified(user_id) is False:
                print "{0}: {1} - [{2} - {3}] - email: {4}".format(
                    idx, user_id, active_from, active_last, email)

                send_email(site, user_id, email)
                users.append(user_id)
                notified += 1

            if notified == x:
                break

    timestamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
    add_to_emails_log(users, timestamp)


def send_email_notifications(site):
    logger.info('Sending emails... START.')
    # delete_emails_log()
    notify_next_users(site, 5000)
    logger.info('Sending emails... STOP.')
    print get_emails_log()
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

    def __call__(self):

        return self.render()


class SetEmailNotificationsView(BrowserView):
    index = ViewPageTemplateFile("templates/set_email_notifications.pt")

    def render(self):
        return self.index()

    def set_email_notifications(self, user_id, key):
        print "Set notifications preferences."
        encoded = encode(SECRET_KEY_DEMO, user_id)
        if encoded == key:
            user = api.user.get(user_id)
            if user is not None:
                print "CURRENT STATE: "
                user.setMemberProperties({'disclaimer_permission': True})
                print user.disclaimer_permission
                msg = "GOOD"
            else:
                msg = "User not found."
        else:
            msg = "Invalid URL. User ID and key don't match."
        return msg

    def __call__(self):
        user_id = self.request.get('user_id', None)
        key = self.request.get('key', None)

        msg = self.set_email_notifications(user_id, key)
        print "ZZZZZ " + msg
        return self.render()
