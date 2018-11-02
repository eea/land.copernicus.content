from Products.CMFCore.utils import getToolByName
from plone import api
import logging


logger = logging.getLogger('land.copernicus.content')


def do_migration():
    site = api.portal.get()

    md = getToolByName(site, 'portal_memberdata')

    _members = md._members
    _properties = site['acl_users']['mutable_properties']._storage

    number_accounts = 0
    fixed_accounts = 0

    for idx, user_id in enumerate(_members.iterkeys()):
        user_properties = _properties.get(user_id, dict())
        # user_member_data = _members.get(user_id)

        old_data = user_properties.get("thematic_domain", "")

        if "Energy" in old_data:
            number_accounts += 1
            new_data = old_data.replace("Energy,", "Energy_")
            print "{0}: {1}".format(idx, user_id)

            try:
                user = api.user.get(user_id)
                user.setMemberProperties({'thematic_domain': new_data})
                fixed_accounts += 1
            except AttributeError:
                pass  # not a real account

    logger.info("Fixed {0} accounts from {1} found.".format(
        fixed_accounts, number_accounts))


def run(_):
    logger.info(
        "Fixing professional_thematic_domain: "
        "Energy, Utilities and Industrial Infrastructure")

    do_migration()
    logger.info('Success!')
