#!/usr/bin/env python3
"""
Test the updated zoom_utils with OAuth2 authentication
"""

import sys
import os
import logging
import json
import requests

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from configuration import Configuration
from zoom_utils.models import ZoomAdminAccount
from zoom_utils.api_client import ZoomAPIClient

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_zoom_utils_oauth2():
    """Test the updated zoom_utils with OAuth2"""
    try:
        logger.info("🚀 Testing updated zoom_utils with OAuth2...")
        
        # Load configuration
        configuration = Configuration()
        
        # Create zoom admin account
        zoom_admin_account = ZoomAdminAccount(
            api_key=configuration.ZOOM_ACCOUNT_API_KEY,
            api_secret=configuration.ZOOM_ACCOUNT_API_SECRET
        )
        
        # Test OAuth2 token generation
        from zoom_utils.api_client import ZoomAPIClient
        api_client = ZoomAPIClient(zoom_admin_account)
        
        logger.info("✅ OAuth2 API client created successfully")
        
        # Test a simple API call
        try:
            user_info = api_client._send_request('GET', '/users/me', {})
            logger.info(f"✅ User info retrieved: {user_info}")
            return True
        except Exception as e:
            logger.error(f"❌ API call failed: {str(e)}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_zoom_utils_oauth2()
