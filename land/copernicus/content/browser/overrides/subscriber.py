# -*- coding: utf-8 -*-
from land.copernicus.content.config import EEAMessageFactory as _
from plone import api
from plone.dexterity.browser import edit
from plone.dexterity.interfaces import IDexterityEditForm
from plone.z3cform import layout
from zope.interface import classImplements
from plone.z3cform.fieldsets.extensible import FormExtender
from Products.Five.browser import BrowserView
from z3c.form.field import Fields
from z3c.form import util
from zope import schema


class SubscriberView(BrowserView):
    """ Override subscriber view to have member related fields
    """


class EditFormExtender(FormExtender):
    def update(self):
        if self.request.REQUEST_METHOD == 'GET':
            # add fields
            subscriber = self.context
            details = subscriber.get_details()
            phones = details.get("phone_numbers", "").split(", ")

            first_name = schema.TextLine(
                __name__="first_name",
                title=_(u'label_first_name', default=u'Name'),
                description=_(u'help_first_name',
                              default=u'Enter your first name.'),
                required=False,
                default=util.toUnicode(details.get("first_name", ""))
            )

            last_name = schema.TextLine(
                __name__="last_name",
                title=_(u'label_last_name', default=u'Surname'),
                description=_(u'help_last_name',
                              default=u'Enter your last name (family name).'),
                required=False,
                default=util.toUnicode(details.get("last_name", ""))
            )

            phone_numbers = schema.List(
                __name__="phone_numbers",
                title=_(u'label_phone_numbers', default=u'Phone numbers'),
                description=_(u'help_phone_numbers',
                              default=u'Fill in phone numbers.'),
                value_type=schema.TextLine(),
                required=False,
                default=phones
            )

            institution = schema.TextLine(
                __name__="institution",
                title=_(u'label_institution', default=u'Institution'),
                description=_(u'help_institution',
                              default=u'Fill in the institution'),
                required=False,
                default=util.toUnicode(details.get("institution", ""))
            )

            position = schema.TextLine(
                __name__="position",
                title=_(u'label_position', default=u'Position'),
                description=_(
                    u'help_position',
                    default=u'Fill in your position within your Institution'),
                required=False,
                default=util.toUnicode(details.get("position", ""))
            )

            from_country = schema.TextLine(
                __name__="from_country",
                title=_(u'label_from_country', default=u'From country'),
                description=_(u'help_from_country',
                              default=u'Fill in the From country'),
                required=False,
                default=util.toUnicode(details.get("from_country", ""))
            )

            from_city = schema.TextLine(
                __name__="from_city",
                title=_(u'label_from_city', default=u'From city'),
                description=_(u'help_from_city',
                              default=u'Fill in the From city'),
                required=False,
                default=util.toUnicode(details.get("from_city", ""))
            )

            address = schema.Text(
                __name__="address",
                title=_(u'label_address', default=u'Address'),
                description=_(u'help_address',
                              default=u'Fill in the address'),
                required=False,
                default=util.toUnicode(details.get("address", ""))
            )

            self.form.fields += Fields(
                first_name, last_name, phone_numbers,
                institution, position, from_country, from_city, address)

        if self.request.REQUEST_METHOD == 'POST':
            # save values
            if 'form.buttons.save' in self.request.form:
                prefix = 'form.widgets.'
                userid = self.request.form.get('form.widgets.userid')
                member = api.user.get(userid=userid)
                member.setMemberProperties(mapping={
                    "first_name": self.request.form.get(
                        prefix + 'first_name'),
                    "last_name": self.request.form.get(
                        prefix + 'last_name'),
                    "phone_numbers": self.request.form.get(
                        prefix + 'phone_numbers').split("\r\n"),
                    "institution": self.request.form.get(
                        prefix + 'institution'),
                    "position": self.request.form.get(
                        prefix + 'position'),
                    "from_country": self.request.form.get(
                        prefix + 'from_country'),
                    "from_city": self.request.form.get(
                        prefix + 'from_city'),
                    "address": self.request.form.get(
                        prefix + 'address')
                    })


class EditForm(edit.DefaultEditForm):
    """ Override meeting subscriber edit form to add fields
    """


EditView = layout.wrap_form(EditForm)
classImplements(EditView, IDexterityEditForm)
