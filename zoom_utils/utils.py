import urllib.parse


def get_double_encoded_uuid(uuid):
    encoded_uuid = urllib.parse.quote(uuid)
    return urllib.parse.quote(encoded_uuid)
