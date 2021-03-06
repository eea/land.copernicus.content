from Products.CMFCore.interfaces import ISiteRoot
from collective.captcha.form.field import Captcha
from collective.captcha.form.widget import CaptchaWidget
from land.copernicus.content.config import EEAMessageFactory as _
from plone.app.controlpanel.widgets import MultiCheckBoxVocabularyWidget
from plone.app.users.browser.personalpreferences import UserDataPanel
from plone.app.users.browser.register import CantChoosePasswordWidget
from plone.app.users.browser.register import RegistrationForm
from plone.app.users.userdataschema import IUserDataSchema
from plone.app.users.userdataschema import IUserDataSchemaProvider
from zope import schema
from zope.browserpage import ViewPageTemplateFile
from zope.component import getUtility
from zope.formlib import form
from zope.formlib.boolwidgets import CheckBoxWidget
from zope.interface import Interface
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
import re


professional_thematic_domain_options = SimpleVocabulary([
    # Keep alphabetical order here.
    # Don't use "," in values. The "," is the separator. Replace with "_".
    SimpleTerm(value='Agriculture', title=_(u'Agriculture')),
    SimpleTerm(value='Architectural and Landscape Design',
               title=_(u'Architectural and Landscape Design')),
    SimpleTerm(value='Atmosphere', title=_(u'Atmosphere')),
    SimpleTerm(value='Climate Change', title=_(u'Climate Change')),
    SimpleTerm(value='Demography', title=_(u'Demography')),
    SimpleTerm(value='Ecology and Environment',
               title=_(u'Ecology and Environment')),
    SimpleTerm(value='Emergency Management', title=_(u'Emergency Management')),
    SimpleTerm(value='Energy_ Utilities and Industrial Infrastructure',
               title=_(u'Energy, Utilities and Industrial Infrastructure')),
    SimpleTerm(value='Forestry', title=_(u'Forestry')),
    SimpleTerm(value='Health', title=_(u'Health')),
    SimpleTerm(value='Hydrography', title=_(u'Hydrography')),
    SimpleTerm(value='Mapping', title=_(u'Mapping')),
    SimpleTerm(value='Security', title=_(u'Security')),
    SimpleTerm(value='Snow and Ice', title=_(u'Snow and Ice')),
    SimpleTerm(value='Soils and Geology', title=_(u'Soils and Geology')),
    SimpleTerm(value='Tourism and Recreation',
               title=_(u'Tourism and Recreation')),
    SimpleTerm(value='Transport and Routing',
               title=_(u'Transport and Routing')),
    SimpleTerm(value='Urban and Spatial Planning',
               title=_(u'Urban and Spatial Planning')),
])

institutional_domain_options = SimpleVocabulary([
    # Keep alphabetical order here.
    SimpleTerm(value='Citizen', title=_(u'Citizen')),
    SimpleTerm(value='Commercial', title=_(u'Commercial')),
    SimpleTerm(value='Education', title=_(u'Education')),
    SimpleTerm(value='NGO', title=_(u'NGO')),
    SimpleTerm(value='Public Authority', title=_(u'Public Authority')),
    SimpleTerm(value='Research and development',
               title=_(u'Research and development'))
])


def validateAccept(value):
    if value is not True:
        return False
    return True


def at_least_one_checked(value):
    if len(value) == 0:
        return False
    return True


def validate_phone(value):
    phone_re = re.compile(r'(\d{3})\D*(\d{3})\D*(\d{4})\D*(\d*)$', re.VERBOSE)
    if phone_re.match(value):
        return True
    return False


class DisclaimerWidget(CheckBoxWidget):
    """ Widget for accept terms of use in user registration """

    template = ViewPageTemplateFile('browser/templates/disclaimer-widget.pt')

    def __call__(self):
        val = super(DisclaimerWidget, self).__call__()
        self.val = val
        return self.template()


class DisclaimerPermissionWidget(CheckBoxWidget):
    """ Widget for permission to be contacted by email """

    template = ViewPageTemplateFile(
        'browser/templates/disclaimer-permission-widget.pt')

    def __call__(self):
        val = super(DisclaimerPermissionWidget, self).__call__()
        self.val = val
        return self.template()


class ICaptchaSchema(Interface):
    captcha = Captcha(
        title=_(u'Verification'),
        required=False
    )


