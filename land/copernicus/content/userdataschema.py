from plone.app.users.userdataschema import IUserDataSchema
from plone.app.users.userdataschema import IUserDataSchemaProvider
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import implements
from land.copernicus.content.config import EEAMessageFactory as _
import re

thematic_domain_options = SimpleVocabulary([
    SimpleTerm(value='Environment', title=_(u'Environment')),
    SimpleTerm(value='Agriculture', title=_(u'Agriculture')),
    SimpleTerm(value='Demography', title=_(u'Demography')),
    SimpleTerm(value='Energy', title=_(u'Energy')),
    SimpleTerm(value='Education', title=_(u'Education')),
    SimpleTerm(value='Forestry', title=_(u'Forestry')),
    SimpleTerm(value='Health', title=_(u'Health')),
    SimpleTerm(value='Physical Planning', title=_(u'Physical Planning')),
    SimpleTerm(value='Research', title=_(u'Research')),
    SimpleTerm(value='Tourism', title=_(u'Tourism')),
    SimpleTerm(value='Transport', title=_(u'Transport'))
    ])

institutional_domain_options = SimpleVocabulary([
    SimpleTerm(value='Commercial', title=_(u'Commercial')),
    SimpleTerm(value='Public Authority', title=_(u'Public Authority')),
    SimpleTerm(value='Citizen', title=_(u'Citizen'))
    ])


def validateAccept(value):
    if not value == True:
        return False
    return True


def validate_phone(value):
    phone_re = re.compile(r'(\d{3})\D*(\d{3})\D*(\d{4})\D*(\d*)$', re.VERBOSE)
    if phone_re.match(value):
        return True
    return False


class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        """
        """
        return IEnhancedUserDataSchema


class IEnhancedUserDataSchema(IUserDataSchema):
    """ Use all the fields from the default user data schema, and add various
    extra fields.
    """
    thematic_domain = schema.List(
        title=_(u'label_thematic_domain',
                default=u'Thematic domain of usage of the data'),
        value_type=schema.Choice(vocabulary=thematic_domain_options))

    institutional_domain = schema.List(
        title=_(u'label_institutional_domain',
                default=u'Institutional domain of usage of the data'),
        value_type=schema.Choice(vocabulary=institutional_domain_options))

    reason = schema.TextLine(
        title=_(u'label_reason', default=u'Reason to create the account'),
        description=_(u'help_reason',
                      default=u'Fill in the reason for account creation'),
        required=False,
        )

    job_title = schema.TextLine(
        title=_(u'label_job_title', default=u'Job title'),
        description=_(u'help_job_title',
                      default=u'Fill in the job title'),
        required=False,
        )

    postal_address = schema.Text(
        title=_(u'label_postal_address', default=u'Postal address'),
        description=_(u'help_postal_address',
                      default=u'Fill in the postal address'),
        required=False,
        )

    telephone = schema.ASCIILine(
        title=_(u'label_telephone', default=u'Telephone number'),
        description=_(u'help_telephone',
                      default=u'Fill in the telephone number'),
        required=False,
        constraint=validate_phone
        )

    mobile = schema.ASCIILine(
        title=_(u'label_mobile', default=u'Mobile telephone number'),
        description=_(u'help_mobile',
                      default=u'Fill in the mobile telephone number'),
        required=False,
        constraint=validate_phone
        )

    fax = schema.ASCIILine(
        title=_(u'label_fax', default=u'Fax number'),
        description=_(u'help_fax',
                      default=u'Fill in the fax number'),
        required=False,
        constraint=validate_phone
        )

    organisation = schema.TextLine(
        title=_(u'label_organisation', default=u'Organisation'),
        description=_(u'help_organisation',
                      default=u'Fill in the organisation'),
        required=False,
        )

    disclaimer = schema.Bool(
        title=_(u'label_disclaimer', default=u'Accept terms of use'),
        description=_(u'help_disclaimer',
                      default=u"Tick this box to indicate that you have found,"
                      " read and accepted the terms of use for this site. "
                      "Your email will not be further distributed to third parties. "
                      "The registration is only used for reporting purposes to "
                      "the EP and Council."),
        required=True,
        constraint=validateAccept,
        )
