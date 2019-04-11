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

    found = 0
    deleted = 0
    errors = 0
    to_be_deleted = []

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
                found += 1
                to_be_deleted.append(user_id)
                logger.info("To be deleted {0}: {1} - [{2} - {3}]".format(
                        found, user_id, active_from, active_last))

    for user_id in to_be_deleted:
        try:
            api.user.delete(username=user_id)
            deleted += 1
            logger.info("Delete {0}: {1}".format(deleted, user_id))
        except Exception:
            errors += 1
            logger.info("ERROR Delete {0}: {1}".format(errors, user_id))

    logger.info("Done. Found: {0} Deleted: {1} Errors: {2}.".format(
        found, deleted, errors))


def run(_):
    delete_unused_accounts()
