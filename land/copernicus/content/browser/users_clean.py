# from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
import logging


logger = logging.getLogger('land.copernicus.content')


def get_users_for_email(site, email):
    md = getToolByName(site, 'portal_memberdata')

    _members = md._members
    _properties = site['acl_users']['mutable_properties']._storage

    result = []
    for idx, user_id in enumerate(_members.iterkeys()):
        user_properties = _properties.get(user_id, dict())
        user_email = user_properties.get('email', '')

        if user_email == email:
            result.append(user_id)

    return result


def users_get_details(site, emails):
    html_logs = ""

    # md = getToolByName(site, 'portal_memberdata')

    # _members = md._members
    # _properties = site['acl_users']['mutable_properties']._storage
    # _never_active = DateTime("2010/01/01")

    users = []
    for email in emails:
        users += get_users_for_email(site, email)

        # user_id = "ghitab"
        # user_properties = _properties.get(user_id, dict())
        # user_member_data = _members.get(user_id)

        # import pdb; pdb.set_trace()
        #
        # if user_member_data is not None:
        #     active_last = user_properties.get('last_login_time')
        #     active_from = user_member_data.bobobase_modification_time()
        #
        # was_active = True
        # if active_last is not None and active_from is not None:
        #     if active_last < _never_active:
        #         # NEVER USED
        #         # A lot of accounts have 2000/01/01 as last login.
        #         # This means the account was created but never used.
        #         was_active = False

    for user_id in users:
        logger.info("{0}".format(user_id))
        html_logs += "<p>Details for {0}</p>".format(user_id)

    return html_logs


def users_clean(site, emails):
    html_logs = ""

    for email in emails:
        logger.info("{0}".format(emails))
        html_logs += "<p>{0}</p>".format(email)

    return html_logs


class UsersCleanView(BrowserView):
    index = ViewPageTemplateFile("templates/users_clean.pt")

    def render(self):
        return self.index()

    def do_operations(self, emails, get=False):
        site = self.context.portal_url.getPortalObject()

        if get is True:
            logs = users_get_details(site, emails)
            return logs

        logs = users_clean(site, emails)
        return logs

    @property
    def ajax_url_get(self):
        return api.portal.get(
                ).absolute_url() + '/users_clean?get_accounts=true'

    @property
    def ajax_url(self):
        return api.portal.get(
                ).absolute_url() + '/users_clean?do_operations=true'

    def __call__(self):
        """ /users_clean?get_accounts=true - AJAX usage
        """
        if 'get_accounts' in self.request.form:
            emails = self.request.get('emails', "").split("\n")
            return self.do_operations(emails, get=True)

        """ /users_clean?do_operations=true - AJAX usage
        """
        if 'do_operations' in self.request.form:
            emails = self.request.get('emails', "").split("\n")
            return self.do_operations(emails)

        """ /users_clean - the template that includes the AJAX call """
        return self.render()
