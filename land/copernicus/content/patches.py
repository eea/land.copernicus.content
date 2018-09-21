from Acquisition import aq_inner
from Products.PlonePAS.interfaces.plugins import IUserManagement
from Products.PlonePAS.pas import _doDelUser
from Products.PluggableAuthService.PluggableAuthService import \
    PluggableAuthService
from Products.PluggableAuthService.PluggableAuthService import \
    _SWALLOWABLE_PLUGIN_EXCEPTIONS
from Products.PluggableAuthService.events import PASEvent
from Products.PluggableAuthService.events import PrincipalDeleted
from Products.PluggableAuthService.interfaces.events import IPASEvent
from collective.captcha.browser.captcha import Captcha
from plone.app.discussion.browser.conversation import ConversationView
from zope.event import notify
from zope.interface import implements

from plone.app.z3cform.interfaces import IPloneFormLayer

old_enabled = ConversationView.enabled
old_doDelUser = _doDelUser
old_verify = Captcha.verify


class IDataGridFieldLayer(IPloneFormLayer):
    """ Marker interface that defines a browser layer.
        (in order to skip PicklingError: Can't pickle <class
         'collective.z3cform.datagridfield.interfaces.IDataGridFieldLayer'>:
        attribute lookup collective.z3cform.datagridfield.interfaces
        .IDataGridFieldLayer failed in demo website)

        We are using an older collective.z3cform.datagridfield version.
    """


def enabled(self):
    """ Fix to enable comments for PloneHelpCenter types
    """
    parent = aq_inner(self.__parent__)
    if parent.portal_type in [
        'HelpCenterDefinition', 'HelpCenterErrorReference', 'HelpCenterFAQ',
        'HelpCenterFAQFolder', 'HelpCenterGlossary', 'HelpCenter',
        'HelpCenterHowTo', 'HelpCenterHowToFolder',
        'HelpCenterInstructionalVideo', 'HelpCenterInstructionalVideoFolder',
        'HelpCenterKnowledgeBase', 'HelpCenterLeafPage', 'HelpCenterLink',
        'HelpCenterLinkFolder', 'HelpCenterReferenceManual',
        'HelpCenterReferenceManualFolder', 'HelpCenterReferenceManualPage',
        'HelpCenterReferenceManualSection', 'HelpCenterTutorial',
        'HelpCenterTutorialFolder', 'HelpCenterTutorialPage'
    ]:
        return True
    return old_enabled(self)


def verify(self, input):
    try:
        words = self._generate_words()
        # Delete the session key, we are done with this captcha
        # EDW Override:
        # self.request.response.expireCookie(COOKIE_ID, path='/')
    except KeyError:
        # No cookie was present
        return False
    input = input.upper()
    return input == words[0] or input == words[1]


Captcha.verify = verify


class IPrincipalBeforeDeletedEvent(IPASEvent):
    """A user is marked to be removed but still into database.
    """


class PrincipalBeforeDeleted(PASEvent):
    implements(IPrincipalBeforeDeletedEvent)


def _doDelUser(self, id):
    """
    Given a user id, hand off to a deleter plugin if available.
    Fix: Add PrincipalBeforeDeleted notification
    """
    plugins = self._getOb('plugins')
    userdeleters = plugins.listPlugins(IUserManagement)

    if not userdeleters:
        raise NotImplementedError(
            "There is no plugin that can delete users.")

    for userdeleter_id, userdeleter in userdeleters:
        # vvv Custom
        notify(PrincipalBeforeDeleted(id))
        # ^^^ Custom

        try:
            userdeleter.doDeleteUser(id)
        except _SWALLOWABLE_PLUGIN_EXCEPTIONS:
            pass
        else:
            notify(PrincipalDeleted(id))


PluggableAuthService._doDelUser = _doDelUser
