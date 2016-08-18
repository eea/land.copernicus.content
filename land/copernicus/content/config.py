""" Config module
"""
from zope.i18nmessageid.message import MessageFactory
EEAMessageFactory = MessageFactory('eea')

product_globals = globals()


# GENERAL package related settings ============================================

PACKAGE_NAME = "land.copernicus.content"
PACKAGE_DESCRIPTION = "Custom Content-Types for Land Copernicus"
PACKAGE_URL = "http://github.com/eea/land.copernicus.content"

PACKAGE_README_FILE = "README.txt"
PACKAGE_VERSION_FILE = "version.txt"
PACKAGE_HISTORY_FILE = "HISTORY.txt"
PACKAGE_DOCS_FOLDER = "docs"

PACKAGE_CLASSIFIERS = [
    "Programming Language :: Python",
]
PACKAGE_KEYWORDS = "land copernicus eea content-types plone zope"

PACKAGE_AUTHOR = "European Environment Agency"
PACKAGE_AUTHOR_EMAIL = "webadmin@eea.europa.eu"
PACKAGE_NAMESPACE_PACKAGES = ['land', 'land.copernicus']


# Security --------------------------------------------------------------------

ADD_PERMISSION = "land.copernicus.content: Add presentation"


# Layout ----------------------------------------------------------------------

IFRAME_WIDTH = "920"
IFRAME_HEIGHT = "450"

# Other consts here ===========================================================
