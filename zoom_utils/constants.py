DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
DATE_FORMAT = '%Y-%m-%d'


class ZoomAPIEndpoint(object):
    """Zoom API Endpoints"""

    GET_MEETING = '/meetings/{meeting_id}'
    MEETING_PARTICIPANT_REPORT = '/report/meetings/{meeting_id}/participants'
    GET_MEETINGS_INSTANCES = '/past_meetings/{meeting_id}/instances'
