class ZoomAdminAccount(object):
    """ Model to hold Zoom Admin Account info """

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

