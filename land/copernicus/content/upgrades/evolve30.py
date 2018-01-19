from functools import partial
import logging
from plone import api
from land.copernicus.content.content.api import LandFileApi


logger = logging.getLogger('land.copernicus.content')


MSG_CHANGED_TITLE = u'Changed title: %s -> %s. %s'
MSG_CHANGED_SHORTNAME = u'Changed ID: %s -> %s. %s'


def extract_props(landfile):
    # Only way to get the true value of the description field.
    # getAccessor()() converts the value to ASCII.
    description = landfile._md['description'].raw  # NOQA

    return dict(
        title=landfile.title,
        shortname=landfile.id,
        description=description,
        remoteUrl=landfile.remoteUrl,
        _fileSize=landfile.fileSize,
        fileCategories=tuple(
            (cat['name'], cat['value'])
            for cat in landfile.fileCategories
            if cat['value']
        )
    )


def _join_categories(categories):
    return u' '.join(u'(%s)' % val for _, val in categories)


def add_with_fallback(lfa, props):
    """ If the title exists, create a new title
        by appending the file categories.
    """
    if lfa.get(props['title']):
        props['title'] = u'{} {}'.format(
            props['title'],
            _join_categories(props['fileCategories'])
        )
    return lfa.add(**props)


def _log_prop_change(msg, old_prop, new_prop, url):
    if new_prop != old_prop:
        logger.warn(msg, old_prop, new_prop, url)


log_title_change = partial(_log_prop_change, MSG_CHANGED_TITLE)
log_shortname_change = partial(_log_prop_change, MSG_CHANGED_SHORTNAME)


def run(_):
    catalog = api.portal.get_tool(name='portal_catalog')
    landitems = [b.getObject() for b in catalog(portal_type='LandItem')]
    for landitem in landitems:
        # only interested in published content
        query = dict(portal_type='LandFile', review_state='published')
        brains = landitem.getFolderContents(contentFilter=query)
        landfiles = [b.getObject() for b in brains]

        if landfiles:
            lfa = LandFileApi(landitem.landfiles)

            # migrate each landfile
            for landfile in landfiles:
                # avoid acquisition
                url = landfile.absolute_url(1)
                obj = landfile.aq_inner.aq_self

                props = extract_props(obj)
                new_landfile = add_with_fallback(lfa, props)
                log_title_change(obj.title, new_landfile.title, url)
                log_shortname_change(obj.id, new_landfile.shortname, url)

            # stats
            len_orig = len(landfiles)
            len_added = len(landitem.landfiles)

            # delete migrated LandFiles
            api.content.delete(objects=landfiles)

            logger.info('Done %s -> %s!', len_orig, len_added)
