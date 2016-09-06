""" land.copernicus.content schema
"""
from AccessControl import ClassSecurityInfo
from DateTime import DateTime
from eea.forms.browser.app.temporal_coverage import grouped_coverage
from land.copernicus.content.content.vocabulary import COUNTRIES_DICTIONARY_ID
from Products.Archetypes import atapi
from Products.Archetypes.atapi import BooleanField
from Products.Archetypes.atapi import BooleanWidget
from Products.Archetypes.atapi import CalendarWidget
from Products.Archetypes.atapi import DateTimeField
from Products.Archetypes.atapi import LinesField
from Products.Archetypes.atapi import LinesWidget
from Products.Archetypes.atapi import MultiSelectionWidget
from Products.Archetypes.atapi import RichWidget
from Products.Archetypes.atapi import Schema
from Products.Archetypes.atapi import SelectionWidget
from Products.Archetypes.atapi import StringField
from Products.Archetypes.atapi import StringWidget
from Products.Archetypes.atapi import TextField
from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.link import ATLink
from Products.ATVocabularyManager.namedvocabulary import NamedVocabulary
from land.copernicus.content.widgets.geographic_bounding_box import (
    GeographicBoundingBoxWidget
)
from land.copernicus.content.fields.geographic_bounding_box import (
    GeographicBoundingBoxField
)

CONFORMITY_DEGREE_VOCAB = [
    (u'False', u'False'),
    (u'True', u'True'),
    (u'Null', u'Null'),
]

TOPIC_CATEGORY_VOCAB = [
    (u'Farming', u'Farming'),
    (u'Biota', u'Biota'),
    (u'Boundaries', u'Boundaries'),
    (u'Climatology/Meteorology/Atmosphere',
        u'Climatology/Meteorology/Atmosphere'),
    (u'Economy', u'Economy'),
    (u'Environment', u'Environment'),
    (u'Geoscientific Information', u'Geoscientific Information'),
    (u'Health', u'Health'),
    (u'Imagery/Base Maps/Earth Cover', u'Imagery/Base Maps/Earth Cover'),
    (u'Intelligence', u'Intelligence'),
    (u'Inland Water', u'Inland Water'),
    (u'Location', u'Location'),
    (u'Oceans', u'Oceans'),
    (u'Planning/Cadastre', u'Planning/Cadastre'),
    (u'Society', u'Society'),
    (u'Transportation', u'Transportation'),
    (u'Utilities/Communication', u'Utilities/Communication')
]


