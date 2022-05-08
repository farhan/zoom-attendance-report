DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
DATE_FORMAT = '%Y-%m-%d'
DATE_TIME_DIFFERENCE_HOURS = -5
MIN_MINUTES_FOR_ATTENDANCE = 1


class ZoomAPIEndpoint(object):
    """Zoom API Endpoints"""

    GET_MEETING = '/meetings/{meeting_id}'
    MEETING_PARTICIPANT_REPORT = '/report/meetings/{meeting_id}/participants'
    GET_MEETINGS_INSTANCES = '/past_meetings/{meeting_id}/instances'
