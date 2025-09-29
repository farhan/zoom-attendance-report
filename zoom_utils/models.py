class ZoomAdminAccount(object):
    """ Model to hold Zoom Admin Account info """

    def __init__(self, api_key, api_secret, account_id):
        self.api_key = api_key
        self.api_secret = api_secret
        self.account_id = account_id
