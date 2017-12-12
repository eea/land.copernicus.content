""" Custom overrides for eea.rdfmarshaller
"""

from eea.rdfmarshaller.archetypes.fields import ShortenHTMLField2Surf


class LandItemDescription(ShortenHTMLField2Surf):
    sentences = 1
    alternate_field = 'dataResourceAbstract'
