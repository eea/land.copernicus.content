from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
import logging


logger = logging.getLogger('land.copernicus.content')


def get_users_for_email(site, email):
    if email is None:
        return []
    elif len(email) < 2:
        return []

    md = getToolByName(site, 'portal_memberdata')

    _members = md._members
    _properties = site['acl_users']['mutable_properties']._storage

    result = []
    for idx, user_id in enumerate(_members.iterkeys()):
        user_properties = _properties.get(user_id, dict())
        user_email = user_properties.get('email', '')

        if user_email == email:
            result.append((user_id, email))

    return result


def delete_local_account(user_id, site):
    """ Delete the local website account for given user id
    """
    api.user.delete(username=user_id)
    logger.info('Deleted local account %s', user_id)


def users_get_or_delete(site, emails, delete=False):
    html_logs = ""

    md = getToolByName(site, 'portal_memberdata')

    _members = md._members
    _properties = site['acl_users']['mutable_properties']._storage
    _never_active = DateTime("2010/01/01")

    users = []
    for email in emails:
        users += get_users_for_email(site, email)

    for user in users:
        user_id = user[0]
        user_email = user[1]

        user_properties = _properties.get(user_id, dict())
        user_member_data = _members.get(user_id)

        if user_member_data is not None:
            active_last = user_properties.get('last_login_time')
            active_from = user_member_data.bobobase_modification_time()

        was_active = True
        if active_last is not None and active_from is not None:
            if active_last < _never_active:
                # NEVER USED
                # A lot of accounts have 2000/01/01 as last login.
                # This means the account was created but never used.
                was_active = False
            active_last_str = active_last.strftime("%Y/%m/%d")
            active_from_str = active_from.strftime("%Y/%m/%d")

        else:
            if active_last is None:
                active_last_str = "N/A"

            if active_from is None:
                active_from_str = "N/A"

        if was_active is True:
            status = "ACTIVE"
        else:
            status = "NEVER USED"

        if delete is True:
            if was_active is True:
                sufix = "NOT DELETED use Site Setup / Users to delete active \
                        accounts"
            else:
                delete_local_account(user_id, site)
                sufix = "DELETED"
        else:
            sufix = "NO CHANGES"

        logger.info("{0}".format(user_id))
        html_logs += """
            <p>
                <b>{0}</b> - {1} - {2} (Created: {3}, Last login: {4}) - {5}
            </p>""".format(
                user_id, user_email, status, active_from_str,
                active_last_str, sufix)

    return html_logs


class UsersCleanView(BrowserView):
    index = ViewPageTemplateFile("templates/users_clean.pt")

    def render(self):
        return self.index()

    def do_operations(self, emails, delete=False):
        site = self.context.portal_url.getPortalObject()

        logs = users_get_or_delete(site, emails, delete=delete)
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
            return self.do_operations(emails, delete=False)

        """ /users_clean?do_operations=true - AJAX usage
        """
        if 'do_operations' in self.request.form:
            emails = self.request.get('emails', "").split("\n")
            return self.do_operations(emails, delete=True)

        """ /users_clean - the template that includes the AJAX call """
        return self.render()
