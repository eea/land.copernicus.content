from Products.Five.browser import BrowserView


class ExportNews(BrowserView):
    """ JSON list of Coronavirus news COVID-19
    """

    def __call__(self):
        return {"a": "aaa"}
