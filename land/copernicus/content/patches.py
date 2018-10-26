from Acquisition import aq_inner
from plone.app.discussion.browser.conversation import ConversationView

old_enabled = ConversationView.enabled


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