class CopernicusRegistrationForm(RegistrationForm):

    @property
    def form_fields(self):
        if not self.showForm:
            # We do not want to spend time calculating fields that
            # will never get displayed.
            return []
        portal = getUtility(ISiteRoot)
        defaultFields = super(RegistrationForm, self).form_fields
        # Can the user actually set his/her own password?
        if portal.getProperty('validate_email', True):
            # No? Remove the password fields.
            defaultFields = defaultFields.omit('password', 'password_ctl')
            # Show a message indicating that a password reset link
            # will be mailed to the user.
            defaultFields['mail_me'].custom_widget = CantChoosePasswordWidget
            defaultFields['disclaimer'].custom_widget = DisclaimerWidget
        else:
            # The portal is not interested in validating emails, and
            # the user is not interested in getting an email with a
            # link to set his password if he can set this password in
            # the current form already.
            defaultFields = defaultFields.omit('mail_me')

        defaultFields = defaultFields.omit('fullname')

        thematic_domain = defaultFields['thematic_domain']
        thematic_domain.custom_widget = MultiCheckBoxVocabularyWidget

        institutional_domain = defaultFields['institutional_domain']
        institutional_domain.custom_widget = MultiCheckBoxVocabularyWidget

        disclaimer_permission = defaultFields['disclaimer_permission']
        disclaimer_permission.custom_widget = DisclaimerPermissionWidget

        # Add a captcha field to the schema
        defaultFields += form.Fields(ICaptchaSchema)
        defaultFields['captcha'].custom_widget = CaptchaWidget

        # Fix fields order
        defaultFields = defaultFields.select(
                'username', 'email', 'first_name', 'last_name',
                'thematic_domain', 'institutional_domain',
                'mail_me', 'disclaimer_permission', 'captcha', 'disclaimer')

        return defaultFields


class CustomizedUserDataPanel(UserDataPanel):
    def __init__(self, context, request):
        super(CustomizedUserDataPanel, self).__init__(context, request)

        self.form_fields = self.form_fields.omit(
            'email', 'first_name', 'last_name', 'description', 'disclaimer',
            'fax', 'fullname', 'home_page', 'job_title', 'location', 'mobile',
            'postal_address', 'portrait', 'pdelete', 'organisation',
            'reason', 'telephone')

        thematic_domain = self.form_fields['thematic_domain']
        thematic_domain.custom_widget = MultiCheckBoxVocabularyWidget

        institutional_domain = self.form_fields['institutional_domain']
        institutional_domain.custom_widget = MultiCheckBoxVocabularyWidget

        disclaimer_permission = self.form_fields['disclaimer_permission']
        disclaimer_permission.custom_widget = DisclaimerPermissionWidget

    def validate(self, action, data):
        # We omit email field in form, so we must prevent error:
        # Module plone.app.users.browser.personalpreferences, line 262,
        # in validate
        # Module zope.formlib.form, line 207, in getitem
        # KeyError: 'email'
        errors = super(UserDataPanel, self).validate(action, data)

        return errors

    def _on_save(self, data=None):
        """ Example:
            Login from a meeting view with a new account (that has not the
            complete profile). We want to redirect the user to meeting view
            after the profile is saved.

            Nothing happens if the came_from parameter is missing, so basic
            usage - when the user edits his Personal settings - remains the
            same.
        """
        next_url = self.request.SESSION.get("go_next", None)

        if next_url:
            self.request.response.redirect(next_url)
            self.request.SESSION.set("go_next", None)


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
    first_name = schema.TextLine(
        title=_(u'label_first_name', default=u'Name'),
        description=_(u'help_first_name',
                      default=u'Enter your first name.'),
        required=True,
    )

    last_name = schema.TextLine(
        title=_(u'label_last_name', default=u'Family name'),
        description=_(u'help_last_name',
                      default=u'Enter your last name.'),
        required=True,
    )

    thematic_domain = schema.List(
        title=_(u'label_thematic_domain',
                default=u'Professional thematic domain'),
        value_type=schema.Choice(
            vocabulary=professional_thematic_domain_options),
        required=True,
        constraint=at_least_one_checked
    )

    institutional_domain = schema.List(
        title=_(u'label_institutional_domain',
                default=u'Institutional domain'),
        value_type=schema.Choice(vocabulary=institutional_domain_options),
        required=True,
        constraint=at_least_one_checked
    )

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
                      "Your email will not be further distributed to third "
                      "parties. The registration is only used for reporting "
                      "purposes to the EP and Council."),
        required=True,
        constraint=validateAccept,
    )

    disclaimer_permission = schema.Bool(
        title=_(u'label_disclaimer_permission',
                default=u'I give permission'),
        description=_(
                u'help_disclaimer_permission',
                default=u""),
        required=True,
    )

    phone_numbers = schema.List(
        title=_(u'label_phone_numbers', default=u'Phone numbers'),
        description=_(u'help_phone_numbers',
                      default=u'Fill in phone numbers.'),
        value_type=schema.TextLine(),
        required=False
    )

    institution = schema.TextLine(
        title=_(u'label_institution', default=u'Institution'),
        description=_(u'help_institution',
                      default=u'Fill in the institution'),
        required=False,
    )

    position = schema.TextLine(
        title=_(u'label_position', default=u'Position'),
        description=_(
            u'help_position',
            default=u'Fill in your position within your Institution'),
        required=False,
    )

    from_country = schema.TextLine(
        title=_(u'label_from_country', default=u'From country'),
        description=_(u'help_from_country',
                      default=u'Fill in the From country'),
        required=False,
    )

    from_city = schema.TextLine(
        title=_(u'label_from_city', default=u'From city'),
        description=_(u'help_from_city',
                      default=u'Fill in the From city'),
        required=False,
    )

    address = schema.Text(
        title=_(u'label_address', default=u'Address'),
        description=_(u'help_address',
                      default=u'Fill in the address'),
        required=False,
    )
