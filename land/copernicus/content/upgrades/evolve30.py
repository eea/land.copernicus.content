import logging
from plone import api


logger = logging.getLogger('land.copernicus.content')


def run(_):
    portal = api.portal.get()
    catalog = portal.portal_catalog
    landitems = [b.getObject() for b in catalog(portal_type='LandItem')]
    for landitem in landitems:
        landfiles = [
            b.getObject()
            for b in landitem.getFolderContents(
                contentFilter=dict(portal_type='LandFile')
            )
        ]
        known_titles = []
        for landfile in landfiles:
            title = landfile.title_or_id()
            if title in known_titles:
                logger.error(
                    'Duplicate title: %s in %s',
                    title,
                    landitem.absolute_url(1)
                )
            known_titles.append(title)
    raise NotImplementedError
