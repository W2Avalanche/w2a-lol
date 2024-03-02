import requests

class RequestType:
    GET_TOURNAMENTS = 'get-tournaments'
    GET_TOURNAMENT = 'get-tournament'
    GET_TEAM = 'get-team'

class CircuitoTormentaAPI():
    def __init__(self, tournament_url: str = None, team_url: str = None, tournaments_url: str = None):
        self.REQUESTS_URLS = {
            RequestType.GET_TOURNAMENTS: tournaments_url,
            RequestType.GET_TOURNAMENT: tournament_url,
            RequestType.GET_TEAM: team_url 
        }
    def get_team(self, slug):
        response = self._get_request(web= self._api_url(request=RequestType.GET_TEAM, id= slug))
        if response.json()['status'] == 'success': return response.json()['returnData']
        else: return None

    def get_tournament(self, slug): 
        response = self._get_request(web= self._api_url(request=RequestType.GET_TOURNAMENT, id= slug))
        if response.json()['status'] == 'success': return response.json()['returnData']["torneo"]
        else: return None

    def get_teams_from_tournament(self, slug):
        tournament_data = self.get_tournament(slug=slug)
        if not tournament_data: return None
        return tournament_data['equipos']

    def get_tournaments(self):
        response = self._get_request(web= self._api_url(request=RequestType.GET_TOURNAMENTS))
        if response.json()['status'] == 'success': return response.json()['returnData']
        else: return None

    def _api_url(self, request: RequestType, id: str = '') -> str:
        return "https://api.circuitotormenta.com//{}".format(self.REQUESTS_URLS[request].format(id))

    def _post_request(self, web, header, data) -> requests.Response:
        return requests.post(web, headers= header, json=data)

    def _get_request(self, web, header = None) -> requests.Response:
        return requests.get(web, headers= header)
    