class TemporalLinesField(LinesField):
    """ derivative of linesfield for extending schemas """

    security = ClassSecurityInfo()

    security.declarePrivate('set')

    def set(self, instance, value, **kwargs):
        """ Expands year range input into a list of all elements
        """
        expanded_range = []

        for elem in value:
            if "-" in elem and elem != "-1":
                start, end = elem.split("-")
                expanded_range.extend(range(int(start), int(end) + 1))
            else:
                expanded_range.append(int(elem))

        save_value = [str(x) for x in set(expanded_range)]

        superclass = super(TemporalLinesField, self)
        superclass.set(instance, save_value, **kwargs)


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
    BooleanField(
        name='isValidatedDataset',
        schemata="default",
        widget=BooleanWidget(
            label=("Is Validated Dataset"),
            description=("Check this only if dataset is validated.")
        ),
    ),
    StringField(
        name='notValidatedCustomText',
        widget=StringWidget(
            label="Custom text for not validated",
            description=(
                "If this dataset is not validated you can set a "
                "custom label text here."),
            i18n_domain='eea',
        ),
        default="",
        searchable=False,
        schemata="default",
    ),
    LinesField(
        name='geographicCoverage',
        languageIndependent=True,
        required=False,
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
            description=("Countries that are covered by the resource"),
            label_msgid='dataservice_label_geographic',
            description_msgid='dataservice_help_geographic',
            i18n_domain='eea',
        )
    ),
    TemporalLinesField(
        name='temporalCoverage',
        languageIndependent=True,
        schemata='metadata',
        required=False,
        multiValued=1,
        widget=TemporalMultiSelectionWidget(
            macro="temporal_widget",
            helper_js=("temporal_widget.js",),
            size=15,
            label="Temporal Extent",
            description=(
                "The time period covered by the content of the resource"),
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
            label_msgid='eea_geographic_accuracy',
            i18n_domain='eea',
        ),
        default_content_type="text/html",
        searchable=True,
        schemata="metadata",
        default_output_type="text/x-html-safe",
    ),
    StringField(
        name='coordinateReferenceSystem',
        widget=StringWidget(
            label="Coordinate Reference System",
            description="CRS of the resource",
            i18n_domain='eea',
        ),
        default="EPSG:3035 (ETRS89, LAEA)",
        searchable=True,
        schemata="metadata",
    ),
    TextField(
        name='dataSources',
        allowable_content_types=('text/plain', 'text/structured', 'text/html',
                                 'application/msword',),
        widget=RichWidget(
            label="Data sources",
            description=(
                "A reference to a resource from which the present "
                "resource is derived. Details such exact body "
                "or department, date of delivery, original database, "
                "table or GIS layer, scientific literature ..."),
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
            label="Responsible organisation / Responsible party",
            description=(
                "Organisation associated with the resource. Organisation "
                "name, contact information (email)."),
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
    TextField(
        name='accessAndUseConstraints',
        allowable_content_types=('text/plain', 'text/structured', 'text/html',
                                 'application/msword',),
        widget=RichWidget(
            label="Constraints related to access and use "
            "/ Conditions applying to access and use",
            description=("Restriction on the access and use of a "
                         "resource or metadata"),
            i18n_domain='eea',
        ),
        default_content_type="text/html",
        searchable=True,
        schemata="metadata",
        default_output_type="text/x-html-safe",
    ),
    TextField(
        name='descriptionDetailedMetadata',
        allowable_content_types=('text/plain', 'text/structured', 'text/html',
                                 'application/msword',),
        widget=RichWidget(
            label="Description",
            description=("Description for Detailed metadata"),
            i18n_domain='eea',
        ),
        default_content_type="text/html",
        searchable=True,
        schemata="metadata",
        default_output_type="text/x-html-safe",
    ),
    DateTimeField(
        name='lastUpload',
        languageIndependent=True,
        required=False,
        default=DateTime(),
        schemata="metadata",
        imports="from DateTime import DateTime",
        widget=CalendarWidget(
            show_hm=False,
            label="Date of publication",
            description=("The date of the resource when available"),
            label_msgid='dataservice_label_last_upload',
            description_msgid='dataservice_help_last_upload',
            i18n_domain='eea',
        ),
    ),
    LinesField(
        name='fileCategories',
        languageIndependent=True,
        required=False,
        multiValued=1,
        default=[],
        schemata='metadata',
        widget=LinesWidget(
            size=15,
            label="Categories for Download Files",
            description=("One category per line."),
            i18n_domain='eea',
        )
    ),

    StringField(
        name='dataResourceTitle',
        widget=StringWidget(
            label="Data identification / Resource title",
            description="Name by which the cited resource is known",
            i18n_domain='eea',
        ),
        default="",
        searchable=True,
        schemata="metadata",
    ),
    TextField(
        name='dataResourceAbstract',
        allowable_content_types=('text/plain', 'text/structured', 'text/html',
                                 'application/msword',),
        widget=RichWidget(
            label="Data identification / Resource abstract",
            description=(
                "Brief narrative summary of the content of the "
                "resource(s) with coverage, main attributes, data sources, "
                "important of the work, etc."),
            label_msgid='eea_data_resource_abstract',
            i18n_domain='eea',
        ),
        default_content_type="text/html",
        searchable=True,
        schemata="metadata",
        default_output_type="text/x-html-safe",
    ),
    StringField(
        name='dataResourceType',
        widget=StringWidget(
            label="Data identification / Resource type",
            description="Scope to which metadata applies.",
            i18n_domain='eea',
        ),
        default="Dataset",
        searchable=True,
        schemata="metadata",
    ),
    StringField(
        name='dataResourceLocator',
        widget=StringWidget(
            label="Data identification / Resource Locator",
            description="URL address to locate the data",
            i18n_domain='eea',
        ),
        default="",
        searchable=True,
        schemata="metadata",
    ),
    LinesField(
        name='classificationTopicCategory',
        languageIndependent=True,
        required=False,
        multiValued=1,
        default=[],
        vocabulary=TOPIC_CATEGORY_VOCAB,
        schemata='metadata',
        widget=MultiSelectionWidget(
            size=17,
            label="Classification of spatial data / Topic of category",
            description=("Main theme(s) of the dataset"),
            label_msgid='topic_of_category',
            description_msgid='description_topic_of_category',
            i18n_domain='eea',
        )
    ),
    TextField(
        name='qualityLineage',
        allowable_content_types=('text/plain', 'text/structured', 'text/html',
                                 'application/msword',),
        widget=RichWidget(
            label="Quality and validity / Lineage",
            description=(
                "General explanation of the data produce knowledge's about "
                "the lineage of a dataset"),
            label_msgid='eea_quality_lineage',
            i18n_domain='eea',
        ),
        default_content_type="text/html",
        searchable=True,
        schemata="metadata",
        default_output_type="text/x-html-safe",
    ),
    TextField(
        name='qualitySpatialResolution',
        allowable_content_types=('text/plain', 'text/structured', 'text/html',
                                 'application/msword',),
        widget=RichWidget(
            label="Quality and validity / Spatial resolution",
            description=(
                "A set of zero to many resolution distances (typically for "
                "gridded data and imagery-derived products) or equivalent "
                "scales (typically for maps or map-derived products)"),
            label_msgid='eea_quality_spatial_resolution',
            i18n_domain='eea',
        ),
        default_content_type="text/html",
        searchable=True,
        schemata="metadata",
        default_output_type="text/x-html-safe",
    ),
    TextField(
        name='conformitySpecification',
        allowable_content_types=('text/plain', 'text/structured', 'text/html',
                                 'application/msword',),
        widget=RichWidget(
            label="Conformity / Specification",
            description=(
                "A citation of the implementing rules adopted under "
                "Article 7(1) of Directive 2007/2/EC or other specification "
                "to which a particular resource conforms"),
            label_msgid='eea_conformity_specification',
            i18n_domain='eea',
        ),
        default_content_type="text/html",
        searchable=True,
        schemata="metadata",
        default_output_type="text/x-html-safe",
    ),
    StringField(
        name='conformityDegree',
        vocabulary=CONFORMITY_DEGREE_VOCAB,
        widget=SelectionWidget(
            label="Conformity / Degree",
            description=(
                "The degree of conformant  with cited specification "
                "(true - if conformant, false - if not conformant, "
                "or null - if not evaluated)"),
            i18n_domain='eea',
        ),
        default="",
        searchable=False,
        schemata="default",
    ),
    TextField(
        name='accessAndUseLimitationPublic',
        allowable_content_types=('text/plain', 'text/structured', 'text/html',
                                 'application/msword',),
        widget=RichWidget(
            label="Constraints related to access and use / "
            "Limitation of public access",
            description=("Limitation and other reason for public access"),
            i18n_domain='eea',
        ),
        default_content_type="text/html",
        searchable=True,
        schemata="metadata",
        default_output_type="text/x-html-safe",
    ),
    TextField(
        name='responsiblePartyRole',
        allowable_content_types=('text/plain', 'text/structured', 'text/html',
                                 'application/msword',),
        widget=RichWidget(
            label="Responsible organisation / Responsible party role",
            description=("Function performed by the party"),
            i18n_domain='eea',
        ),
        default_content_type="text/html",
        searchable=True,
        schemata="metadata",
        default_output_type="text/x-html-safe",
    ),
    GeographicBoundingBoxField(
        name='geographicBoundingBox',
        languageIndependent=True,
        required=False,
        validators=('isGeographicBoundingBoxValid',),
        multiValued=1,
        default=[],
        schemata='metadata',
        widget=GeographicBoundingBoxWidget(
            label="Geographic reference / Bounding Box",
            description=("Coordinates of the four (West, East, North, South) "
                         "foremost corners of the dataset"),
            label_msgid='eea_geographic_bounding_box',
            i18n_domain='eea',
        )
    ),
))


