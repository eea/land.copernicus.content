from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from zope.globalrequest import getRequest
from Products.statusmessages.interfaces import IStatusMessage
import subprocess


def autofillFullname(principal, event):
    """ Because we splitted user fullname in first_name and last_name on
        register, fullname was omited from schema. But we autofill this
        on register event.
    """
    site = getSite()
    if site is not None:
        first_name = site.REQUEST.form.get('form.first_name', '')
        last_name = site.REQUEST.form.get('form.last_name', '')
        auto_fullname = first_name + " " + last_name
        properties = principal._propertysheets.get('mutable_properties')
        properties.setProperty(principal, 'fullname', auto_fullname)


def forceUpdateProfile(principal, event):
    """ Redirect to edit profile if user has not completed info about
        thematic and institutional domains
    """
    site = getSite()
    if site is not None:
        membership = getToolByName(site, 'portal_membership')
        authenticated_user = membership.getAuthenticatedMember()
        t_d = authenticated_user.getProperty('thematic_domain', '')
        i_d = authenticated_user.getProperty('institutional_domain', '')

        if t_d == '' or i_d == '':
            request = getRequest()

            messages = IStatusMessage(request)
            messages.add(
                u"Please complete your profile adding your Professional " +
                "thematic domain and Institutional domain.", type=u"info")

            if request.get('came_from', None):
                request['came_from'] = ''
                request.form['came_from'] = ''
                request.form['next'] = ''

            edit_profile_url = site.portal_url() + '/@@personal-information'
            request.RESPONSE.redirect(edit_profile_url)


def nice_sizeof(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)


def saveAutoExtractedFileSize(landfile, event):
    """ Auto extract file size for created landfile based on its remoteUrl
        info and save it in landfile.fileSize
    """
    try:
        url = landfile.remoteUrl
        cmd = "curl -sIL " + url
        args = cmd.split()
        process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if "302 Moved" in stdout:
            part = stdout.split("Content-Length: ")[-1]
            file_size = int(
                [token for token in part.split() if token.isdigit()][0])
            file_size = nice_sizeof(file_size)
        elif "200 OK" in stdout:
            content_length_info = stdout.split("\r\n")[1]
            file_size = int(content_length_info.split(":")[1])
            file_size = nice_sizeof(file_size)
        else:
            file_size = "N/A"
    except:
        file_size = "N/A"  # Not Applicable, Not Available, No Answer

    landfile.setFileSize(file_size)
