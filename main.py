import logging

logging.basicConfig(level=logging.INFO)

from configuration import Configuration
from writer import xls_writer
from zoom_utils.models import ZoomAdminAccount
from zoom_utils.zoom_attendance_report import ZoomAttendanceReport

if __name__ == '__main__':
    logging.info('----- Script running start! ------')
    configuration = Configuration()
    zoom_admin_account = ZoomAdminAccount(
        account_id=configuration.ZOOM_ACCOUNT_ID,
        client_id=configuration.ZOOM_ACCOUNT_CLIENT_ID,
        client_secret=configuration.ZOOM_ACCOUNT_CLIENT_SECRET
    )
    report = ZoomAttendanceReport(
        start_date=configuration.START_DATE,
        end_date=configuration.END_DATE,
        meeting_id=configuration.MEETING_ID,
        zoom_admin_account=zoom_admin_account,
        utc_time_diff=configuration.UTC_TIME_DIFFERENCE
    )
    meetings, report = report.get_report()
    xlsxwriter = xls_writer.XlsWriter(configuration)
    xlsxwriter.write_meeting_report_into_xls(meetings, report)
    logging.info('----- Script running end! ------')
