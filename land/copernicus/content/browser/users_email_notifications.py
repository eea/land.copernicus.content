from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import logging
import base64

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


def send_email_notifications(site):
    logger.info('Sending emails... START.')
    test_clear = "ghitab"
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

    def set_email_notifications(self):

        print "Set notifications preferences."
        return True

    def __call__(self):
        self.set_email_notifications()

        return self.render()
