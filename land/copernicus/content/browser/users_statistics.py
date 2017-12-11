from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from StringIO import StringIO
from datetime import datetime
import plone.api as api
import xlwt


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


# from Products.CMFCore.utils import getToolByName
#
# site = self.context.portal_url.getPortalObject()
#
# mt = getToolByName(site, 'portal_membership')
# md = getToolByName(site, 'portal_memberdata')
# ut = getToolByName(self, 'acl_users')
#
# all_members = [x for x in md._members.keys()]
# local_members = mt.listMemberIds()
# eionet_members = [x for x in all_members if x not in local_members]
#
# user = mt.getAuthenticatedMember()
# user.bobobase_modification_time()
#
# mt.getMemberById('gonchvic').bobobase_modification_time()
#
# (Pdb) md.getMemberDataContents()
# [{'orphan_count': 669, 'member_count': 14386}]
# members = md._members

# DateTime('2015/05/12 10:54:7.022828 GMT+3')
# user
# <MemberData at /copernicus/portal_memberdata/ghitab ...
# user.getUser()
# <PloneUser 'ghitab'>

# userid = "someid"
# site.acl_users.get("ldap-plugin").acl_users.searchUsers(uid=userid)[0]
# {
#   'dn': 'uid=someid,ou=Users,o=EIONET,l=Europe',
#   'mail': 'someid@eaudeweb.ro', 'uid': 'someid',
#   'sn': 'Someid', 'cn': 'Some Name'
# }
# mt.getMemberById('someid').getProperty('thematic_domain', '')
# 'Agriculture'

# user.getUser().getOrderedPropertySheets()[0])
# user.getUser().getOrderedPropertySheets()[0].propertyItems()
# [('email', u'ghita.bizau@eaudeweb.ro'), ('fullname', u'Ghita Bizau')]
# user.getUser().getOrderedPropertySheets()[1].propertyItems()
# [('email', 'ghita_bizau@yahoo.com'), ('portal_skin', ''), ('listed', True),
#  ('login_time', DateTime('2017/12/05 15:40:40.806253 GMT+2')),
#  ('last_login_time', DateTime('2017/11/20 14:04:8.161584 GMT+2')),
#  ('fullname', ''), ('error_log_update', 0.0), ('home_page', ''),
#  ('location', ''), ('description', ''), ('language', ''),
#  ('ext_editor', False), ('wysiwyg_editor', ''), ('visible_ids', False),
#  ('first_name', u'Ghita'), ('last_name', u'Bizau'),
#  ('thematic_domain', 'Agriculture'), ('institutional_domain', 'Education'),
#  ('reason', ''), ('job_title', ''),
#  ('postal_address', u'Fundatia Life Cuza Voda \nlanga Biserica cu Luna'),
#  ('telephone', ''), ('mobile', ''), ('fax', ''), ('organisation', '')]

# len(membership_tool.listMemberIds())
# 13718

# user = mt.getMemberById('ghitab')
# user.getUser().getPropertysheet(
#     'mutable_properties').getProperty('last_login_time')
# DateTime('2017/12/05 15:40:40.806253 GMT+2')
