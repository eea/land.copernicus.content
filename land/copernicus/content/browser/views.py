import json
from datetime import datetime
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.PloneBatch import Batch
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from StringIO import StringIO
from zope.component import getMultiAdapter
from zope.component.hooks import getSite
import plone.api as api
import subprocess
import xlwt
import json
import re


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


class GoPDB(BrowserView):
    def __call__(self):

        import pdb
        pdb.set_trace()
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
                except:
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


ACTION_GET = 'get'
ACTION_POST = 'post'
ACTION_PUT = 'put'
ACTION_DELETE = 'delete'
ACTION_SUCCESS = 'success'
ACTION_ERROR = 'error'
ACTION_INFO = 'info'
ACTION_EVALUATE = 'evaluate'


def parse_tags(string_input):
    """ Input: '(tagname1, tagvalue1),(tagname2,tagvalue2),
                ( tagname3, tagvalue3 ), (tag name4,tag value4)'
        Output: [
            ("tagname1", "tagvalue1"), ("tagname2", "tagvalue2"),
            ("tagname3", "tagvalue3"), ("tag name4", "tag value4")
        ]
    """
    expression = '\(\s?(.*?)\s?,\s?(.*?)\s?\)'
    return re.findall(expression, string_input)


class AdminLandFilesView(BrowserView):
    """ Administration view for land files of a land item
    """
    index = ViewPageTemplateFile("templates/admin-land-files.pt")

    def render(self):
        return self.index()

    def show_error(self, item, action, details):
        """ Show an error message related to an action for a land file
        """
        messages = IStatusMessage(self.request)
        messages.add(
            u"""Error on {action} {item} {details}""".format(
                action=safe_unicode(action),
                item=safe_unicode(item),
                details=safe_unicode(details)
            ), type=ACTION_ERROR)

    def show_info(self, item, action, details):
        """ Show an info message related to an action for a land file
        """
        messages = IStatusMessage(self.request)
        messages.add(
            u"""Success on {action} {item} {details}""".format(
                action=safe_unicode(action),
                item=safe_unicode(item),
                details=safe_unicode(details)
            ), type=ACTION_INFO)

    def do_get(self, title, logs=True):
        """ Get information about a landfile
            Input: landfile title
            Output: dict containing landfile details
            Also show error or info msg
        """
        landfile = self.context.getFolderContents(
            contentFilter={
                'portal_type': 'LandFile',
                'Title': title
            }
        )
        result = {
            'title': safe_unicode(title),
            'status': ACTION_ERROR
        }
        if len(landfile) > 0:
            landfile = landfile[0].getObject()
            result['status'] = ACTION_SUCCESS
            result['title'] = landfile.Title().decode('utf8')
            result['id'] = landfile.id
            result['description'] = landfile.Description().decode('utf8')
            result['download_url'] = landfile.remoteUrl
            result['categorization_tags'] = landfile.fileCategories
            result['size'] = landfile.fileSize
            result['url'] = landfile.absolute_url()

        if result['status'] == ACTION_SUCCESS and logs is True:
            self.show_info(title, ACTION_GET, "- " + result['url'])

        if result['status'] == ACTION_ERROR and logs is True:
            self.show_error(
                title, ACTION_GET, '- No item with this title found')

        return result

    def do_get_all(self, logs=True):
        """ Get information about all landfiles in this context
            Output: list of dicts containing landfiles details
        """
        landfiles = self.context.getFolderContents(
            contentFilter={
                'portal_type': 'LandFile',
            }
        )
        result = []
        for landfile in landfiles:
            result.append(self.do_get(landfile.getObject().Title()))

        return result

    def do_post(self, title, description, download_url, categorization_tags,
                logs=True):
        """ Create a landfile item
            Input: fields values
            Output: title, status (error or success)
            Also show error or info message
        """
        result = {
            'title': title.decode('utf8'),
            'status': ACTION_SUCCESS
        }
        valid_tags = [
            {'name': x[0], 'value': x[1]} for x in parse_tags(
                categorization_tags) if x[0] in
            self.context.fileCategories
        ]

        try:
            landfile = api.content.create(
                container=self.context, type='LandFile', title=title,
                description=description, remoteUrl=download_url,
                fileCategories=valid_tags)
            url = landfile.absolute_url()
            api.content.transition(obj=landfile, transition='publish')
            if logs is True:
                self.show_info(title, ACTION_POST, "- " + url)
        except Exception:
            result['status'] = ACTION_ERROR
            if logs is True:
                self.show_error(title, ACTION_POST, "- landfile not created.")
        return result

    def do_delete(self, title, logs=True):
        """ Delete all landfiles with given title
            Input: landfile title
            Output: title, status
            Also show error or info message
        """
        landfiles = self.context.getFolderContents(
            contentFilter={
                'portal_type': 'LandFile',
                'Title': title
            }
        )
        result = {
            'title': title.decode('utf8'),
            'status': ACTION_SUCCESS
        }
        if len(landfiles) > 0:
            for a_landfile in landfiles:
                landfile = a_landfile.getObject()
                result['title'] = landfile.Title().decode('utf8')
                url = landfile.absolute_url()
                self.context.manage_delObjects([landfile.id])
                if logs is True:
                    self.show_info(title, ACTION_DELETE, "- " + url)
        else:
            result['status'] = ACTION_ERROR
            if logs is True:
                self.show_error(
                    title, ACTION_DELETE, '- No items with this title found')

        return result

    def do_delete_all(self, logs=True):
        """ Delete all landfiles in this context
            Output: list of dicts containing title and status
        """
        landfiles = self.context.getFolderContents(
            contentFilter={
                'portal_type': 'LandFile',
            }
        )
        result = []
        landfiles_titles = [x.getObject().Title() for x in landfiles]
        for landfile in landfiles_titles:
            result.append(self.do_delete(landfile))

        return result

    def do_put(self, title, description, download_url, categorization_tags,
               logs=True):
        """ Replace a landfile
        """
        del_result = self.do_delete(title, logs=False)
        if del_result['status'] == ACTION_ERROR:
            if logs is True:
                self.show_error(
                    title, ACTION_PUT, '- Cannot delete old landfile')
            return {
                'title': title.decode('utf8'),
                'status': ACTION_ERROR
            }
        else:
            create_result = self.do_post(
                title=title, description=description,
                download_url=download_url,
                categorization_tags=categorization_tags, logs=False)

            if create_result['status'] == ACTION_ERROR:
                if logs is True:
                    self.show_error(
                        title, ACTION_PUT, '- Cannot create new landfile')
                return {
                    'title': title.decode('utf8'),
                    'status': ACTION_ERROR
                }
            else:
                if logs is True:
                    self.show_info(
                        title, ACTION_PUT, '- Landfile replaced')
                return {
                    'title': title.decode('utf8'),
                    'status': ACTION_SUCCESS
                }

    def do_operations(self):
        """ Do the requested operation by form
        """
        action = self.request.form.get('inlineRadioOptions', None)
        txt_file = self.request.form.get('file', None)

        if txt_file.filename is not '':
            if action == ACTION_GET:
                # GET info for a list of landfiles
                landfiles = txt_file.read().splitlines()
                output_json = []

                if landfiles[0].lower() == 'all':
                    output_json = self.do_get_all()
                else:
                    for landfile in landfiles:
                        output_json.append(self.do_get(landfile))
                result = json.dumps(
                    output_json, ensure_ascii=False).encode('utf8')

            elif action == ACTION_DELETE:
                # DELETE a list of landfiles
                landfiles = txt_file.read().splitlines()
                output_json = []

                if landfiles[0].lower() == 'all':
                    output_json = self.do_delete_all()
                else:
                    for landfile in landfiles:
                        output_json.append(self.do_delete(landfile))
                result = json.dumps(
                        output_json, ensure_ascii=False).encode('utf8')

            elif action == ACTION_POST:
                # CREATE landfiles
                lines = txt_file.read().splitlines()
                landfiles = [lines[i:i + 4] for i in xrange(0, len(lines), 4)]
                result = []
                for landfile in landfiles:
                    a_result = self.do_post(
                        title=landfile[0],
                        description=landfile[1],
                        download_url=landfile[2],
                        categorization_tags=landfile[3]
                        )
                    result.append(a_result)
                result = json.dumps(
                     result, ensure_ascii=False).encode('utf8')

            elif action == ACTION_PUT:
                # UPDATE landfiles
                lines = txt_file.read().splitlines()
                landfiles = [lines[i:i + 4] for i in xrange(0, len(lines), 4)]
                result = []
                for landfile in landfiles:
                    a_result = self.do_put(
                        title=landfile[0],
                        description=landfile[1],
                        download_url=landfile[2],
                        categorization_tags=landfile[3]
                        )
                    result.append(a_result)
                result = json.dumps(
                     result, ensure_ascii=False).encode('utf8')

            else:
                result = {}
                self.show_error(
                    action, ACTION_EVALUATE,
                    " - missing action. Use radio buttons to select one.")
        else:
            result = {}
            self.show_error(
                txt_file.filename, ACTION_EVALUATE,
                " - missing text file. Use file input to upload it.")
        return result

    def __call__(self):
        self.output_json = {}
        if 'submit' in self.request.form:
            self.output_json = self.do_operations()
        return self.render()

    @property
    def values(self):
        return {'output_json': self.output_json}
