from .service import BaseService
class RiotAPI(BaseService):
    def __init__(self, token: str, region: str) -> None:
        self.token = token
        self.region = region
        pass
    def get_riot_id(self, lol_nick):
        response = self._get_request(web= "https://{}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}".format(self.region, lol_nick), 
                                     header={"X-Riot-Token": self.token})
        if response.ok:
            return(response.json()["puuid"])
        else:
            return None
        