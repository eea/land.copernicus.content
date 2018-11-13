"""
  WIP fields clarification

===============================================================================
Field name              Field title                     site/@@register
-------------------------------------------------------------------------------
username                User Name                       YES
email                   E-mail                          YES
first_name              First Name                      YES
last_name               Last Name                       YES
fullname                ?
thematic_domain         Professional thematic domain    YES
institutional_domain    Institutional domain            YES
disclaimer_permission   I give permission to the        YES
                        Copernicus Land Monitoring
                        Service to contact me by e-mail
                        with the information about the
                        new products or product updates
                        and other important events in
                        the service or for my feedback
                        about the products of the
                        service and about this website.
captcha                 Verification                    YES
disclaimer              I accept privacy policy and     YES
                        terms of use of this website
address
description             x
fax                     x
from_city
from_country
home_page               x
institution
job_title               x
location                x
mail_me                 ?
mobile                  x
organisation
password                x
password_ctl            x
pdelete                 x
phone_numbers
portrait                x
position
postal_address          x
reason                  x
telephone               x
-------------------------------------------------------------------------------
"""
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.meeting.browser import views
from eea.meeting.events.rules import SendNewSubscriberEmailEvent
from functools import partial
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.contentprovider.interfaces import IContentProvider
from zope.event import notify
from zope.schema.interfaces import IVocabularyFactory
import plone.api as api
import socket
import transaction

simple_test = "TEST TODO"

FIELDS_REGISTRATION = (
    ('first_name', 'first_name'),
    ('last_name', 'last_name'),
    ('position', 'position'),
    ('organisation', 'institution'),
    ('address', 'address'),
    ('country', 'from_country'),
    ('email', 'email'),
    ('phone_numbers', 'phone_numbers'),
    ('username', None),
)


FIELDS_REQUIRED = (
    ('first_name', 'First name'),
    ('last_name', 'Last name'),
    ('position', 'Position'),
    ('organisation', 'Organisation'),
    ('address', 'Address'),
    ('country', 'Country'),
    ('username', 'Username'),
    ('email', 'Email'),
    ('pw1', 'Password'),
)


FIELDS_SIGNUP = (
    ('role', 'role'),
)


FIELDS_SIGNUP_REQUIRED = (
    ('role', 'Role'),
)


def create_user(request):
    member_data = {
        member_key: request.get(form_key)
        for form_key, member_key in FIELDS_REGISTRATION
        if member_key
    }

    member_data['fullname'] = '{} {}'.format(
        member_data['first_name'],
        member_data['last_name'],
    )

    return api.user.create(
        email=request.get('email'),
        username=request.get('username'),
        password=request.get('pw1'),
        properties=member_data,
    )


def login_user(response, user):
    acl = api.portal.get().acl_users
    acl.session._setupSession(user.getId(), response)


def err_reducer(acc, cur):
    return '\n'.join((acc, cur)) if type(cur) == str else acc


def check_pw(request):
    pw1, pw2 = request.get('pw1'), request.get('pw2')
    return pw1 == pw2 or 'Passwords do not match!'


def check_required(fields, request):
    missing_fields = [
        label for fname, label in fields
        if request.get(fname, None) in (None, '', [])
    ]

    if missing_fields:
        return (
            'These fields are required: {}!'
            .format(', '.join(missing_fields))
        )


def check_signup_other(request):
    field_role = request.get('role')
    field_role_other = request.get('role_other')
    if field_role == 'Other' and not field_role_other:
        return 'Please specify the role!'


VALIDATORS_REGISTER = (
    check_pw,
    partial(check_required, FIELDS_REQUIRED),
)


VALIDATORS_SIGNUP = (
    partial(check_required, FIELDS_SIGNUP_REQUIRED),
    check_signup_other
)


def register_error(request, template, msg):
    return template(
        register_message={'type': 'error', 'text': msg},
        fields={
            form_key: request.get(form_key)
            for form_key, _ in FIELDS_REGISTRATION
        }
    )


def signup_error(request, template, msg):
    return template(
        signup_message={'type': 'error', 'text': msg},
        fields={
            form_key: request.get(form_key)
            for form_key, _ in FIELDS_SIGNUP
        }
    )


class Register(views.Register):
    index = ViewPageTemplateFile('meeting_register.pt')

    def formatted_date(self, occ):
        provider = getMultiAdapter(
            (self.context, self.request, self),
            IContentProvider, name='formatted_date'
        )
        return provider(occ)

    def __call__(self):
        self.is_anon = api.user.is_anonymous()
        self.response = self.request.response

        if self.request.method == 'POST':
            if 'submit.login' in self.request:
                return self.login()
            elif 'submit.register' in self.request:
                return self.register()
            elif 'submit.signup' in self.request:
                return self.signup()

        if not self.is_anon:
            if self.request.get('login'):
                return self.index(
                    login_message={
                        'type': 'good',
                        'text': 'Login successful!'
                    }
                )
            elif self.request.get('created'):
                return self.index(
                    created_message={
                        'type': 'good',
                        'text': 'User account created!',
                    }
                )

        return self.index()

    def login(self):
        name = self.request.get('__ac_name')
        pwd = self.request.get('__ac_password')
        portal = api.portal.get()
        acl = portal.acl_users
        user = acl.authenticate(name, pwd, self.request)

        if user is not None:
            login_user(self.response, user)
            return self.response.redirect(
                self.context.absolute_url() + '/register?login=true')

        return self.index(
            login_message={'type': 'error', 'text': 'Invalid credentials!'}
        )

    def register(self):
        err_msg = partial(register_error, self.request, self.index)

        errors = reduce(err_reducer, (
            name(self.request)
            for name in VALIDATORS_REGISTER
        ), '')
        if errors:
            return err_msg(errors)

        try:
            login_user(self.response, create_user(self.request))
        except Exception as e:
            return err_msg(e.message)

        return self.response.redirect(
            self.context.absolute_url() + '/register?created=true')

    def signup(self):
        err_msg = partial(signup_error, self.request, self.index)

        errors = reduce(err_reducer, (
            name(self.request)
            for name in VALIDATORS_SIGNUP
        ), '')
        if errors:
            return err_msg(errors)

        try:
            subscribers = self.context.get('subscribers')
            self.validate(subscribers)

            user = api.user.get_current()
            uid = user.getId()

            props = dict(
                title=user.getProperty('fullname', uid),
                id=uid,
                userid=uid,
                email=user.getProperty('email', ''),
                role=self.request.get('role'),
                role_other=self.request.get('role_other', ''),
            )
            views.add_subscriber(subscribers, **props)
            notify(SendNewSubscriberEmailEvent(self.context))
        except socket.gaierror:
            # Make sure the transaction gets aborted.
            transaction.get().abort()
            return err_msg('Cannot send email!')
        except Exception as e:
            return err_msg(e.message or e)

        return self.response.redirect(
            self.context.absolute_url() + '/register')

    def role_options(self):
        vocab = getUtility(
            IVocabularyFactory,
            name='subscriber_roles'
        )(self.context)
        return tuple((term.token, term.title) for term in vocab)

    def prefill_form_data(self):
        user = api.user.get_current()
        uid = user.getId()

        return {
            'fields': {
                "first_name": user.getProperty('first_name', uid),
                "last_name": user.getProperty('last_name', uid),
                "organisation": user.getProperty('institution', uid),
                "position": user.getProperty('position', uid),
                "country": user.getProperty('from_country', uid),
                "address": user.getProperty('address', uid),
                "email": user.getProperty('email', uid),
                "phone_no": user.getProperty('phone_numbers', uid)
            }
        }
