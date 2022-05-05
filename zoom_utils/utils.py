import urllib.parse
from datetime import timedelta, datetime

from zoom_utils.constants import DATE_TIME_FORMAT, DATE_TIME_DIFFERENCE_HOURS


def get_double_encoded_uuid(uuid):
    encoded_uuid = urllib.parse.quote(uuid)
    return urllib.parse.quote(encoded_uuid)


def converted_date_time(date_time_str):
    date_time = datetime.strptime(date_time_str, DATE_TIME_FORMAT)
    return date_time - timedelta(hours=DATE_TIME_DIFFERENCE_HOURS)
