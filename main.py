from properties import ProjectProperties
from writer import xls_writer
from zoom_utils.models import ZoomAdminAccount
from zoom_utils.zoom_attendance_report import ZoomAttendanceReport

if __name__ == '__main__':
    print('----- Script running start! ------')
    properties = ProjectProperties()
    zoom_admin_account = ZoomAdminAccount(
        api_key=properties.ZOOM_ACCOUNT_API_KEY,
        api_secret=properties.ZOOM_ACCOUNT_API_SECRET
    )
    report = ZoomAttendanceReport(
        start_date=properties.START_DATE,
        end_date=properties.END_DATE,
        meeting_id=properties.MEETING_ID,
        zoom_admin_account=zoom_admin_account
    )
    meetings, report = report.get_report()
    xlsxwriter = xls_writer.XlsWriter(properties)
    xlsxwriter.write_meeting_report_into_xls(meetings, report)
    print('----- Script running end! ------')