def finalize_product_schema(schema):

    default_fields = ['id', 'title', 'description']
    meta_fields = [
        'subject', 'temporalCoverage', 'geographicCoverage',
        'geographicAccuracy', 'subject', 'rights', 'coordinateReferenceSystem',
        'dataSources', 'owners', 'dataCustodians', 'dataResourceTitle',
        'dataResourceAbstract', 'dataResourceType', 'dataResourceLocator',
        'classificationTopicCategory', 'qualityLineage',
        'qualitySpatialResolution', 'conformitySpecification',
        'conformityDegree', 'accessAndUseLimitationPublic',
        'responsiblePartyRole']

    for field in meta_fields:
        schema.changeSchemataForField(field, 'metadata')

    fields = default_fields + meta_fields
    for name in schema._names:
        if name not in fields:
            fields.append(name)
    schema._names = fields

SCHEMA = atapi.Schema(())

SECTION_SCHEMA = ATFolder.schema.copy() + SCHEMA.copy()
ITEM_SCHEMA = ATFolder.schema.copy() + SCHEMA.copy() + PRODUCT_SCHEMA

LANDFILE_SCHEMA = ATLink.schema.copy() + atapi.Schema((
    StringField(
        name='fileSize',
        widget=StringWidget(
            label="Download file size",
            description="Let this field empty. It is automatically extracted.",
            i18n_domain='eea',
        ),
        default="",
        searchable=False,
        schemata="default",
    ),
))


finalize_product_schema(ITEM_SCHEMA)
