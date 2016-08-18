""" Config module
"""
from zope.i18nmessageid.message import MessageFactory
EEAMessageFactory = MessageFactory('eea')

product_globals = globals()


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
