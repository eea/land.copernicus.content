from plone import api
import logging
import transaction


logger = logging.getLogger('land.copernicus.content')

COUNTRIES = [
    'Albania',
    'Austria',
    'Belgium',
    'Bosnia and Herzegovina',
    'Bulgaria',
    'Croatia',
    'Cyprus',
    'Czech Republic',
    'Denmark',
    'Estonia',
    'Finland',
    'France',
    'Germany',
    'Greece',
    'Hungary',
    'Iceland',
    'Ireland',
    'Italy',
    'Kosovo',
    'Latvia',
    'Liechtenstein',
    'Lithuania',
    'Luxembourg',
    'Macedonia the former Yugoslavian Republic of',
    'Malta',
    'Montenegro',
    'Netherlands',
    'Norway',
    'Poland',
    'Portugal',
    'Romania',
    'Serbia',
    'Slovakia',
    'Slovenia',
    'Spain',
    'Sweden',
    'Switzerland',
    'Turkey',
    'United Kingdom'
    ]

# TODO
# OK: make a list of existing locations
# manually generate json data for all locations, create a dict to be used later
# create a function: input locations, output json data
# update migration to set the json data for locations as value of GT field


def do_migration(landitem):
    tool = api.portal.get_tool('portal_languages')
    countries = dict(tool.listAvailableCountries())
    # all_locations = []
    #
    # locations = [
    #     countries.get(t, t) for t in landitem.getGeographicCoverage()
    # ]
    #
    # for location in locations:
    #     if location not in all_locations:
    #         all_locations.append(location)
    #         print location

    if "test-landitem" in landitem.absolute_url():
        anno = getattr(landitem, '__annotations__', {})
        print anno.get('eea.geotags.tags')

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
