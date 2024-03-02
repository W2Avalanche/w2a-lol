import requests
from .service import BaseService
from ..schemas.team import Team
class W2API(BaseService):
    def __init__(self, user: str, password: str, url: str) -> None:
        self.user = user
        self.password = password
        self.url = url
        self.token = self.login()
    
    def login(self):
        response:  requests.Response = self._post_request(web=self.url + "/token", data={
            "username": self.user,
            "password": self.password,
            "grant_type": "",
            "scope":"",
            "client_id": "",
            "client_secret":""
        
            })
        if response.ok:
            return response.json()["access_token"]
        else:
            raise Exception("Unable to loggin")
    
    def create_team(self, team: Team):
        response: requests.Response = self._post_request(web=self.url + "/team", 
                                                         header={"Authorization": "Bearer {}".format(self.token),
                                                                 "Content-Type":"application/json"}, 
                                                         json=team.model_dump(exclude_none=True))
        if response.ok:
            return response.json()
        else:
            raise Exception(response.json())