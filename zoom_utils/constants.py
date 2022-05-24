import os
from enum import Enum

DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
DATE_FORMAT = '%Y-%m-%d'
# Environment Variable
ENV_ZOOM_API_TOKEN_EXPIRY = os.getenv('ZOOM_API_TOKEN_EXPIRY', default='1496091963999')


class ZoomAPIEndpoint(Enum):
    """Zoom API Endpoints"""
    GET_MEETING = '/meetings/{meeting_id}'
    MEETING_PARTICIPANT_REPORT = '/report/meetings/{meeting_id}/participants'
    GET_MEETINGS_INSTANCES = '/past_meetings/{meeting_id}/instances'
