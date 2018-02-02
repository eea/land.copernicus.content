import logging
from plone import api
from land.copernicus.content.content.api import LandFileApi
from land.copernicus.content.content.landfile import LandFileStore


logger = logging.getLogger('land.copernicus.content')


def do_migration(landitem, tree):
    landfiles = [lf for lf in tree.values()]
    landitem._landfiles = LandFileStore()
    store = landitem.landfiles
    for landfile in landfiles:
        store.add(landfile)

    api = LandFileApi(store)
    for landfile in landfiles:
        logger.info('Migrated: %s', api.get(landfile.title).title)


def run(_):
    catalog = api.portal.get_tool(name='portal_catalog')
    landitems = [b.getObject() for b in catalog(portal_type='LandItem')]
    for landitem in landitems:
        tree = landitem.landfiles

        if not isinstance(tree, LandFileStore):
            logger.info('Migrating: %s!', landitem.absolute_url(1))
            do_migration(landitem, tree)
            logger.info('Success: %s!', landitem.absolute_url(1))
