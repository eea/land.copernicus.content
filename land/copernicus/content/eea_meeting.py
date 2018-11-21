# -*- coding: utf-8 -*-
from eea.meeting import _
from eea.meeting.interfaces.util import validate_email
from eea.meeting.interfaces.util import validate_userid
from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobFile
from zope import schema
from zope.interface import Interface
from zope.interface import invariant, Invalid
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
import datetime


meeting_types = SimpleVocabulary(
    [
        SimpleTerm(value=u'conference', title=_(u'Conference')),
        SimpleTerm(value=u'meeting', title=_(u'Meeting')),
        SimpleTerm(value=u'workshop', title=_(u'Workshop')),
        SimpleTerm(value=u'webminar', title=_(u'Webminar')),
        SimpleTerm(value=u'eionet-copernicus-nrc-lc-meeting',
                   title=_(u'EIONET Copernicus NRC LC Meeting')),
        SimpleTerm(value=u'other', title=_(u'Other')),
    ]
)


class IMeeting(Interface):
    """ Meeting """
    text = RichText(
        title=_(u"Body text"),
        required=True,
    )

    meeting_type = schema.Choice(
        title=_(u"Meeting type"),
        vocabulary=meeting_types,
        required=True,
    )

    allow_register = schema.Bool(
        title=_(u"Allow users to register to the meeting"),
        required=True,
    )

    allow_register_start = schema.Datetime(
        title=_(u"From"),
        description=_(u"Allow registration starting with this datetime."),
        required=False,
    )

    allow_register_end = schema.Datetime(
        title=_(u"To"),
        description=_(u"Allow registration until this datetime."),
        required=False,
    )

    need_e_pass = schema.Bool(
        title=_(u"E-pass is required"),
        required=True,
    )

    restrict_content_access = schema.Bool(
        title=_(u"Hide meeting content list for not registered users"),
        required=True
    )

    auto_approve = schema.Bool(
        title=_(u"Automatically approve registrations"),
        required=True,
    )

    max_participants = schema.Int(
        title=_(u"Maximum number of subscribers"),
        required=True,
    )

    hosting_organisation = schema.TextLine(
        title=_(u"Supporting organisations"),
        required=True,
        default=None,
    )

    contact_name = schema.TextLine(
        title=_(u"Contact name"),
        required=True,
    )

    contact_email = schema.TextLine(
        title=_(u"Contact email"),
        required=True,
        constraint=validate_email
    )

    location = schema.TextLine(
        title=_(
            u'label_event_location',
            default=u'Event location'
        ),
        description=_(
            u'help_event_location',
            default=u'Location of the event.'
        ),
        required=False,
        default=None
    )

    agenda = NamedBlobFile(
        title=_(u"Event agenda"),
        description=_(u"Upload your agenda file."),
        required=False,
    )

    @invariant
    def validate_location_required(data):
        if data.meeting_type != 'webminar' and data.location is None:
            raise Invalid(_(
                u"Event location input is missing." +
                " This field is not required only in " +
                "'Meeting type: webminar' case."))


@provider(IVocabularyFactory)
def subscriber_roles_vocabulary(context):
    items = [
        ('Speaker', u'Speaker'),
        ('Participant', u'Participant')
    ]

    terms = [
        SimpleTerm(value=pair[0], token=pair[0], title=pair[1])
        for pair in items
    ]
    return SimpleVocabulary(terms)


class ISubscriber(Interface):
    """ Meeting subscriber """

    userid = schema.TextLine(
        title=_("User id"),
        required=True,
        constraint=validate_userid,
    )

    email = schema.TextLine(
        title=_(u"Email"),
        required=True,
        constraint=validate_email
    )

    # directives.widget(reimbursed=RadioFieldWidget)
    # reimbursed = schema.Bool(
    #     title=_(u"Reimbursed participation"),
    #     required=True
    # )

    role = schema.Choice(
        title=_(u"Role"),
        vocabulary="subscriber_roles",
        required=True,
    )

    role_other = schema.TextLine(
        title=_(u"Role (other)"),
        required=False,
    )

    date_of_birth = schema.Date(
        title=_(u"DATE OF BIRTH"),
        required=False,
        min=datetime.date(1900, 1, 1),
        max=datetime.date(2050, 1, 1),

    )

    nationality = schema.TextLine(
        title=_(u"NATIONALITY"),
        required=False,
    )

    id_card_nbr = schema.TextLine(
        title=_(u"ID CARD NBR"),
        required=False,
    )

    id_valid_date = schema.Date(
        title=_(u"ID VALID DATE"),
        required=False,
        min=datetime.date(1900, 1, 1),
        max=datetime.date(2050, 1, 1),
    )

    parking = schema.TextLine(
        title=_(u"PARKING"),
        required=False,
    )

    car_id = schema.TextLine(
        title=_(u"CAR ID"),
        required=False,
    )
