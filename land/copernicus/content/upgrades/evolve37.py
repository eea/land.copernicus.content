from eea.rdfmarshaller.actions.pingcr import ping_CRSDS
from Products.CMFCore.utils import getToolByName
from plone import api
import logging


logger = logging.getLogger('land.copernicus.content')


def do_ping():
    site = api.portal.get()
    cat = getToolByName(site, 'portal_catalog')

    query = {
        'portal_type': ['File', 'Image', 'HelpCenterFAQFolder']
    }
    results = cat.searchResults(query)
    logger.info("Found %s objects " % len(results))
    count = 0
    options = {}
    options['create'] = False
    options['service_to_ping'] = 'http://semantic.eea.europa.eu/ping'
    for res in results:
        context = res.getObject()
        url = res.getURL()
        options['obj_url'] = url + '/@@rdf'

        logger.info("Pinging: %s", url)
        ping_CRSDS(context, options)
        logger.info("Finished pinging: %s", url)

        count += 1
        if count % 100 == 0:
            logger.info('Went through %s brains' % count)

    logger.info('Finished pinging all brains')


def run(_):
    logger.info(
        "Pinging objects belonging to the File/Image content type.")

    do_ping()
    logger.info('Success!')
