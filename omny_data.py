from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import re
from station_coords_parse import Station_Coords
import json

coords = Station_Coords("stationCords.csv", "stop_locations.csv")

#manual data entry of lines
lines = {'A line': 'A', 'B line': 'B', 'C line': 'C'}
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

PATH = "C:\Program Files (x86)\chromedriver.exe" #path on your machine
driver = webdriver.Chrome(PATH)

omny_url = "https://omny.info/schedules/new-york-city-subway"
driver.get(omny_url)

def get_alt(alt: str):
    return '//img[@alt="' + alt + '"]'

def iterate_line(line: str, name: str):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    spans = soup.find_all('span')
    
    is_station = False
    for i in range(len(spans)):
        span = spans[i]
        if span.text == "New York City Subway":
            i+=1
            is_station = True
            span = spans[i]
        if span.text == "Save favorite":
            is_station = False
        if is_station and span.text != name:
            print(span.text)


def iterate_lines(lines: dict):
    names = list(line_names.keys())
    lines = list(lines.keys())
    for i in range(len(lines)):
        line = lines[i]
        name = names[i]
        link = driver.find_element(By.XPATH, get_alt(line))
        link.click()
        iterate_line(line, name)
        driver.back()
        print("")

iterate_lines(lines)

driver.close()