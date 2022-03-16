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
        meeting_name=properties.MEETING_NAME,
        zoom_admin_account=zoom_admin_account
    )
    print(report.get_report())
