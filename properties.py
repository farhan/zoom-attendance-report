import json


class ProjectProperties:
    def __init__(self):
        f = open('properties.json')
        json_data = json.load(f)
        self.ZOOM_ACCOUNT_API_KEY = json_data['zoom_account']['api_key']
        self.ZOOM_ACCOUNT_API_SECRET = json_data['zoom_account']['api_secret']
        self.MEETING_ID = json_data['meeting']['meeting_id']
        self.START_DATE = json_data['meeting']['start_date']
        self.END_DATE = json_data['meeting']['end_date']
