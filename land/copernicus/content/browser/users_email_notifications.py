from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
import base64
import logging

logger = logging.getLogger('land.copernicus.content')


SECRET_KEY_DEMO = "aaabbbccc"  # TODO Set a key as env var


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


def get_users(site):
    md = getToolByName(site, 'portal_memberdata')

    _members = md._members
    _properties = site['acl_users']['mutable_properties']._storage

    for idx, user_id in enumerate(_members.iterkeys()):
        user_properties = _properties.get(user_id, dict())
        user_member_data = _members.get(user_id)

        if user_member_data is not None:
            active_last = user_properties.get('last_login_time')
            active_from = user_member_data.bobobase_modification_time()
            email = user_properties.get('email', None)
        print "{0}: {1} - active from: {2} to: {3} - email: {4}".format(
                idx, user_id, active_from, active_last, email)

    return True


def send_email_notifications(site):
    # TODO WIP
    aa = get_users(site)
    aa = aa
    logger.info('Sending emails... START.')
    test_clear = "ghitabzope"
    encoded = encode(SECRET_KEY_DEMO, test_clear)
    logger.info('Encoded: %s', encoded)
    decoded = decode(SECRET_KEY_DEMO, encoded)
    logger.info('Decoded: %s', decoded)
    link = """{0}/set_email_notifications?user_id={1}&key={2}""".format(
        site.absolute_url(), test_clear, encoded)
    logger.info('Link: %s', link)
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
