#!/usr/bin/env python3
"""
Simple OAuth2 auth API test
Tests the auth API using credentials from configuration.json
"""

import json
import requests

def load_config():
    """Load configuration from configuration.json"""
    with open("configuration.json", 'r') as f:
        return json.load(f)

def test_auth_api():
    """Test OAuth2 auth API"""
    config = load_config()
    
    # Get credentials
    client_id = config['zoom_account']['api_key']
    client_secret = config['zoom_account']['api_secret']
    
    print(f"Testing with credentials: {client_id[:10]}...")
    
    # Make OAuth2 request
    response = requests.post(
        "https://zoom.us/oauth/token",
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data={
            'grant_type': 'client_credentials'
        },
        auth=(client_id, client_secret),
        timeout=30
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    return response.status_code == 200

if __name__ == "__main__":
    test_auth_api()
