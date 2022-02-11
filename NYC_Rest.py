import sys
import requests

class NYC_Rest_API:
    def __init__(self):
        pass
    def arrival_times(self, id: str) -> list:
        api_call = "http://mtaapi.herokuapp.com/api?id=" + id
        res = requests.get(api_call)
        if not res.ok:
            times = [-1]
        times = res.json()["result"]["arrivals"]
        return times
    

api = NYC_Rest_API()
print(len(api.arrival_times("120S")))