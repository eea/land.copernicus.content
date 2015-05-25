from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.PloneBatch import Batch
from Products.Five.browser import BrowserView
import urllib2
from zope.component.hooks import getSite
from zope.component import getMultiAdapter


class LandItemsOverview(BrowserView):
    """Overview page for LandItems
    """
    def __call__(self):
        """ Render the content item listing.
        """
        self.limit = self.request.get('limit', '10')
        start = self.request.get("b_start", '0')
        self.contents = self.find_landitems(start)

        return self.index()

    def find_landitems(self, start):
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog.searchResults({'portal_type': 'LandItem'})
        results = [result.getObject() for result in results]
        batch = Batch(results, int(self.limit), int(start), orphan=0)

        return batch


class LandProductInlineView(BrowserView):
    """ Inline view for products
    #TODO: hide plone.belowcontentbody.relateditems viewlet
    """

    def __call__(self):
        if not getattr(self.context, 'meta_type', '') == "LandItem":
            return ""
        return self.index()


class GoPDB(BrowserView):
    def __call__(self):

        import pdb; pdb.set_trace()
        return "done"


def remoteUrl_exists(remoteUrl):
    try:
        urllib2.urlopen(remoteUrl)
        return True
    except urllib2.HTTPError, e:
        print(e.code)
        return False
    except urllib2.URLError, e:
        print(e.args)
        return False


class RedirectDownloadUrl(BrowserView):
    """ Redirect to download url for a LandItem if logged in """

    def url_login_with_params(self):
        """ Returns the login url with params in came_from url """

        auto_selected = self.request.form.get('selected', None)
        portal_state = getMultiAdapter(
            (self.context, self.request), name=u'plone_portal_state')
        root_url = portal_state.portal_url()
        land_item_url = self.context.aq_parent.absolute_url()
        login_url = root_url + "/login" + "?came_from=" + land_item_url + \
            "?fieldsetlegend-download=True"

        if auto_selected:
            login_url += "-selected-" + auto_selected

        return login_url

    def url_open_download_tab(self):
        """ Sets url param used to open download tab """
        url_tab = self.context.aq_parent.absolute_url() + \
            '?fieldsetlegend-download=true'
        return url_tab

    def url_missing_file(self):
        """ Returns the url for case: file missing, page not found """

        land_file_title = self.context.title
        error_param = '-error-not-found-' + land_file_title
        error_url = self.url_open_download_tab() + error_param

        return error_url

    def url_profile_error(self):
        """ Returns the url for case: profile is not complete
            missing thematic_domain or institutional_domain fields
        """

        error_param = '-error-profile-not-complete'
        error_url = self.url_open_download_tab() + error_param

        return error_url

    def url_download(self):
        """ Returns the page url used to set google analytics custom vars
            before redirecting to land file remoteUrl
        """
        land_item_url = self.context.aq_parent.absolute_url()
        url_download = land_item_url + '/@@download-land-file?remoteUrl=' + \
            self.context.remoteUrl

        return url_download

    def __call__(self):
        is_anonymous = \
            bool(getToolByName(
                getSite(), 'portal_membership').isAnonymousUser())

        if not is_anonymous:
            profile_is_complete = True
            membership = getToolByName(self.context, 'portal_membership')
            authenticated_user = membership.getAuthenticatedMember()
            t_d = authenticated_user.getProperty('thematic_domain', '')
            i_d = authenticated_user.getProperty('institutional_domain', '')
            if t_d == '' or i_d == '':
                profile_is_complete = False

        if is_anonymous:
            return self.request.response.redirect(self.url_login_with_params())
        else:
            remoteUrl = self.context.remoteUrl
            if remoteUrl_exists(remoteUrl):
                if profile_is_complete:
                    return self.request.response.redirect(self.url_download())
                else:
                    return self.request.response.redirect(
                        self.url_profile_error())
            else:
                return self.request.response.redirect(self.url_missing_file())


class DownloadLandFileView(BrowserView):
    """ Set Google Analytics custom params and redirect to remoteUrl
    """
    def __call__(self):
        remoteUrl = self.request.form.get('remoteUrl', None)
        if remoteUrl is not None:
            return self.request.response.redirect(remoteUrl)
