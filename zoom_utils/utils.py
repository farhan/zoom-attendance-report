import urllib.parse
from datetime import timedelta, datetime

from zoom_utils.constants import DATE_TIME_FORMAT, DATE_FORMAT


def get_double_encoded_uuid(uuid):
    encoded_uuid = urllib.parse.quote(uuid)
    return urllib.parse.quote(encoded_uuid)


def to_date_time(utc_time_difference, date_time_str):
    date_time = datetime.strptime(date_time_str, DATE_TIME_FORMAT)
    return date_time + timedelta(hours=utc_time_difference)


def to_date(utc_time_difference, date_time_str):
    date_time = datetime.strptime(date_time_str, DATE_FORMAT)
    return date_time + timedelta(hours=utc_time_difference)
