from land.copernicus.content.browser.users_statistics import \
        users_statistics_operations_center
from land.copernicus.content.browser.subscribers_data_reset import \
        clean_old_subscribers_data
from land.copernicus.content.config import ENV_HOST_USERS_STATS
from land.copernicus.content.browser.users_email_notifications import \
        send_email_notifications

HOST = ENV_HOST_USERS_STATS

PLONE = "/copernicus"


def get_plone_site():
    import Zope2
    app = Zope2.app()
    from Testing.ZopeTestCase import utils
    utils._Z2HOST = HOST

    path = PLONE.split('/')

    app = utils.makerequest(app)
    app.REQUEST['PARENTS'] = [app]
    app.REQUEST.other['VirtualRootPhysicalPath'] = path
    from zope.globalrequest import setRequest
    setRequest(app.REQUEST)

    from AccessControl.SpecialUsers import system as user
    from AccessControl.SecurityManagement import newSecurityManager
    newSecurityManager(None, user)

    _site = app[path[-1]]
    site = _site.__of__(app)

    from zope.site.hooks import setSite
    setSite(site)

    return site


def users_stats():
    """ A cron callable script to take care of our users statistics reports
        bin/zeo_client run bin/users_stats
    """
    site = get_plone_site()
    users_statistics_operations_center(site)


def subscrib_reset():
    """ A cron callable script to reset subscribers data based on this request:

        E-pass information due to its sensitivity shall be treated very
        carefully - we would like to ask whether it would be possible to
        automate the deletion of this information, ie that E-pass information
        is deleted automatically 72hrs (3 days) after the end of the event

        bin/zeo_client run bin/subscrib_reset
    """
    site = get_plone_site()
    clean_old_subscribers_data(site)


def send_emails():
    """ A cron callable script to send user emails notifications

        bin/zeo_client run bin/send_emails
    """
    site = get_plone_site()
    send_email_notifications(site)
