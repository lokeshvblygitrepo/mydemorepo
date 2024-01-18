import hvac

class Keys(object):

    def __init__(self,url,secret):
        client = hvac.Client(url=url)
        client.secrets.kv.default_kv_version = '1'
        secret = client.secrets.kv.read_secret(secret)
        data = secret['data']
        self.bitbucket_username = data['bitbucket.username']
        self.bitbucket_password = data['bitbucket.password']
        self.qac_db_username = data['qac.db.username']
        self.qac_db_password = data['qac.db.password']


def get_keys():
    return Keys('http://127.0.0.1:8200', 'qa-automation')