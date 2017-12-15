from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from StringIO import StringIO
from calendar import monthrange
from datetime import datetime
from persistent.dict import PersistentDict
from zope.annotation import IAnnotations
import plone.api as api
import transaction
import xlwt

USERS_STATISTICS_KEY = "land.copernicus.content.users_statistics"


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


def period_title(period):
    """ Input: (DateTime, DateTime)
        Output format (as used in annotations): 2015/01/01-2015/01/31
    """
    return "{0}-{1}".format(
        period[0].strftime("%Y/%m/%d"),
        period[1].strftime("%Y/%m/%d")
    )


def save_users_statistics_reports(site, time_periods, reports):
    """ Input:
        - the list of time periods (as used in generate_users_statistics())
        - the list of reports (as returned by generate_users_statistics())

        Save reports as annotations on site in format:
        '2015/01/01-2015/01/31': {
            'active': 300,
            'new': 100,
            'total': 2000,
            'last_update': DateTime
        }

        Return True on saved or False for invalid input
    """
    stats_annot = IAnnotations(site).setdefault(
            USERS_STATISTICS_KEY, PersistentDict({}))

    if len(time_periods) == len(reports):
        for i in range(0, len(time_periods)):
            report = reports[i]
            report['last_update'] = DateTime()
            stats_annot[period_title(time_periods[i])] = report

            print "Saved report: {0}".format(period_title(time_periods[i]))
    else:
        return False

    transaction.commit()
    return True


def get_users_statistics_reports(site):
    """ Get existing reports saved in annotations
    """
    annotations = IAnnotations(site)
    reports = annotations.get(USERS_STATISTICS_KEY, None)

    return reports


def all_periods():
    """ Return the list of time_periods by months from Jan. 2013 to current
        year, last complete month
    """
    res = []
    now = DateTime()
    current_year = now.year()
    current_month = now.month()

    years = [x for x in range(2013, current_year + 1)]
    months = [x for x in range(1, 13)]
    for year in years:
        for month in months:
            if year == current_year and month >= current_month:
                pass
            else:
                days = monthrange(year, month)[1]
                start_date = DateTime("""{0}/{1}/{2}""".format(year, month, 1))
                end_date = DateTime(
                        """{0}/{1}/{2}""".format(year, month, days))
                res.append((start_date, end_date))

    return res


def generate_users_statistics(site, time_periods=[]):
    """ Return statistics for given time periods

        Input: [(DateTime, DateTime), (DateTime, DateTime), ...]
            Default: [(yesterday, today)]

        Output: [results, results, results, ...]
            results format:
                {
                    'total': 12000,
                    'active': 350,
                    'new': 20
                }
    """
    res = []

    if len(time_periods) == 0:
        return res

    for period in time_periods:
        res.append({'total': 0, 'active': 0, 'new': 0})

    mt = getToolByName(site, 'portal_membership')
    md = getToolByName(site, 'portal_memberdata')

    all_members = [x for x in md._members.keys()]

    for i in range(0, len(all_members)):
        user_id = all_members[i]
        print "{0}: {1}".format(i, user_id)
        user_member_data = mt.getMemberById(user_id)

        if user_member_data is not None:
            user = user_member_data.getUser()

            try:
                active_last = user.getPropertysheet(
                    'mutable_properties').getProperty('last_login_time')
            except Exception:
                active_last = None

            try:
                active_from = user_member_data.bobobase_modification_time()
            except Exception:
                active_from = None

            was_active = True
            if active_last is not None and active_from is not None:
                if active_last < DateTime("2010/01/01"):
                    # NEVER USED
                    # A lot of accounts have 2000/01/01 as last login.
                    # This means the account was created but never used.
                    was_active = False

                for j in range(0, len(time_periods)):
                    start_date = time_periods[j][0]
                    end_date = time_periods[j][1]

                    if active_last >= start_date and \
                            active_from <= end_date and was_active:
                        res[j]['active'] += 1

                    if active_from <= end_date:
                        res[j]['total'] += 1
                        if active_from >= start_date:
                            res[j]['new'] += 1

    return res


def schedule_reports(site, time_periods=[]):
    """ Schedule reports by setting last_update param as pending.
        The script will take care of them.
    """
    stats_annot = IAnnotations(site).setdefault(
            USERS_STATISTICS_KEY, PersistentDict({}))

    for period in time_periods:
        title = period_title(period)
        if stats_annot.get(title, None) is None:
            stats_annot[title] = {'active': 0, 'new': 0, 'total': 0}

        stats_annot[title]['last_update'] = 'pending'

        print "Scheduled report: {0}".format(title)
    return True


def schedule_all_reports(site):
    """ Good for init lots of reports
    """
    periods = all_periods()
    schedule_reports(site=site, time_periods=periods)
    return True


def schedule_missing_monthly_reports(site):
    """ Make sure we are up to date with monthly reports
    """
    periods = all_periods()
    reports = get_users_statistics_reports(site)

    todo_reports = []
    for period in periods:
        title = period_title(period)
        try:
            if title not in reports.keys():
                todo_reports.append(period)
        except Exception:
            todo_reports.append(period)

    if len(todo_reports) > 0:
        schedule_reports(site=site, time_periods=todo_reports)
    return True


def get_pending_reports(site):
    """ Return all pending reports as list of time periods
    """
    reports = get_users_statistics_reports(site)

    pending = []
    for report_title in reports.keys():
        report = reports[report_title]
        if report.get('last_update', None) == 'pending':
            parts = report_title.split('-')
            start_date = DateTime(parts[0])
            end_date = DateTime(parts[1])
            pending.append((start_date, end_date))

    return pending


def solve_pending_reports(site):
    """ Generate users statistics for all pending reports
    """
    pending_time_periods = get_pending_reports(site)
    reports = generate_users_statistics(
        site, time_periods=pending_time_periods)
    return save_users_statistics_reports(
        site, time_periods=pending_time_periods, reports=reports)


def remove_all_reports(site):
    """ Delete annotations related to users statistics
    """
    del IAnnotations(site)[USERS_STATISTICS_KEY]


def users_statistics_operations_center(site):
    """ Take care of:
        - annotations exist
        - we are up to date with monthly reports
        - all pending reports are solved

        To be used by scheduled script.
    """
    reports = get_users_statistics_reports(site)
    if reports is None:
        schedule_all_reports(site)
    else:
        schedule_missing_monthly_reports(site)

    solve_pending_reports(site)
    return True


class UsersStatisticsView(BrowserView):
    """ Admin panel for users statistics
    """
    index = ViewPageTemplateFile("templates/users_statistics.pt")

    def render(self):
        return self.index()

    @property
    def reports(self):
        site = self.context.portal_url.getPortalObject()
        return get_users_statistics_reports(site)

    def __call__(self):
        site = self.context.portal_url.getPortalObject()

        if 'submit' in self.request.form:
            start_date = DateTime(self.request.form.get('start-date'))
            end_date = DateTime(self.request.form.get('end-date'))
            time_periods = [(start_date, end_date)]
            schedule_reports(site=site, time_periods=time_periods)

            self.request.form = {}

        if 'refresh' in self.request.form:
            self.request.form = {}

        if 'remove' in self.request.form:
            remove_all_reports(site)
            self.request.form = {}
        return self.render()
