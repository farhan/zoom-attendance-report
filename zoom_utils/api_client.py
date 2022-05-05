import json

import jwt
import requests

from zoom_utils import status
from zoom_utils.constants import ZoomAPIEndpoint
import logging as logger


class ZoomAPIClient(object):
    """
    Helper class to consume Zoom API endpoints
    """
    VERSION = 'v2'
    BASE_URL = 'https://api.zoom.us/' + VERSION
    TOKEN_EXPIRY = '1496091963999'

    def __init__(self, zoom_admin_account):
        """Zoom API Client init"""
        self._zoom_admin_account = zoom_admin_account
        self._token = self._create_jwt()

    def _create_jwt(self):
        """Generate a new token against key and secret"""
        self._token = jwt.encode({
            'iss': self._zoom_admin_account.api_key, 'exp': self.TOKEN_EXPIRY
        }, self._zoom_admin_account.api_secret, algorithm='HS256')

        return self._token

    def _get_request_header(self):
        """Add generated token as a header for authorization"""
        return {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer' + self._token,
        }

    def _send_request(self, http_method, endpoint, data, headers=None, **kwargs):
        """Send request"""
        url = self.BASE_URL + endpoint
        request_headers = self._get_request_header()
        if headers:
            request_headers = dict(request_headers, **headers)
        response = requests.request(
            http_method, url, headers=request_headers, data=data, params=kwargs.get('query_args', {})
        )

        print(u'Zoom API Request: {} - {}.'.format(url, data))
        print(u'Zoom API Response: {} - {}.'.format(response.status_code, response.text))

        # Regenerate token in case of expiry
        if response.status_code == status.HTTP_401_UNAUTHORIZED and not kwargs.get('jwt_renewed'):
            self._create_jwt()
            return self._send_request(
                http_method, endpoint, data, jwt_renewed=True, query_args=kwargs.get('query_args', {})
            )

        if status.is_success(response.status_code):
            return json.loads(response.text) if response.text else {}
        elif response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
            logger.error('Zoom - Got 429 status code. Zoom api limit has reached. {}'.format(response.text or ''))
        else:
            logger.error('Zoom - API error occurred. {}'.format(response.text or ''))

        return {}

    def get_participant_report(self, meeting_id):
        """ Get participant report """
        endpoint = ZoomAPIEndpoint.MEETING_PARTICIPANT_REPORT.format(meeting_id=meeting_id)
        query_args = {
            'page_size': 300
        }
        response = self._send_request('GET', endpoint, {}, query_args=query_args)
        participant = response.get('participants', [])
        while response.get('next_page_token'):
            query_args['next_page_token'] = response.get('next_page_token')
            response = self._send_request('GET', endpoint, {}, query_args=query_args)
            participant.extend(response.get('participants', []))
        return participant

    def get_meeting_instances(self, meeting_id):
        """Get past meeting instances UUID's"""
        endpoint = ZoomAPIEndpoint.GET_MEETINGS_INSTANCES.format(meeting_id=meeting_id)
        return self._send_request('GET', endpoint, {})
