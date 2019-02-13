""" Custom overrides for eea.rdfmarshaller
"""

from zope.component import adapts
from zope.interface import implements

from eea.rdfmarshaller.archetypes.fields import ShortenHTMLField2Surf
from eea.rdfmarshaller.interfaces import ISurfResourceModifier, ISurfSession
from plone.app.blob.interfaces import IATBlob
from Products.ATContentTypes.interfaces.file import IATFile


import rdflib
import pytz


class LandItemDescription(ShortenHTMLField2Surf):
    sentences = 1
    alternate_field = 'dataResourceAbstract'


class IssuedFieldModifier(object):
    """Add publishing information to rdf export
    """
    implements(ISurfResourceModifier)
    adapts(IATFile)

    def __init__(self, context):
        self.context = context

    def run(self, resource, *args, **kwds):
        """Change the rdf resource to include issued term
        """
        if not hasattr(self.context, 'created'):
            return

        value = self.context.created().utcdatetime()

        timezone = pytz.timezone('UTC')
        utc_date = timezone.localize(value)
        value = rdflib.term.Literal(utc_date,
                                    datatype=rdflib.term.URIRef(u'http://www.w3.org/2001/XMLSchema#dateTime'
                                    ))
        setattr(resource, "dcterms_issued", value)
