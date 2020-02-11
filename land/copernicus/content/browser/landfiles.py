from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from land.copernicus.content.content.api import LandFileApi
from urlparse import urlparse
import json
import re

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


def fix_tags_encoding(tags_list):
    try:
        return [
            (x[0].decode("utf-8"), x[1].decode("utf-8")) for x in tags_list]
    except UnicodeEncodeError:
        try:
            return [
                (x[0].decode("latin1"), x[1].decode(
                    "latin1")) for x in tags_list]
        except Exception:
            return safe_unicode(tags_list)


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

    def _do_get(self, landfile):
        return dict(
            status=ACTION_SUCCESS,
            title=landfile.title,
            id=landfile.shortname,
            description=landfile.description,
            download_url=landfile.remoteUrl,
            categorization_tags=fix_tags_encoding(landfile.fileCategories),
            size=landfile.fileSize,
        )

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
            result.update(self._do_get(landfile))

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
        landfiles = self.context.landfiles.get_all()
        _do_get = self._do_get
        return [_do_get(landfile) for landfile in landfiles]

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
        store = self.context.landfiles
        landfiles_titles = [lf.title for lf in store.get_all()]
        store.clear_all()
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

            if len(lines) == 0:
                result = {}
                self.show_error(
                    action, ACTION_EVALUATE, " - the uploaded file is empty.")
                return result

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
        return self.context.landfiles.get_all()

    @staticmethod
    def relative_url(url):
        return urlparse(url).path
