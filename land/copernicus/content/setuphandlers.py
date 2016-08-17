from Products.CMFCore.utils import getToolByName
from Products.ATVocabularyManager.config import TOOL_NAME as ATVOCABULARYTOOL
from Products.ATVocabularyManager.utils.vocabs import createHierarchicalVocabs
from land.copernicus.content.content.vocabulary import COUNTRIES_DICTIONARY_ID
from land.copernicus.content.content.vocabulary import getCountriesDictionary
import logging


logger = logging.getLogger('land.copernicus.content: setuphandlers')


def installVocabularies(context):
    """ Creates/imports the atvm vocabs.
    """
    # only run this step if we are in eea.dataservice profile
    if context.readDataFile('land.copernicus.content.txt') is None:
        return

    site = context.getSite()
    atvm = getToolByName(site, ATVOCABULARYTOOL)

    # Create countries vocabulary
    if COUNTRIES_DICTIONARY_ID not in atvm.contentIds():
        hierarchicalVocab = {}
        hierarchicalVocab[(COUNTRIES_DICTIONARY_ID, 'European Countries')] = {}
        createHierarchicalVocabs(atvm, hierarchicalVocab)

        countries = getCountriesDictionary()
        for term in countries.keys():
            vocab = atvm[COUNTRIES_DICTIONARY_ID]
            vocab.invokeFactory('TreeVocabularyTerm', term[0], title=term[1])
            for subterm in countries[term].keys():
                subvocab = vocab[term[0]]
                subvocab.invokeFactory('TreeVocabularyTerm',
                                       subterm[0], title=subterm[1])
                subvocab.reindexObject()
            vocab.reindexObject()
    else:
        logger.warn('eea.dataservice countries vocabulary already exist.')
