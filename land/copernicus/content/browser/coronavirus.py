from Products.CMFPlone.utils import isExpired
from Products.Five.browser import BrowserView
import json


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

        res = []
        for item in covid_news:
            res.append(
                {
                    "id": item.id,
                    'title': item.Title,
                    'link': item.getURL(),
                    'image': item.getURL() + '/@@images/image/preview',
                    'abstract': item.Description,
                    'tags': [x for x in item.Subject],
                    'created': item.created.strftime(
                        "%Y-%m-%dT%H:%M:%S+03:00"),
                    'updated': item.modified.strftime(
                        "%Y-%m-%dT%H:%M:%S+03:00")
                }
            )
        return json.dumps(res)
