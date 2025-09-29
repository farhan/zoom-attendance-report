class ZoomAdminAccount(object):
    """ Model to hold Zoom Admin Account info """

    def __init__(self, account_id, client_id, client_secret):
        self.account_id = account_id
        self.client_id = client_id
        self.client_secret = client_secret
