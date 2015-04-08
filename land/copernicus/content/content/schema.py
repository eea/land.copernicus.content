""" land.copernicus.content schema
"""

from Products.ATContentTypes.content.folder import ATFolder
from Products.ATVocabularyManager.namedvocabulary import NamedVocabulary
from Products.Archetypes import atapi
from Products.Archetypes.atapi import StringField
from Products.Archetypes.atapi import LinesField
from Products.Archetypes.atapi import MultiSelectionWidget
from Products.Archetypes.atapi import Schema
from Products.Archetypes.atapi import TextField
from Products.Archetypes.atapi import RichWidget
from eea.forms.browser.app.temporal_coverage import grouped_coverage
from land.copernicus.content.content.vocabulary import COUNTRIES_DICTIONARY_ID


SCHEMA = atapi.Schema(())

SECTION_SCHEMA = ATFolder.schema.copy() + SCHEMA.copy()
ITEM_SCHEMA = ATFolder.schema.copy() + SCHEMA.copy()


class TemporalMultiSelectionWidget(MultiSelectionWidget):
    """ derivative of MultiSelectionWidget in order to
        add a new formatting function
    """

    def formatted_value(self, value):
        """ Format value from temporal widget
        """
        try:
            return "\n".join(grouped_coverage(value))
        except ValueError:
            return "\n".join(value)


PRODUCT_SCHEMA = Schema((
    LinesField(
        name='geographicCoverage',
        languageIndependent=True,
        required=True,
        multiValued=1,
        default=[],
        vocabulary=NamedVocabulary(COUNTRIES_DICTIONARY_ID),
        schemata='metadata',
        widget=MultiSelectionWidget(
            macro="countries_widget",
            helper_js=("countries_widget.js",),
            helper_css=("countries_widget.css",),
            size=15,
            label="Geographical coverage",
            description=("The geographical extent of the content of "
                         "the data resource."),
            label_msgid='dataservice_label_geographic',
            description_msgid='dataservice_help_geographic',
            i18n_domain='eea',
        )
    ),
    LinesField(
        name='temporalCoverage',
        languageIndependent=True,
        schemata='metadata',
        required=False,
        multiValued=1,
        widget=TemporalMultiSelectionWidget(
            macro="temporal_widget",
            helper_js=("temporal_widget.js",),
            size=15,
            label="Temporal coverage",
            description=("The temporal scope of the content of the data "
                            "resource. Temporal coverage will typically "
                            "include a set of years or time ranges."),
            label_msgid='dataservice_label_coverage',
            description_msgid='dataservice_help_coverage',
            i18n_domain='eea',
        )
    ),
    TextField(
        name='geographicAccuracy',
        allowable_content_types=('text/plain', 'text/structured', 'text/html',
                                 'application/msword',),
        widget=RichWidget(
            label="Geographic Accuracy",
            description=("Information about how accurate is data."),
            label_msgid='eea_label_more_updates_on',
            i18n_domain='eea',
            ),
        default_content_type="text/html",
        searchable=True,
        schemata="metadata",
        default_output_type="text/x-html-safe",
    ),
    TextField(
        name='coordinateReferenceSystem',
        allowable_content_types=('text/plain', 'text/structured', 'text/html',
                                 'application/msword',),
        widget=RichWidget(
            label="Coordinate reference system",
            description="",
            label_msgid='eea_label_more_updates_on',
            i18n_domain='eea',
            ),
        default_content_type="text/html",
        searchable=True,
        schemata="metadata",
        default_output_type="text/x-html-safe",
    ),
    TextField(
        name='dataSources',
        allowable_content_types=('text/plain', 'text/structured', 'text/html',
                                 'application/msword',),
        widget=RichWidget(
            label="Data sources",
            description=("Where does the data come from?"),
            i18n_domain='eea',
        ),
        default_content_type="text/html",
        searchable=True,
        schemata="metadata",
        default_output_type="text/x-html-safe",
    ),
    TextField(
        name='owners',
        allowable_content_types=('text/plain', 'text/structured', 'text/html',
                                 'application/msword',),
        widget=RichWidget(
            label="Owners",
            description=("Who owns the data?"),
            i18n_domain='eea',
        ),
        default_content_type="text/html",
        searchable=True,
        schemata="metadata",
        default_output_type="text/x-html-safe",
    ),
    TextField(
        name='dataCustodians',
        allowable_content_types=('text/plain', 'text/structured', 'text/html',
                                 'application/msword',),
        widget=RichWidget(
            label="Data Custodians",
            description=("Who keeps the data up to date?"),
            i18n_domain='eea',
        ),
        default_content_type="text/html",
        searchable=True,
        schemata="metadata",
        default_output_type="text/x-html-safe",
    ),

))

PRODUCT_SCHEMA = ATFolder.schema.copy() + PRODUCT_SCHEMA

def finalize_product_schema(schema):

    for field in ['subject', 'rights']:
        schema.changeSchemataForField(field, 'metadata')

    # creators = ['creators']
    # if 'rights' in creators:
    #     i = creators.index('rights')
    #     del creators[i]
    #     fields['metadata'] = ['temporalCoverage', 'geographicCoverage',
    #                             'geographicAccuracy', 'Subject', 'rights',
    #                             'coordinateReferenceSystem', 'dataSources', 'owners',
    #                             'dataCustodians']
    # return fields

finalize_product_schema(PRODUCT_SCHEMA)

# These will be the entries to be filled out for the products:
# - Temporal coverage,
# - Latest upload
# - Geographic coverage
# - Geographic accuracy
# - Tags
# - Rights (mostly: full, open and free access in line with the Copernicus delegated regulation (EU) No 1159/2013 of 12 July 2013, supplementing Regulation (EU) No 911/2010 of the European Parliament and licensing conditions for GMES users and defining criteria for restricting access to GMES dedicated data and GMES service information)
# - Coordinate Reference System (always EPSG:3035 (ETRS89, LAEA) in our case)
# - Data sources
# - Owners (mostly European Union, EC DG Enterprise and Industry)
# - Data custodians (mostly: EEA)
#schema extender for rights
