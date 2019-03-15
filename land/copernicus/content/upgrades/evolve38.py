import logging
from plone import api
from land.copernicus.content.content.api import LandFileApi
from land.copernicus.content.content.landfile import LandFileStore


logger = logging.getLogger('land.copernicus.content')
KEY = "Country"


def replace(key, value, new_value):
    if key == KEY:
        return (key, new_value)
    return (key, value)


def do_migration(landitem):
    if KEY in landitem.fileCategories:
        landfiles = [x for x in landitem.landfiles.get_all()]
        lfa = LandFileApi(landitem.landfiles)

        for landfile in landfiles:
            categories = landfile.fileCategories
            country = dict(categories).get(KEY, "")

            # North Macedonia -------------------------------------------------
            new_country = "North Macedonia"
            if ("the former Yugoslavian Republic of Macedonia" in country) or (
                "Macedonia" in country) or ("FYROM" in country) or (
                    "Macedonia the former Yugoslavian Republic of" in country):

                res = [replace(x, y, new_country) for x, y in categories]
                # lfa.edit(
                #     landfile.title, title=landfile.title,
                #     description=landfile.description,
                #     remoteUrl=landfile.remoteUrl,
                #     fileCategories=tuple(res)
                # )

                new_c = dict(lfa.get(landfile.title).fileCategories).get(
                        "Country", "")

                if new_c == new_country:
                    logger.info(
                        "[OK] Migrated: {0} [{1}]: {2} -> {3}".format(
                            landitem.absolute_url(1),
                            landfile.title,
                            country,
                            new_c
                        )
                    )
                else:
                    logger.info(
                        "[??] Migrated: {0} [{1}]: {2} -> {3}".format(
                            landitem.absolute_url(1),
                            landfile.title,
                            country,
                            new_c
                        )
                    )

            # Czechia ---------------------------------------------------------
            new_country = "Czechia"

            if "Czech Republic" in country:

                res = [replace(x, y, new_country) for x, y in categories]
                # lfa.edit(
                #     landfile.title, title=landfile.title,
                #     description=landfile.description,
                #     remoteUrl=landfile.remoteUrl,
                #     fileCategories=tuple(res)
                # )

                new_c = dict(lfa.get(landfile.title).fileCategories).get(
                        "Country", "")

                if new_c == new_country:
                    logger.info(
                        "[OK] Migrated: {0} [{1}]: {2} -> {3}".format(
                            landitem.absolute_url(1),
                            landfile.title,
                            country,
                            new_c
                        )
                    )
                else:
                    logger.info(
                        "[??] Migrated: {0} [{1}]: {2} -> {3}".format(
                            landitem.absolute_url(1),
                            landfile.title,
                            country,
                            new_c
                        )
                    )


def run(_):
    catalog = api.portal.get_tool(name='portal_catalog')
    landitems = [b.getObject() for b in catalog(portal_type='LandItem')]
    for landitem in landitems:
        do_migration(landitem)
