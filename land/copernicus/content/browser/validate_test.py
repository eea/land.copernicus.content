from Products.Five.browser import BrowserView
import plone.api as api
import urllib

class TestUrlsView(BrowserView):
    """ Administration view for test internal urls
    """

    def get_portal_url(self):
        return self.get_host()

    def get_host(self):
        if 'host' in self.request.form:
            return self.request.form['host']
        return ''

    def get_textarea_urls(self):
        if 'urls' in self.request.form:
            return self.request.form['urls']
        return ''

    def get_input_urls(self):
        url = self.get_portal_url()
        response = []
        if 'urls' in self.request.form:
            items = self.get_textarea_urls().split('\n')
            for item in items:
                itemUrl = item.strip()
                if len(itemUrl):
                    response.append(url + itemUrl)
        return response


    def get_inputs(self):
        return self.process_urls(self.get_input_urls())

    def process_urls(self, urls):
        response = {}
        for url in urls:
            try:
                res  = urllib.urlopen(url)
            except IOError:
                import pdb; pdb.set_trace()

            content = res.read()
            response_code = res.getcode()
            if 'This page does not seem to exist' in content:
                response_code = 404
            res_headers = res.info()
            response.update({url:
                {'code':response_code
                ,'type':res_headers.type
                ,'length':len(content)}
                })
        return response
