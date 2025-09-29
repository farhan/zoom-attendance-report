import json


class Configuration:
    def __init__(self):
        f = open('configuration.json')
        json_data = json.load(f)
        self.ZOOM_ACCOUNT_ID = json_data['zoom_account']['account_id']
        self.ZOOM_ACCOUNT_CLIENT_ID = json_data['zoom_account']['client_id']
        self.ZOOM_ACCOUNT_CLIENT_SECRET = json_data['zoom_account']['client_secret']
        self.MEETING_ID = json_data['meeting']['meeting_id']
        self.START_DATE = json_data['meeting']['start_date']
        self.END_DATE = json_data['meeting']['end_date']
        self.UTC_TIME_DIFFERENCE = float(json_data['meeting']['utc_time_diff_hours'])
        self.MIN_MINUTES_FOR_ATTENDANCE = float(json_data['meeting']['minimum_minutes_for_attendance'])
