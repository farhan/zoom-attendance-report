from datetime import datetime

from zoom_utils.api_client import ZoomAPIClient


class ZoomMeetingReport:
    def __init__(self, start_date, end_date, meeting_id, zoom_admin_account):
        self.zoom_admin_account = zoom_admin_account
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d')
        self.meeting_id = meeting_id

    def get_report(self):
        zoom_client = ZoomAPIClient(self.zoom_admin_account)
        report = {}
        meeting_instances = zoom_client.get_meeting_instances(self.meeting_id).get('meetings', [])
        for instance in meeting_instances:
            # TODO: double encode the uuid
            # uuid = get_double_encoded_uuid(instance['uuid'])
            uuid = instance['uuid']
            meeting_start_date_time = datetime.strptime(instance['start_time'], '%Y-%m-%dT%H:%M:%SZ')
            if self.start_date <= meeting_start_date_time <= self.end_date:
                meeting_participant_entries = zoom_client.get_participant_report(uuid)
                report[str(meeting_start_date_time)] = self.get_report_of_a_meeting_users(meeting_participant_entries)

        return report

    def get_report_of_a_meeting_users(self, meeting_participant_entries):
        user_records = {}
        for entry in meeting_participant_entries:
            user_id = entry['id']
            if user_id in user_records.keys():
                user_records[user_id]['duration'] += entry.get('duration', 0)
                user_records[user_id]['entry_exit'] = '{} + {}'.format(
                    user_records[user_id]['entry_exit'],
                    self.get_meeting_entry_exit_time(entry)
                )
            else:
                fields = ['id', 'name', 'user_email', 'duration']
                user_records[user_id] = {key: entry[key] for key in fields}
                user_records[user_id]['entry_exit'] = self.get_meeting_entry_exit_time(entry)
        return user_records

    def get_meeting_entry_exit_time(self, entry):
        return '{} - {}'.format(entry['join_time'], entry['leave_time'])
