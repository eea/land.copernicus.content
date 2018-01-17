from Acquisition import aq_inner
from Products.PlonePAS.interfaces.plugins import IUserManagement
from Products.PlonePAS.pas import _doDelUser
from Products.Ploneboard.browser.search import SearchView
from Products.PluggableAuthService.PluggableAuthService import \
    PluggableAuthService
from Products.PluggableAuthService.PluggableAuthService import \
    _SWALLOWABLE_PLUGIN_EXCEPTIONS
from Products.PluggableAuthService.events import PASEvent
from Products.PluggableAuthService.events import PrincipalDeleted
from Products.PluggableAuthService.interfaces.events import IPASEvent
from plone.app.discussion.browser.conversation import ConversationView
from zope.component import getMultiAdapter
from zope.event import notify
from zope.interface import implements

old_enabled = ConversationView.enabled
old_crop = SearchView.crop
old_doDelUser = _doDelUser


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


def crop(self, text):
    """ Fix search results view in Ploneboard
    """
    plone = getMultiAdapter((self.context, self.request), name="plone")
    return plone.cropText(
        text,
        self.site_properties.search_results_description_length,
        self.site_properties.ellipsis
    )
    return old_crop(self)


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
