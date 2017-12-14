""" Config module
"""
import os
import logging

from zope.i18nmessageid.message import MessageFactory

EEAMessageFactory = MessageFactory('eea')

product_globals = globals()

PROJECTNAME = 'land.copernicus.content'
logger = logging.getLogger(PROJECTNAME)


# GENERAL package related settings ============================================

PACKAGE_NAME = "land.copernicus.content"
PACKAGE_DESCRIPTION = "Custom Content-Types for Land Copernicus"
PACKAGE_URL = "http://github.com/eea/land.copernicus.content"

# Security --------------------------------------------------------------------

ADD_PERMISSION = "land.copernicus.content: Add presentation"


# Layout ----------------------------------------------------------------------

IFRAME_WIDTH = "920"
IFRAME_HEIGHT = "450"

# Other consts here ===========================================================


def ENVPATH(name, default=None):
    """ GET path from os env
    """
    path = os.environ.get(name)
    if not path and default is None:
        raise EnvironmentError('{} needs to be defined!'.format(name))
    else:
        return path or default


ENV_DL_SRC_PATH = ENVPATH('LAND_DOWNLOADS_SRC_PATH')
ENV_DL_DST_PATH = ENVPATH('LAND_DOWNLOADS_DST_PATH')
ENV_DL_STATIC_PATH = ENVPATH('LAND_DOWNLOADS_STATIC_PATH', '/land-files/')

ENV_HOST_USERS_STATS = ENVPATH('LAND_HOST_USERS_STATS', 'land.copernicus.eu')
# Possible values: 'land.copernicus.eu', 'demo-copernicus.eea.europa.eu' or
# 'localhost:8090'
