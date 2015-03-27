from plone.app.users.userdataschema import IUserDataSchema
from plone.app.users.userdataschema import IUserDataSchemaProvider
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import implements
from land.copernicus.content.config import EEAMessageFactory as _


gender_options = SimpleVocabulary([
    SimpleTerm(value='Male', title=_(u'Male')),
    SimpleTerm(value='Female', title=_(u'Female')),
    ])

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
        title=u"Thematic domain of usage of the data",
        value_type=schema.Choice(vocabulary=thematic_domain_options))

    institutional_domain = schema.List(
        title=u"Institutional domain of usage of the data",
        value_type=schema.Choice(vocabulary=institutional_domain_options))

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
