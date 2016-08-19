from Products.ATVocabularyManager.config import TOOL_NAME as ATVOCABULARYTOOL
from Products.CMFCore.utils import getToolByName
from eea.cache import cache as eeacache
from land.copernicus.content.content.vocabulary import COUNTRIES_DICTIONARY_ID
from plone.i18n.locales.interfaces import ICountryAvailability
from zope.component import getUtility
import operator
import json

MEMCACHED_CACHE_SECONDS_KEY = 86400


@eeacache(lambda *args: MEMCACHED_CACHE_SECONDS_KEY)
def _country_terms(context):
    """ Cache the value of the countries dictionary
    """
    atvm = getToolByName(context, ATVOCABULARYTOOL)
    vocab = getattr(atvm, COUNTRIES_DICTIONARY_ID, None)
    return vocab.getVocabularyDict()


@eeacache(lambda * args: MEMCACHED_CACHE_SECONDS_KEY)
def _getCountryInfo(context):
    """ Country Info
    """
    res = {'groups': {}, 'countries': {}}
    terms = _country_terms(context)
    if not terms:
        return res

    util = getUtility(ICountryAvailability)
    countries = util.getCountries()

    for key in terms.keys():
        code = terms[key][0]
        if terms[key][1].keys():
            res['groups'][code] = code
        else:
            res['countries'][code] = _getCountryName(code, countries)
    return res


def _getCountryName(country_code, countries=None):
    """ Country Name
    """
    if countries is None:
        util = getUtility(ICountryAvailability)
        countries = util.getCountries()
    res = countries.get(country_code.lower(), {})
    res = res.get('name', country_code)
    return res


class GetCountryGroups(object):
    """ Country Groups
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        return _getCountryInfo(self.context)['groups']


class GetCountries(object):
    """ Countries
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        countries = _getCountryInfo(self.context)['countries']
        res = [(key, countries[key]) for key in countries.keys()]
        return sorted(res, key=operator.itemgetter(1))


class GetCountryGroupsData(object):
    """ Country Groups Data
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, group_id=''):
        res = {}
        terms = _country_terms(self)
        for key in terms.keys():
            if terms[key][1].keys():
                res[terms[key][0]] = []
                for c_key in terms[key][1].keys():
                    res[terms[key][0]].append(terms[key][1][c_key][0])
        return json.dumps(res)


class GetCountriesByGroup(object):
    """ Countries by group
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, group_id=''):
        res = []
        terms = _country_terms(self)
        for key in terms.keys():
            if terms[key][0] == group_id:
                for c_key in terms[key][1].keys():
                    res.append(terms[key][1][c_key][0])
                break
        return res
