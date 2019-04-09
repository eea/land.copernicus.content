# -*- coding: utf-8 -*-

import logging

from eea.rdfmarshaller.actions.pingcr import ping_CRSDS
from plone.api.portal import get_tool
from Products.Five.browser import BrowserView

logger = logging.getLogger('land.copernicus.content')


class ForcePingCRView(BrowserView):
    """ Force pingcr on objects between a set interval """

    def __call__(self):
        cat = get_tool('portal_catalog')

        query = {
            'review_state': 'published'
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
        return 'Finished'
