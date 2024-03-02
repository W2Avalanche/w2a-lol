import requests
class BaseService():
    def _post_request(self, web, header = None, json = None, data = None) -> requests.Response:
        return requests.post(web, headers= header, json=json, data= data)

    def _get_request(self, web, header = None) -> requests.Response:
        return requests.get(web, headers= header)
    
