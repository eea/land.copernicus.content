from datetime import datetime
from DateTime import DateTime
from plone import api
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.PloneBatch import Batch
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from StringIO import StringIO
from zope.component import getMultiAdapter
from zope.component.hooks import getSite
import subprocess
import xlwt
import json


ALL_TAGS = [
    'security', 'emergency', 'observations', 'atmosphere',
    'spatial-data', 'policy', 'agreements', 'infrastructure',
    'open-data', 'land', 'marine', 'climate-change'
]


def is_EIONET_member(member):
    """ Check if a given member is EIONET user
    """
    site = api.portal.get()

    try:
        return "EIONET" in site.acl_users.get(
            "ldap-plugin").acl_users.searchUsers(
            uid=member.getId())[0].get('dn', '')

    except Exception:
        return False


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


def remoteUrl_exists(location):
    try:
        res = subprocess.check_call(['/usr/bin/curl', '-I', '-f', location])
        res = res
        return True
    except subprocess.CalledProcessError:
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
            # [TODO] Investigate why we have here
            # multiple "?selected=@file_id1@file_id2..."
            auto_selected_unique_list = auto_selected.split("?")[0]

            login_url += "-selected-" + auto_selected_unique_list

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


class SearchByTags(BrowserView):
    """ Search by Tags section
    """
    index = ViewPageTemplateFile("templates/search-by-tags.pt")

    def render(self):
        return self.index()

    def __call__(self):
        return self.render()

    def format_tags(self, tags):
        """ Input: ('Climate change', 'Security', 'Marine', 'Not relevant')
            Output: ['climate-change', 'security', 'marine']
        """
        return [
            y for y in [x.replace(" ", "-").lower() for x in tags]
            if y in ALL_TAGS
        ]

    def do_search(self):
        """ Search website for tagged content
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        results = catalog.searchResults(
            {
                'portal_type': ['Event', 'News Item', 'inproximity'],
                'review_state': 'published',
                'sort_on': 'effective',
                'sort_order': 'descending'
            }
        )

        results = [
            {
                'title': x['Title'],
                'description': x['Description'],
                'id': x['id'],
                'url': x.getURL() if x['portal_type'] != 'inproximity'
                else x.getObject().external_link,
                'tags': self.format_tags(x['Subject'])
                if x['portal_type'] != 'inproximity' else
                self.format_tags(x.getObject().subject)
            } for x in results]

        return {'results': json.dumps(results)}


class DownloadLandFileView(BrowserView):
    """ Set Google Analytics custom params and redirect to remoteUrl
    """
    index = ViewPageTemplateFile("templates/download-land-file.pt")

    def render(self):
        return self.index()

    def __call__(self):
        return self.render()

    @property
    def values(self):
        membership = getToolByName(self.context, 'portal_membership')
        authenticated_user = membership.getAuthenticatedMember()
        institutional_domain = authenticated_user.getProperty(
            'institutional_domain')
        professional_thematic_domain = authenticated_user.getProperty(
            'thematic_domain')
        remoteUrl = self.request.form.get('remoteUrl', None)
        is_eionet_member = is_EIONET_member(authenticated_user)

        return {'institutional_domain': institutional_domain,
                'professional_thematic_domain': professional_thematic_domain,
                'is_eionet_member': is_eionet_member,
                'start_download_url': remoteUrl}


# Settings for xls file columns
SHEET_TITLE = 'Users data'
WIDTH_UNIT = 340  # Something like a letter width
SHEET_COLUMNS = {
    # id, order number, column title, column width
    'user_id': [0, 'Username', 15 * WIDTH_UNIT],
    'user_full_name': [1, 'Fullname', 25 * WIDTH_UNIT],
    'user_email': [2, 'Contact email', 35 * WIDTH_UNIT],
    'user_memberships': [3, 'Group memberships', 50 * WIDTH_UNIT],
    'institutional_domain': [4, 'Institutional Domain', 100 * WIDTH_UNIT],
    'professional_thematic_domain': [
        5, 'Professional Thematic Domain', 100 * WIDTH_UNIT],
}


def get_user_data_list(context):
    """ Returns all users data used in xls export
    """
    membership_tool = getToolByName(context, 'portal_membership')

    for member in membership_tool.listMembers():
        user_id = member.getId()
        user_full_name = member.getProperty('fullname', '')
        user_email = member.getProperty('email', '')
        institutional_domain = member.getProperty(
            'institutional_domain')
        professional_thematic_domain = member.getProperty(
            'thematic_domain')
        groups = api.group.get_groups(user=member)
        user_memberships = '; '.join([group.id for group in groups])

        yield dict(
            user_id=user_id,
            user_full_name=user_full_name,
            user_email=user_email,
            user_memberships=user_memberships,
            institutional_domain=institutional_domain,
            professional_thematic_domain=professional_thematic_domain
        )


class ExportUsersXLS(BrowserView):
    """ A view linked from Site Setup that exports a xls file with info
        about registered users.
    """
    def __call__(self):
        return self.export_users_data()

    def export_users_data(self):
        """ Generates the xls file
        """
        user_data_records = get_user_data_list(self.context)

        xls_book = xlwt.Workbook()
        xls_sheet = xls_book.add_sheet(SHEET_TITLE)

        for row_index, data_dict in enumerate(user_data_records):
            for data_key in data_dict:
                column_index = SHEET_COLUMNS[data_key][0]
                value = data_dict.get(data_key, None)

                if row_index == 0:
                    column_name = SHEET_COLUMNS[data_key][1]
                    column_width = SHEET_COLUMNS[data_key][2]
                    xls_sheet.write(row_index, column_index, column_name)
                    xls_sheet.col(column_index).width = column_width

                try:
                    value = value.replace(tzinfo=None)
                except Exception:
                    pass

                if isinstance(value, DateTime):
                    str_date = value.strftime('%d/%m/%y')
                    xls_sheet.write(row_index + 1, column_index, str_date)
                elif isinstance(value, datetime):
                    str_date = value.strftime('%d/%m/%y')
                    xls_sheet.write(row_index + 1, column_index, str_date)
                else:
                    if value is not None:
                        xls_sheet.write(
                            row_index + 1, column_index, value.decode('utf-8'))
                    else:
                        xls_sheet.write(row_index + 1, column_index, value)

        xls_file = StringIO()
        xls_book.save(xls_file)
        xls_file.seek(0)
        filename = '{0}.xls'.format(SHEET_TITLE)

        self.request.response.setHeader(
            'Content-type', 'application/vnd.ms-excel; charset=utf-8'
        )
        self.request.response.setHeader(
            'Content-Disposition', 'attachment; filename={0}'.format(filename)
        )

        return xls_file.read()


class InProximityView(BrowserView):
    """ In Proximity item view
    """
    index = ViewPageTemplateFile("templates/inproximity_view.pt")

    def render(self):
        return self.index()

    def __call__(self):
        return self.render()
