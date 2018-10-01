""" Unregister portal_transforms items defined by unused Ploneboard
"""
from Products.CMFCore.utils import getToolByName
from Products.MimetypesRegistry.common import MimeTypeException
from plone import api
import logging

logger = logging.getLogger('land.copernicus.content')


def unregister_transform(name):
    portal = api.portal.get()
    transforms = getToolByName(portal, 'portal_transforms')

    result = ""
    try:
        try:
            transforms.unregisterTransform(name)
        except MimeTypeException:
            if name in transforms.objectIds():
                transforms._delObject(name)
        result = ("Removed transform %s" % name)
    except AttributeError:
        result = ("Could not remove transform %s (not found)" % name)

    return result


def run(_):
    logger.info('Start cleaning portal_transforms...')
    broken_items = ['text_to_emoticons', 'url_to_hyperlink']
    for item in broken_items:
        result = unregister_transform(item)
        logger.info(result)
    logger.info('Done cleaning portal_transforms.')
