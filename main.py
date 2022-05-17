import logging

from cofiguration import Configuration
from writer import xls_writer
from zoom_utils.models import ZoomAdminAccount
from zoom_utils.zoom_attendance_report import ZoomAttendanceReport

if __name__ == '__main__':
    print('----- Script running start! ------')
    cofiguration = Configuration()
    zoom_admin_account = ZoomAdminAccount(
        api_key=cofiguration.ZOOM_ACCOUNT_API_KEY,
        api_secret=cofiguration.ZOOM_ACCOUNT_API_SECRET
    )
    report = ZoomAttendanceReport(
        start_date=cofiguration.START_DATE,
        end_date=cofiguration.END_DATE,
        meeting_id=cofiguration.MEETING_ID,
        zoom_admin_account=zoom_admin_account,
        utc_time_diff=cofiguration.UTC_TIME_DIFFERENCE
    )
    meetings, report = report.get_report()
    xlsxwriter = xls_writer.XlsWriter(cofiguration)
    xlsxwriter.write_meeting_report_into_xls(meetings, report)
    print('----- Script running end! ------')
