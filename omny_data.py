from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import re
from station_coords_parse import Station_Coords
from requests_html import HTMLSession
import json

#utilize https://rapidapi.com/mimouncadosch/api/nyc-subway-data/
#to get data for all stations

#url = "https://community-nyc-subway-data.p.rapidapi.com/api"
#url = "mtaapi.herokuapp.com/api?id=120S"

url = "https://community-nyc-subway-data.p.rapidapi.com/api"

querystring = {"id":"A38S"}

headers = {
    'x-rapidapi-host': "community-nyc-subway-data.p.rapidapi.com",
    'x-rapidapi-key': "29ee4e550fmsh06a9d49c4f34284p18e61cjsn43a8cb2cc768"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)

dictionary = json.loads(response.text)
print(response.text)
print(len(dictionary['result']['arrivals']))

coords = Station_Coords("stationCords.csv")

#manual data entry of lines
lines = {'8 Avenue Express': 'A', '6 Avenue Express': 'B', '8 Avenue Local': 'C',
         '6 Avenue Express': 'D', '8 Avenue Local': 'E', 
         'Queens Blvd Express/ 6 Av Local': 'F','Brooklyn F Express': 'F Express',
         'Brooklyn-Queens Crosstown': 'G', 'Nassau St Local': 'J',  
         '14 St-Canarsie Local': 'L', 'Queens Blvd Local/ 6 Av Local': 'M',
         'Broadway Local': 'N', 'Broadway Express': 'Q', 'Broadway Local': 'R',
         'Broadway Local': 'W', 'Nassau St Express': 'Z', 
         '1': 'Broadway - 7 Avenue Local', '2': '7 Avenue Express', 
         '3': '7 Avenue Express', '4': 'Lexington Avenue Express', 
         '5': 'Lexington Avenue Express', '6': 'Lexington Avenue Local', 
         '6 Express': 'Pelham Bay Park Express', '7': 'Flushing Local', 
         '7 Express': 'Flushing Express'}

iterate_lines(lines)
driver.close()