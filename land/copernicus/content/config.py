""" Config module
"""
from zope.i18nmessageid.message import MessageFactory
EEAMessageFactory = MessageFactory('eea')

product_globals = globals()

PACKAGE = 'land.copernicus.content'
ADD_PERMISSION = "land.copernicus.content: Add presentation"

IFRAME_WIDTH = "920"
IFRAME_HEIGHT = "450"
