from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from plone import api
import logging


logger = logging.getLogger('land.copernicus.content')


def delete_unused_accounts():
    logger.info("Deleted unused accounts. WIP")

    site = api.portal.get()

    md = getToolByName(site, 'portal_memberdata')

    _members = md._members
    _properties = site['acl_users']['mutable_properties']._storage
    _never_active = DateTime("2010/01/01")
    _new_accounts = DateTime("2019/01/01")

    deleted = 0
    for idx, user_id in enumerate(_members.iterkeys()):
        user_properties = _properties.get(user_id, dict())
        user_member_data = _members.get(user_id)

        if user_member_data is not None:
            active_last = user_properties.get('last_login_time')
            active_from = user_member_data.bobobase_modification_time()

            was_active = True
            is_new_account = True
            if active_last is not None and active_from is not None:
                if active_last < _never_active:
                    # NEVER USED
                    # A lot of accounts have 2000/01/01 as last login.
                    # This means the account was created but never used.
                    was_active = False

            if active_from < _new_accounts:
                is_new_account = False

            if was_active is False and is_new_account is False:
                deleted += 1
                logger.info("WIP Delete {0}: {1} - [{2} - {3}]".format(
                    idx, user_id, active_from, active_last))

    logger.info("Done. {0} deleted accounts.".format(deleted))


def run(_):
    delete_unused_accounts()
