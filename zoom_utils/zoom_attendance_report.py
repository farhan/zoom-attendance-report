from datetime import datetime

from zoom_utils import utils
from zoom_utils.api_client import ZoomAPIClient
from zoom_utils.constants import DATE_FORMAT
from zoom_utils.utils import get_double_encoded_uuid


class ZoomAttendanceReport:
    def __init__(self, start_date, end_date, meeting_id, zoom_admin_account, utc_time_diff):
        self.zoom_admin_account = zoom_admin_account
        self.start_date = datetime.strptime(start_date, DATE_FORMAT)
        self.end_date = datetime.strptime(end_date, DATE_FORMAT)
        self.end_date = self.end_date.replace(hour=23, minute=59)
        self.meeting_id = meeting_id
        self.utc_time_diff = utc_time_diff

    def get_report(self):
        zoom_client = ZoomAPIClient(self.zoom_admin_account)
        report = {}
        meetings = []
        meeting_instances = zoom_client.get_meeting_instances(self.meeting_id).get('meetings', [])
        for instance in meeting_instances:
            uuid = instance['uuid']
            if uuid.startswith('/'):
                uuid = get_double_encoded_uuid(uuid)
            meeting_start_date_time = instance['start_time']
            if self.start_date <= utils.to_date_time(self.utc_time_diff, meeting_start_date_time) <= self.end_date:
                meeting_participant_entries = zoom_client.get_participant_report(uuid)
                self.__get_report_of_a_meeting_users(meeting_participant_entries, meeting_start_date_time, report)
                meetings.append(meeting_start_date_time)
        return self.sort_data(meetings, report)

    def sort_data(self, meetings, report):
        meetings.sort()
        # Sort dictionary based on names, following method will return list of tuples having data (key, value)
        report = sorted(report.items(), key=lambda x: x[1]['name'])
        return meetings, report

    def __get_report_of_a_meeting_users(self, meeting_participant_entries, meeting_start_date_time, report):
        for entry in meeting_participant_entries:
            user_id = entry['id']

            if user_id not in report.keys():
                report[user_id] = self.__get_user_data(entry)
                report[user_id]['meetings_report'] = {}

            if meeting_start_date_time in report[user_id]['meetings_report'].keys():
                meeting_report = report[user_id]['meetings_report'][meeting_start_date_time]
                # TODO: Add duration only if it lies within the scheduled meeting time
                meeting_report['duration'] += entry['duration']
                meeting_report['entry_exit'] = '{},\n{}'.format(
                    meeting_report['entry_exit'],
                    self.__get_meeting_entry_exit_time(entry)
                )
            else:
                meeting_report = report[user_id]['meetings_report'][meeting_start_date_time] = {}
                meeting_report['duration'] = entry['duration']
                meeting_report['entry_exit'] = self.__get_meeting_entry_exit_time(entry)

    def __get_user_data(self, entry):
        fields = ['id', 'name', 'user_email']
        return {key: entry[key] for key in fields}

    def __get_meeting_entry_exit_time(self, entry):
        return '{} - {}'.format(
            utils.to_date_time(self.utc_time_diff, entry['join_time']),
            utils.to_date_time(self.utc_time_diff, entry['leave_time'])
        )
