from Products.CMFPlone.utils import isExpired
from Products.Five.browser import BrowserView


class ExportNews(BrowserView):
    """ JSON list of Coronavirus news COVID-19
    """

    def __call__(self):
        catalog = self.context.portal_catalog
        query = {
            'portal_type': 'News Item',
            'sort_on': 'effective',
            'sort_order': 'descending',
            'review_state': 'published',
        }

        # [
        #     {
        #         "id":"123",
        #         "title":"Title",
        #         "link":"https:\/\/...",
        #         "image":"https:\/\/...",
        #         "abstract":"text",
        #         "tags":["Coronavirus"],
        #         "created":"2020-04-01T13:10:48+01:00",
        #         "updated":"2020-04-01T11:34:02+01:00"
        #     },{...}
        # ]

        result = [x for x in catalog(**query) if isExpired(x) != 1]
        covid_news = [
            x for x in result if 'Coronavirus' in x.Subject or
            'Covid-19' in x.Subject]

        return covid_news
