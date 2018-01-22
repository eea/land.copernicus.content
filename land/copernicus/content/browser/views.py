import re
import json
import subprocess
from urlparse import urlparse

from zope.component import getMultiAdapter
from zope.component.hooks import getSite

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.PloneBatch import Batch
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage

import plone.api as api

from land.copernicus.content.content.api import LandFileApi


def is_EIONET_member(member):
    """ Check if a given member is EIONET user
    """
    site = api.portal.get()

    try:
        return "EIONET" in (
            site.acl_users.get("ldap-plugin")
            .acl_users.searchUsers(uid=member.getId())
            [0].get('dn', '')
        )

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

    def show_error(self, item, action, details=''):
        """ Show an error message related to an action for a land file
        """
        messages = IStatusMessage(self.request)
        messages.add(
            u"""Error on {action} {item} {details}""".format(
                action=action,
                item=item,
                details=details,
            ), type=ACTION_ERROR)

    def show_info(self, item, action, details=''):
        """ Show an info message related to an action for a land file
        """
        messages = IStatusMessage(self.request)
        messages.add(
            u"""Success on {action} {item} {details}""".format(
                action=action,
                item=item,
                details=details,
            ), type=ACTION_INFO)

    def do_get(self, title, logs=True):
        """ Get information about a landfile
            Input: landfile title
            Output: dict containing landfile details
            Also show error or info msg
        """
        lfa = LandFileApi(self.context.landfiles)
        landfile = lfa.get(title)

        result = {
            'title': title,
            'status': ACTION_ERROR
        }
        if landfile:
            result['status'] = ACTION_SUCCESS
            result['title'] = landfile.title
            result['id'] = landfile.shortname
            result['description'] = landfile.description
            result['download_url'] = landfile.remoteUrl
            result['categorization_tags'] = landfile.fileCategories
            result['size'] = landfile.fileSize

        if result['status'] == ACTION_SUCCESS and logs is True:
            self.show_info(title, ACTION_GET)

        if result['status'] == ACTION_ERROR and logs is True:
            self.show_error(
                title, ACTION_GET, '- No item with this title found')

        return result

    def do_get_all(self):
        """ Get information about all landfiles in this context
            Output: list of dicts containing landfiles details
        """
        landfiles = self.context.landfiles
        do_get = self.do_get
        return [do_get(title) for title in landfiles]

    def do_post(self, title, description, download_url, categorization_tags,
                logs=True):
        """ Create a landfile item
            Input: fields values
            Output: title, status (error or success)
            Also show error or info message
        """
        result = {
            'title': title,
            'status': ACTION_SUCCESS
        }

        fileCategories = self.context.fileCategories
        valid_tags = tuple(
            (name, value)
            for name, value in parse_tags(categorization_tags)
            if name in fileCategories
        )

        lfa = LandFileApi(self.context.landfiles)

        try:
            lfa.add_with_filesize(
                title=title,
                description=description,
                remoteUrl=download_url,
                fileCategories=valid_tags,
            )
            if logs is True:
                self.show_info(title, ACTION_POST)
        except (OSError, KeyError) as err:
            result['status'] = ACTION_ERROR
            if logs is True:
                self.show_error(title, ACTION_POST, '- ' + err.message)
        return result

    def do_delete(self, title, logs=True):
        """ Delete all landfiles with given title
            Input: landfile title
            Output: title, status
            Also show error or info message
        """
        result = {
            'title': title,
            'status': ACTION_SUCCESS
        }
        lfa = LandFileApi(self.context.landfiles)
        try:
            lfa.delete(title)
            if logs is True:
                self.show_info(title, ACTION_DELETE)
        except KeyError:
            result['status'] = ACTION_ERROR
            if logs is True:
                self.show_error(
                    title, ACTION_DELETE, '- No items with this title found')

        return result

    def do_delete_all(self, logs=True):
        """ Delete all landfiles in this context
            Output: list of dicts containing title and status
        """
        tree = self.context.landfiles
        landfiles_titles = tuple(tree.keys())
        tree.clear()
        if logs is True:
            for title in landfiles_titles:
                self.show_info(title, ACTION_DELETE)
        return [
            dict(title=title, status=ACTION_SUCCESS)
            for title in landfiles_titles
        ]

    def do_put(self, title, description, download_url, categorization_tags,
               logs=True):
        """ Replace a landfile
        """
        result = {
            'title': title,
            'status': ACTION_SUCCESS
        }

        fileCategories = self.context.fileCategories
        valid_tags = tuple(
            (name, value)
            for name, value in parse_tags(categorization_tags)
            if name in fileCategories
        )

        lfa = LandFileApi(self.context.landfiles)

        try:
            lfa.edit_with_filesize(
                title,
                title=title,
                description=description,
                remoteUrl=download_url,
                fileCategories=valid_tags,
            )
            if logs is True:
                self.show_info(title, ACTION_PUT, '- Landfile replaced')
        except (OSError, KeyError) as err:
            result['status'] = ACTION_ERROR
            if logs is True:
                self.show_error(title, ACTION_POST, '- ' + err.message)

        return result

    def do_operations(self):
        """ Do the requested operation by form
        """
        action = self.request.form.get('inlineRadioOptions', None)
        txt_file = self.request.form.get('file', None)

        if txt_file.filename is not '':
            txt_content = txt_file.read()
            txt_decoded = None
            try:
                txt_decoded = txt_content.decode('utf-8')
            except UnicodeDecodeError:
                txt_decoded = txt_content.decode('latin1')
            txt_decoded = txt_decoded or safe_unicode(txt_content)
            lines = txt_decoded.splitlines()
            if action == ACTION_GET:
                # GET info for a list of landfiles
                output_json = []

                if lines[0].lower() == 'all':
                    output_json = self.do_get_all()
                else:
                    for line in lines:
                        output_json.append(self.do_get(line))
                result = json.dumps(
                    output_json, ensure_ascii=False)

            elif action == ACTION_DELETE:
                # DELETE a list of landfiles
                output_json = []

                if lines[0].lower() == 'all':
                    output_json = self.do_delete_all()
                else:
                    for line in lines:
                        output_json.append(self.do_delete(line))
                result = json.dumps(
                        output_json, ensure_ascii=False)

            elif action == ACTION_POST:
                # CREATE landfiles
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
                     result, ensure_ascii=False)

            elif action == ACTION_PUT:
                # UPDATE landfiles
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
                     result, ensure_ascii=False)

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


class LandFilesContentView(BrowserView):

    @property
    def landfiles(self):
        return self.context.landfiles.values()

    @staticmethod
    def relative_url(url):
        return urlparse(url).path
