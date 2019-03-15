import logging
from plone import api
from land.copernicus.content.content.api import LandFileApi
from land.copernicus.content.content.landfile import LandFileStore


logger = logging.getLogger('land.copernicus.content')


def do_migration(landitem):
    if "Country" in landitem.fileCategories:
        landfiles = [x for x in landitem.landfiles.get_all()]

        for landfile in landfiles:
            country = dict(landfile.fileCategories).get("Country", "")
            if "Macedonia" in country:
                logger.info(
                    "Migrated: {0} [{1}]: {2} -> {3}".format(
                        landitem.absolute_url(1),
                        landfile.title,
                        country,
                        "North Macedonia"
                    )
                )


def run(_):
    catalog = api.portal.get_tool(name='portal_catalog')
    landitems = [b.getObject() for b in catalog(portal_type='LandItem')]
    for landitem in landitems:
        do_migration(landitem)
