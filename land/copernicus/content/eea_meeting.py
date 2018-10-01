from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
def subscriber_roles_vocabulary(context):
    items = [
        ('test1', u'Test value 1'),
        ('test2', u'Test value 2')
    ]

    terms = [
        SimpleTerm(value=pair[0], token=pair[0], title=pair[1])
        for pair in items
    ]
    return SimpleVocabulary(terms)
