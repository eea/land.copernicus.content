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


class UsersStatisticsView(BrowserView):
    """ WIP Users Statistics
        TODO replace with script
    """
    def __call__(self):
        NA = "N/A"
        site = self.context.portal_url.getPortalObject()
        mt = getToolByName(site, 'portal_membership')
        md = getToolByName(site, 'portal_memberdata')

        all_members = [x for x in md._members.keys()]
        local_members = mt.listMemberIds()
        eionet_members = [x for x in all_members if x not in local_members]

        stats = []
        incomplete = 0
        strange = 0
        max_records = 200  # TODO Iterate over all members, when done

        for i in range(0, max_records):

            user_id = all_members[i]
            user_member_data = mt.getMemberById(user_id)
            if user_member_data is not None:
                user = user_member_data.getUser()

                try:
                    active_last = user.getPropertysheet(
                        'mutable_properties').getProperty('last_login_time')
                except Exception:
                    active_last = NA

                try:
                    active_from = user.bobobase_modification_time()
                except Exception:
                    active_from = NA

                if(active_last is not NA and active_from is not NA):
                    if active_last < active_from:
                        strange += 1

            else:
                active_last = NA
                active_from = NA
                incomplete += 1

            record = {
                'id': user_id,
                'from': active_from,
                'to': active_last,
                'is_eionet': user_id in eionet_members
            }
            stats.append(record)

            print i

        return {
            'all': len(all_members),
            'local': len(local_members),
            'eionet_members': len(eionet_members),
            'stats': stats,
            'incomplete': incomplete,
            'strange': strange
        }
