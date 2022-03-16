class ZoomAdminAccount(object):
    """ Model to hold Zoom Admin Account info """

    def __init__(self, api_key, api_secret, jwt_token=None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.jwt_token = jwt_token
