import json
import logging
import time

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

    def __init__(self, zoom_admin_account):
        """Zoom API Client init"""
        self._zoom_admin_account = zoom_admin_account
        self._access_token = None
        self._token_expires_at = 0
        self._api_url = None

    def _get_oauth2_token(self):
        """Get OAuth2 access token using account credentials"""
        if self._access_token and time.time() < self._token_expires_at:
            return self._access_token
            
        response = requests.post(
            "https://zoom.us/oauth/token",
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={
                'grant_type': 'account_credentials',
                'account_id': self._zoom_admin_account.account_id
            },
            auth=(self._zoom_admin_account.client_id, self._zoom_admin_account.client_secret),
            timeout=30
        )
        
        if response.status_code == 200:
            token_data = response.json()
            self._access_token = token_data['access_token']
            self._api_url = token_data.get('api_url', 'https://api.zoom.us')
            # Set expiration time (subtract 60 seconds for safety margin)
            self._token_expires_at = time.time() + token_data['expires_in'] - 60
            return self._access_token
        else:
            logger.error(f'OAuth2 token request failed: {response.status_code} - {response.text}')
            raise Exception(f'Failed to get OAuth2 token: {response.status_code}')

    def _get_request_header(self):
        """Add OAuth2 token as a header for authorization"""
        token = self._get_oauth2_token()
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}',
        }

    def _send_request(self, http_method, endpoint, data, headers=None, **kwargs):
        """Send request"""
        # Use the API URL from OAuth2 response, fallback to default
        base_url = self._api_url or 'https://api.zoom.us'
        url = f"{base_url}/{self.VERSION}{endpoint}"
        
        request_headers = self._get_request_header()
        if headers:
            request_headers = dict(request_headers, **headers)
        response = requests.request(
            http_method, url, headers=request_headers, data=data, params=kwargs.get('query_args', {})
        )

        logging.info(u'Zoom API Request: {} - {}.'.format(url, data))
        logging.info(u'Zoom API Response: {} - {}.'.format(response.status_code, response.text))

        # Regenerate token in case of expiry
        if response.status_code == status.HTTP_401_UNAUTHORIZED and not kwargs.get('token_renewed'):
            # Force token refresh by clearing current token
            self._access_token = None
            self._token_expires_at = 0
            return self._send_request(
                http_method, endpoint, data, token_renewed=True, query_args=kwargs.get('query_args', {})
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
        endpoint = ZoomAPIEndpoint.MEETING_PARTICIPANT_REPORT.value.format(meeting_id=meeting_id)
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
        endpoint = ZoomAPIEndpoint.GET_MEETINGS_INSTANCES.value.format(meeting_id=meeting_id)
        return self._send_request('GET', endpoint, {})
