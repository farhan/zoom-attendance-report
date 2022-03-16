from zoom_utils.api_client import ZoomAPIClient
from zoom_utils.utils import get_double_encoded_uuid


class ZoomMeetingReport:
    def __init__(self, start_date, end_date, meeting_name, zoom_admin_account):
        self.zoom_admin_account = zoom_admin_account
        self.start_date = start_date
        self.end_date = end_date
        self.meeting_name = meeting_name

    def get_report(self):
        meeting_id = '88177466375'
        # meeting_id = '86345689524'
        zoom_client = ZoomAPIClient(self.zoom_admin_account)
        participants = []
        past_instances = zoom_client.get_meeting_instances(meeting_id).get('meetings', [])
        for instance in past_instances:
            # uuid = get_double_encoded_uuid(instance['uuid'])
            uuid = instance['uuid']
            zoom_participants = zoom_client.get_participant_report(uuid)
            participants += zoom_participants

        participants_duration = {}
        index = 0
        for participant in participants or []:
            user_email = participant.get('user_email') + '_' + str(index)
            if user_email in participants_duration.keys():
                participants_duration[user_email] += participant.get('duration', 0)
            else:
                participants_duration[user_email] = participant.get('duration', 0)
            index += 1
        return participants_duration
