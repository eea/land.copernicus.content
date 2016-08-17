COUNTRIES_DICTIONARY_ID = 'countries_dictionary'
COUNTRIES_DICTIONARY_ID = 'european_countries'

EFTA4 = {('ch', 'ch'): {},
         ('is', 'is'): {},
         ('li', 'li'): {},
         ('no', 'no'): {},
         }

EU15 = {('at', 'at'): {},
        ('be', 'be'): {},
        ('de', 'de'): {},
        ('dk', 'dk'): {},
        ('es', 'es'): {},
        ('fi', 'fi'): {},
        ('fr', 'fr'): {},
        ('gb', 'gb'): {},
        ('gr', 'gr'): {},
        ('ie', 'ie'): {},
        ('it', 'it'): {},
        ('lu', 'lu'): {},
        ('nl', 'nl'): {},
        ('pt', 'pt'): {},
        ('se', 'se'): {},
        }

EU25 = {('at', 'at'): {},
        ('be', 'be'): {},
        ('cy', 'cy'): {},
        ('cz', 'cz'): {},
        ('de', 'de'): {},
        ('dk', 'dk'): {},
        ('ee', 'ee'): {},
        ('es', 'es'): {},
        ('fi', 'fi'): {},
        ('fr', 'fr'): {},
        ('gb', 'gb'): {},
        ('gr', 'gr'): {},
        ('hu', 'hu'): {},
        ('ie', 'ie'): {},
        ('it', 'it'): {},
        ('lt', 'lt'): {},
        ('lu', 'lu'): {},
        ('lv', 'lv'): {},
        ('mt', 'mt'): {},
        ('nl', 'nl'): {},
        ('pl', 'pl'): {},
        ('pt', 'pt'): {},
        ('se', 'se'): {},
        ('si', 'si'): {},
        ('sk', 'sk'): {},
        }

EU27 = {('at', 'at'): {},
        ('be', 'be'): {},
        ('bg', 'bg'): {},
        ('cy', 'cy'): {},
        ('cz', 'cz'): {},
        ('de', 'de'): {},
        ('dk', 'dk'): {},
        ('ee', 'ee'): {},
        ('es', 'es'): {},
        ('fi', 'fi'): {},
        ('fr', 'fr'): {},
        ('gb', 'gb'): {},
        ('gr', 'gr'): {},
        ('hu', 'hu'): {},
        ('ie', 'ie'): {},
        ('it', 'it'): {},
        ('lt', 'lt'): {},
        ('lu', 'lu'): {},
        ('lv', 'lv'): {},
        ('mt', 'mt'): {},
        ('nl', 'nl'): {},
        ('pl', 'pl'): {},
        ('pt', 'pt'): {},
        ('ro', 'ro'): {},
        ('se', 'se'): {},
        ('si', 'si'): {},
        ('sk', 'sk'): {},
        }

EEA39 = {('al', 'al'): {},
         ('at', 'at'): {},
         ('be', 'be'): {},
         ('ba', 'ba'): {},
         ('bg', 'bg'): {},
         ('hr', 'hr'): {},
         ('cy', 'cy'): {},
         ('cz', 'cz'): {},
         ('dk', 'dk'): {},
         ('ee', 'ee'): {},
         ('xk', 'xk'): {},
         ('fi', 'fi'): {},
         ('fr', 'fr'): {},
         ('de', 'de'): {},
         ('gr', 'gr'): {},
         ('hu', 'hu'): {},
         ('is', 'is'): {},
         ('ie', 'ie'): {},
         ('it', 'it'): {},
         ('lv', 'lv'): {},
         ('li', 'li'): {},
         ('lt', 'lt'): {},
         ('lu', 'lu'): {},
         ('mk', 'mk'): {},
         ('mt', 'mt'): {},
         ('me', 'me'): {},
         ('nl', 'nl'): {},
         ('no', 'no'): {},
         ('pl', 'pl'): {},
         ('pt', 'pt'): {},
         ('ro', 'ro'): {},
         ('rs', 'rs'): {},
         ('sk', 'sk'): {},
         ('si', 'si'): {},
         ('es', 'es'): {},
         ('se', 'se'): {},
         ('ch', 'ch'): {},
         ('tr', 'tr'): {},
         ('gb', 'gb'): {},
         }


def getCountriesDictionary():
    """ Countries
    """
    res = {}

    # european countries
    data = getCountries()
    for key in data.keys():
        res[(key.lower(), data[key])] = {}

    # country groups
    res[('efta4', 'EFTA4')] = EFTA4
    res[('eu15', 'EU15')] = EU15
    res[('eu25', 'EU25')] = EU25
    res[('eu27', 'EU27')] = EU27
    res[('eea39', 'EEA39')] = EEA39
    return res


def getCountries():
    """ European countries """
    # In case we need all countries:
    # from Products.PloneLanguageTool.availablelanguages import getCountries
    # return getCountries()

    return {
        'ad': 'ad',
        'al': 'al',
        'am': 'am',
        'at': 'at',
        'az': 'az',
        'ba': 'ba',
        'be': 'be',
        'bg': 'bg',
        'by': 'by',
        'ch': 'ch',
        # 'cs':'cs', #Serbia and Montenegro, not used
        'cy': 'cy',
        'cz': 'cz',
        'de': 'de',
        'dk': 'dk',
        'ee': 'ee',
        'es': 'es',
        'fi': 'fi',
        # 'fo':'fo', #Faroe Islands, not used
        'fr': 'fr',
        'gb': 'gb',
        'ge': 'ge',
        'gr': 'gr',
        'hr': 'hr',
        'hu': 'hu',
        'ie': 'ie',
        # 'il':'il', #Israel, not used
        'is': 'is',
        'it': 'it',
        'kz': 'kz',
        'li': 'li',
        'lt': 'lt',
        'lu': 'lu',
        'lv': 'lv',
        'mc': 'mc',
        'md': 'md',
        'me': 'me',
        'mk': 'mk',
        'mt': 'mt',
        'nl': 'nl',
        'no': 'no',
        'pl': 'pl',
        'pt': 'pt',
        'ro': 'ro',
        'rs': 'rs',
        'ru': 'ru',
        'se': 'se',
        'si': 'si',
        'sk': 'sk',
        'sm': 'sm',
        'tr': 'tr',
        'ua': 'ua',
        'xk': 'xk',  # Kosovo https://countrycode.org/kosovo
    }
