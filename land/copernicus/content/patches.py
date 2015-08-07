from Acquisition import aq_inner
from plone.app.discussion.browser.conversation import ConversationView
from Products.Ploneboard.browser.search import SearchView
from zope.component import getMultiAdapter

old_enabled = ConversationView.enabled
old_crop = SearchView.crop


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
