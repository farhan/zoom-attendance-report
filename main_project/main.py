from csv_writer import csv_writer
from main_project.properties import ProjectProperties
from zoom_utils.models import ZoomAdminAccount
from zoom_utils.zoom_report import ZoomMeetingReport

if __name__ == '__main__':
    print('Hi!')
    properties = ProjectProperties()
    zoom_admin_account = ZoomAdminAccount(
        api_key=properties.ZOOM_ACCOUNT_API_KEY,
        api_secret=properties.ZOOM_ACCOUNT_API_SECRET
    )
    report = ZoomMeetingReport(
        start_date=properties.START_DATE,
        end_date=properties.END_DATE,
        meeting_id=properties.MEETING_ID,
        zoom_admin_account=zoom_admin_account
    )
    report_dict = report.get_report()
    print(report_dict)
    csv_writer.write_meeting_report_into_csv(properties, report_dict)
    print('----- Bye! ------')
