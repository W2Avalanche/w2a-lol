import json

class Configuration:
    def __init__(self, **kwargs):
        self.database_host = kwargs.get('db_host')
        self.database_port = kwargs.get('db_port')
        self.database_name = kwargs.get('db_name')
        self.database_user = kwargs.get('db_user')
        self.database_password = kwargs.get('db_password')
        self.auth_secret = kwargs.get('auth_secret')

def read_config(config_file_path) -> Configuration:
    configuration = open(config_file_path, 'r')
    config : Configuration = json.loads(configuration.read())
    return Configuration(**config)