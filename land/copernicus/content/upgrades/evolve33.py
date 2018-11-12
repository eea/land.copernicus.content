import logging
from plone import api
from land.copernicus.content.content.api import get_filesize


logger = logging.getLogger('land.copernicus.content')


def run(_):
    catalog = api.portal.get_tool(name='portal_catalog')
    land_items = [b.getObject() for b in catalog(portal_type='LandItem')]
    total_li = len(land_items)

    for idx_li, land_item in enumerate(land_items, start=1):
        url_land_item = land_item.absolute_url(1)
        logger.info('[%s/%s] Updating %s', idx_li, total_li, url_land_item)
        store = land_item.landfiles  # type: LandFileStore
        land_files = store.get_all()
        total_lf = len(land_files)

        for idx_lf, lf in enumerate(land_files, start=1):
            short_name = lf.shortname
            logger.info('[%s/%s] Updating %s', idx_lf, total_lf, short_name)
            new_file_size = ''
            try:
                new_file_size = get_filesize(lf.remoteUrl)
            except OSError:
                logger.warn('Missing path for land file: %s!', lf.remoteUrl)

            if new_file_size:
                logger.info(
                    'Updating file size for: %s: %s (%s) [%s]',
                    url_land_item, short_name, lf.remoteUrl, new_file_size)
                lf._fileSize = new_file_size
        logger.info('Done %s', url_land_item)
