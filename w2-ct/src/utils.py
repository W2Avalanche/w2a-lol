import json

class Configuration:
    def __init__(self, **kwargs):
        self.url = kwargs.get('url')
        self.url_tournament = kwargs.get('url_tournament')
        self.url_team = kwargs.get('url_team')
        self.url_tournaments = kwargs.get('url_tournaments')
        self.riot_region = kwargs.get('riot_region')
        self.riot_api = kwargs.get('riot_api')
        self.w2_user = kwargs.get('w2_user')
        self.w2_password = kwargs.get('w2_password')
        self.w2_url = kwargs.get('w2_url')

def read_config(config_file_path) -> Configuration:
    configuration = open(config_file_path, 'r')
    config : Configuration = json.loads(configuration.read())
    return Configuration(**config)