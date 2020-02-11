from DateTime import DateTime
from Products.Five.browser import BrowserView
import plone.api as api


class GetUpcomingEventsView(BrowserView):
    """ Next future Event and eea.meetings items list
    """
    def __call__(self):
        now = DateTime()

        events = [
            b.getObject() for b in api.portal.get(
                ).portal_catalog.searchResults(
                portal_type=['Event', 'Folderish Event', 'eea.meeting'],
                review_state='published',
                sort_on='start')
            if b.start > now
        ]

        return events
