# Zoom Attendance Report Utility Tool

## Project Description

A Utility Python Project to generate the attendance report of the Recurring Zoom meeting.
Project generates the report in the excel sheet.
Zoom portal doesn't provide the feature to generate the monthly report of the recurring zoom meeting.
This utility project can generate it on a click.

This project fetches the data from the Zoom apis.


## Configure the Project
Create `configuration.json` on root of project directory (in sibling of configurationc.py)
Add the appropriate values in the fields

```json
{
  "zoom_account": {
    "api_key": "ADD_API_KEY_HERE",
    "api_secret": "ADD_API_SECRET_HERE"
  },
  "meeting": {
    "meeting_id": "ADD_API_MEETING_ID_HERE",
    "start_date": "2022-01-01",
    "end_date": "2022-01-31",
    "minimum_minutes_for_attendance": "1",
    "utc_time_diff_hours": "+0.0"
  }
}
```
`api_key`, `api_secret`:
Follow the following document to create the api keys and secret against the zoom account.
It must be created from the Zoom account of the meeting host.
https://marketplace.zoom.us/docs/guides/build/oauth-app/

`meeting_id`: It's the id of the Zoom meeting, can be fetched from Zoom portal

`start_date`: Start date of the report

`end_date`: End date of the report

`minimum_minutes_for_attendance`: It's the minimum minutes required to mark the participant present in the meeting

`utc_time_diff_hours` : It's the difference of the time zone as compared to UTC. For example for New York it will be `-4.0` as New York Time zone is UTC-4

## Setup and Run the Project

#### Create the virtual environment
`python3 -m venv venv`

#### Activate the environment
`source venv/bin/activate`

#### Install the requirements
`pip install -r requirements.txt`

#### Run the project
`python main.py`
