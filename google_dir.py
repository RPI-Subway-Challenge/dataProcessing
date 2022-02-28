import requests
import json
import pprint
import config
from config import API_KEY

request_url = "https://maps.googleapis.com/maps/api/directions/json?"
#lat and long are flipped in stationCords.csv
origin = "origin=40.85902199892482, -73.93417999964333"
dest = "destination=40.851694999744616, -73.93796900205011"

request_url = request_url + origin + "&" + dest + "&travel_mode=WALKING" + "&key=" + API_KEY
test_url = "https://maps.googleapis.com/maps/api/directions/json?origin=Brooklyn&destination=Queens&mode=transit&key="
test_url = test_url + API_KEY

payload = {}
headers = {}

response = requests.request("GET", request_url, headers=headers, data=payload)

print(response.text)