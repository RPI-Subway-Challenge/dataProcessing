import requests
import json
import pprint
import config
from config import API_KEY

class Google_API:
    def __init__(self):
        self.request_url = "https://maps.googleapis.com/maps/api/directions/json?"
#lat and long are flipped in stationCords.csv

    def find_walking_seconds(self, coord_1: tuple, coord_2: tuple) -> int:
        origin = "origin=" + str(coord_1[1]) + ', ' + str(coord_1[0])
        dest = "destination=" + str(coord_2[1]) + ', ' + str(coord_2[0])
        
        req = self.request_url + origin + "&" + dest + "&travel_mode=WALKING" + "&key=" + API_KEY
        payload = {}
        headers = {}

        response = requests.request("GET", req, headers=headers, data=payload)
        res = response.json()

        seconds = res["routes"][0]["legs"][0]["duration"]["value"]
        return seconds