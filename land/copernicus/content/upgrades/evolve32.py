import logging
from plone import api


logger = logging.getLogger('land.copernicus.content')


def do_migration(landitem):
    print "WIP getGeographicCoverage -> getGeographicCoverageGT"


def run(_):
    catalog = api.portal.get_tool(name='portal_catalog')
    landitems = [b.getObject() for b in catalog(portal_type='LandItem')]
    for landitem in landitems:
        logger.info('Migrating: %s!', landitem.absolute_url(1))
        do_migration(landitem)
        logger.info('Success: %s!', landitem.absolute_url(1))
