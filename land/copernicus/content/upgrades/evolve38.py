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
            if ("the former Yugoslavian Republic of Macedonia" in country) or (
                "Macedonia" in country) or ("FYROM" in country) or (
                    "Macedonia the former Yugoslavian Republic of" in country):
                logger.info(
                    "Migrated: {0} [{1}]: {2} -> {3}".format(
                        landitem.absolute_url(1),
                        landfile.title,
                        country,
                        "North Macedonia"
                    )
                )

            if "Czech Republic" in country:
                logger.info(
                    "Migrated: {0} [{1}]: {2} -> {3}".format(
                        landitem.absolute_url(1),
                        landfile.title,
                        country,
                        "Czechia"
                    )
                )


def run(_):
    catalog = api.portal.get_tool(name='portal_catalog')
    landitems = [b.getObject() for b in catalog(portal_type='LandItem')]
    for landitem in landitems:
        do_migration(landitem)
