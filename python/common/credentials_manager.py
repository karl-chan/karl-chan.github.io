import json
import os
import common.path_manager as pathmgr


class CredentialsManager:
    ''' Reads in credentials in the /data folder as json objects '''
    tfl_credentials = None
    mysql_credentials = None

    def __init__(self):
        credentials_dir = pathmgr.PathManager().get_credentials_dir()

        tfl_credentials_path = os.path.join(credentials_dir, 'tflCredentials.json')
        with open(tfl_credentials_path, 'r') as f:
            self.tfl_credentials = json.load(f)

        mysql_credentials_path = os.path.join(credentials_dir, 'mysqlCredentials.json')
        with open(mysql_credentials_path, 'r') as f:
            self.mysql_credentials = json.load(f)

    def get_tfl_credentials(self):
        return self.tfl_credentials

    def get_mysql_credentials(self):
        return self.mysql_credentials
