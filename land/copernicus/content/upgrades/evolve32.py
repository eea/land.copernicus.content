from plone import api
import logging
import transaction


logger = logging.getLogger('land.copernicus.content')


def do_migration(landitem):
    # TODO Save old field value in new one in geotags requested format
    # tool = api.portal.get_tool('portal_languages')
    # countries = dict(tool.listAvailableCountries())
    # if "test-landitem" in landitem.absolute_url():
    #     locations = [
    #         countries.get(t, t) for t in landitem.getGeographicCoverage()
    #     ]
    #
    #     import pdb; pdb.set_trace()
    #     locations = ['Bulgaria', 'Romania']
    #     # landitem.geographicCoverageGT = locations
    #     landitem.getField('geographicCoverageGT').set(landitem, locations)
    #     landitem.reindexObject()
    #     transaction.commit()

    print "WIP getGeographicCoverage -> getGeographicCoverageGT"


def run(_):
    catalog = api.portal.get_tool(name='portal_catalog')
    landitems = [b.getObject() for b in catalog(portal_type='LandItem')]
    for landitem in landitems:
        logger.info('Migrating: %s!', landitem.absolute_url(1))
        do_migration(landitem)
        logger.info('Success: %s!', landitem.absolute_url(1))
