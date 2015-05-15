from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.PloneBatch import Batch
from Products.Five.browser import BrowserView
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


class RedirectDownloadUrl(BrowserView):
    """ Redirect to download url for a LandItem if logged in """
    def __call__(self):
        is_anonymous = \
            bool(getToolByName(
                getSite(), 'portal_membership').isAnonymousUser())

        if is_anonymous:
            auto_selected = self.request.form.get('selected', None)
            portal_state = getMultiAdapter(
                (self.context, self.request), name=u'plone_portal_state')
            root_url = portal_state.portal_url()
            land_item_url = self.context.aq_parent.absolute_url()
            login_url = root_url + "/login" + "?came_from=" + land_item_url + \
                "?fieldsetlegend-download=true"
            if auto_selected:
                login_url += "-selected-" + auto_selected
            return self.request.response.redirect(login_url)
        else:
            return self.request.response.redirect(self.context.remoteUrl)
