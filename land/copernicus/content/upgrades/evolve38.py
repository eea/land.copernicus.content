import logging
from plone import api
from land.copernicus.content.content.api import LandFileApi
from land.copernicus.content.content.landfile import LandFileStore


logger = logging.getLogger('land.copernicus.content')


def do_migration(landitem):
    logger.info('Migrated: %s', landitem.absolute_url(1))


def run(_):
    catalog = api.portal.get_tool(name='portal_catalog')
    landitems = [b.getObject() for b in catalog(portal_type='LandItem')]
    for landitem in landitems:
        do_migration(landitem)
        # tree = landitem.landfiles

        # if not isinstance(tree, LandFileStore):
