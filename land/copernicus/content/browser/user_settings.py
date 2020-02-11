from Products.Five.browser import BrowserView
import logging
import plone.api as api

logger = logging.getLogger('land.copernicus.content')


def is_EIONET_member(member):
    """ Check if a given member is EIONET user
    """
    site = api.portal.get()

    try:
        return "EIONET" in (
            site.acl_users.get("ldap-plugin")
            .acl_users.searchUsers(uid=member.getId())
            [0].get('dn', '')
        )

    except Exception:
        return False


class MySettingsView(BrowserView):
    """ Just a redirect to solve:
        * we want Password tab displayed by default
        * but an EIONET account doesn't have this tab
    """
    def __call__(self):
        user = api.user.get_current()
        is_EIONET = is_EIONET_member(user)
        if is_EIONET:
            tab = "@@personal-information"
        else:
            tab = "@@change-password"
        url = "{0}/{1}".format(api.portal.get().absolute_url(), tab)

        return self.request.response.redirect(url)
