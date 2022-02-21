from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import re
from station_coords_parse import Station_Coords
import json
import sys


sys.stdout = open("line_data.txt", "w")

coords = Station_Coords("stationCords.csv", "stop_locations.csv")

#manual data entry of lines
lines ={'1': 3, '2': 3,'3': 1,'4': 1,'5': 3,'6': 2,'7': 2, 'A': 3, 
        'B': 1, 'C': 1, 'D': 1, 'E': 3, 'F': 1, 'G': 1, 'J': 2,
        'L': 1, 'M': 1, 'N': 1, 'Q': 3, 'R': 3, 'Z': 2}
line_names = {'8 Avenue Express': 'A', '6 Avenue Express': 'B', '8 Avenue Local': 'C',
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

op = webdriver.ChromeOptions()
op.add_argument('headless')

PATH = "C:\Program Files (x86)\chromedriver.exe" #path on your machine
driver = webdriver.Chrome(PATH, options=op)

metro_url = "https://metro.fandom.com/wiki/Route_2_(New_York_City_Subway)"
driver.get(metro_url)

def process_string(string: str):
    string = string.replace('\n', '')
    string = string.replace('Avenue', 'Ave')
    string = string.replace ('Street', 'St')
    string = string.replace ('Third', '3rd')
    string = string.replace ('–', '-')
    string = string.replace ('- 110th St', '(110th St)')
    string = string.replace('Parkway', 'Pkwy')
    string = string.replace('Center', 'Ctr')
    string = string.replace('Square', 'Sq')
    string = string.replace('Place', 'Pl')
    string = string.replace('Road', 'Rd')
    string = string.replace('East', 'E')
    string = string.replace('West', 'W')
    return string

def get_alt(alt: str):
    return '//img[@alt="' + alt + '"]'

def get_url(line: str):
    return 'https://metro.fandom.com/wiki/Route_' + line + '_(New_York_City_Subway)'

def iterate_line(line: str, td_num: int):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    table = soup.find_all('table', {'class': 'wikitable'})[2]
    rows = table.find_all('tr')
    for row in rows[1:]:
        tds = row.find_all('td')
        found_link = False

        td = tds[td_num]
        station = ""
        if len(td.find_all('a')) > 0:
            if td.find('a').text != "":
                found_link = True
                station = process_string(td.find('a').text)
        elif len(td.find_all('span')) > 0:
            if td.find('span').text != "":
                found_link = True
                station = process_string(td.find('span').text)
        if not found_link:
            if len(row.find_all('th')) > 0:
                th = row.find('th')
                if th.text != "\n" and th.text != "":
                    station = process_string(th.text)
        index = coords.get_station_id(station, line)
        if index > -1:
            print(f"station name: {station}, index: {index}")
        



def iterate_lines(lines: list):
    line_names = list(lines.keys())
    for i in range(len(line_names)):
        line = line_names[i]
        td_num = lines[line]
        driver.get(get_url(line))
        print(f"Line: {line}")
        iterate_line(line, td_num)
        print("")

iterate_lines(lines)

driver.close()