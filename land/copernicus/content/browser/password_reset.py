from Products.Five.browser import BrowserView
import datetime


class ResetPasswordExpirationView(BrowserView):
    """ Return the expiration time as date and hours

        used in mail_password_template to replace:
            valid for x hours
        with:
            valid until <date and time>.
    """
    def __call__(self):
        hours = self.context.unrestrictedTraverse(
            "portal_password_reset").getExpirationTimeout()
        expiration = datetime.datetime.now() + datetime.timedelta(hours=hours)
        return expiration
