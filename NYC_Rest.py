import sys
import requests

class NYC_Rest_API:
    def __init__(self):
        pass
    def arrival_times(self, id: str) -> list:
        api_call = "http://mtaapi.herokuapp.com/api?id=" + str(id)
        res = requests.get(api_call)
        times = []
        if not res.ok:
            times = [-1]
        #print(res.text)
        if res.json()["result"] != "key not found": 
            times = res.json()["result"]["arrivals"]
            times.sort()
        else:
            print("key not found")
        return times
    
'''#sample usage
api = NYC_Rest_API()
print(len(api.arrival_times("120S")))
'''