import csv
from decimal import *

#use to parse station_coords.csv
#class structure to use in other files
#some apis use alternate id, that is the reason for file 2
class Station_Coords:
    def __init__(self, file_1: str, file_2: str):
        self.file_1 = file_1
        self.file_2 = file_2
        #parse the first file
        self.station_data = list()
        self.index_map = dict()
        self.alt_index_map = dict()
        with open(file_1, "r") as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)
            index = 0
            for row in csv_reader:
                name = row[2]
                point = row[3].replace('POINT (', '')
                point = point.replace(')', '')
                point = point.split(' ')
                lat = float(point[1])
                lon = float(point[0])
                lines = list(row[4].split('-'))
                self.station_data.append([name, (lat,lon), lines])
                if name in self.index_map:
                    self.index_map[name].append((index, lines))
                else:
                    self.index_map[name] = [(index, lines)]
                index += 1
        with open(file_2, "r") as file: 
            csv_reader = csv.reader(file)
            header = next(csv_reader)
            i = 0
            for row in csv_reader:
                if i % 3 == 0:
                    alt_id = row[0]
                    n = row[1]
                    lat = float(row[2])
                    lon = float(row[3])
                    temp_tuple = self.find_station_index(alt_id, lat, lon)
                    index = temp_tuple[0]
                    name = temp_tuple[1]
                    lines = temp_tuple[2]
                    if(index > -1):
                        self.station_data[index].append(alt_id)
                        self.alt_index_map[alt_id] = [(index, lines, name)]          
                i+= 1
            j = 0
            i = 0
            for i in range(len(self.station_data)):
                if len(self.station_data[i]) < 4:
                    j+=1
            print(f"num less than 3: {j}")

    def dist(self, lat1: float, lon1: float, lat2: float, lon2: float):
        return ((lat2-lat1)**2 + (lon2-lon1)**2)**.5

    #given a station and a line, return station id
    def get_station_id(self, station: str, line: str) -> int:
        stations = self.index_map[station]
        #same name stations are on different lines
        for s in stations: 
            if line in s[1]:
                return s[0]
        return -1

    #given lat and lon return index
    def find_station_index(self, name: str, lat: float, lon: float) -> int:
        EPSILON = 0.0005
        to_return = 1
        min_dist = 1000
        temp_name = ""
        l = []
        for i in range(len(self.station_data)):
            station = self.station_data[i]
            if len(station) < 4:
                temp_lat = float(station[1][0])
                temp_lon = float(station[1][1])
                n = station[0]
                lines = station[2]
                temp_dist = self.dist(lat, lon, temp_lat, temp_lon)
                if temp_dist < min_dist:
                    min_dist = temp_dist
                    to_return = i
                    temp_name = n
                    l = lines
                    # print(f"name: {name}, found_station: {n}")
                    # print(f"lat1: {lat}, lat2: {temp_lat}, lon: {lon}, lat2: {temp_lon}")
        return (to_return, temp_name, l)

        #given an alt_id, e.x 119S, return the tuple(index, lines, name)
    def get_station_by_alt_id(self, alt_id: str):
        dir = alt_id[len(alt_id)-1]
        alt_id = alt_id[:len(alt_id)-1]
        station = self.alt_index_map[alt_id]
        return station

    #given an alt_id, e.x. 119S, return the index, 158
    def get_index_by_alt_id(self, alt_id: str) -> int:
        station = self.get_station_by_alt_id(alt_id)
        return station[0][0]

    #given an alt_id, e.x 119S, return the station name, "103rd St"
    def get_name_by_alt_id(self, alt_id: str) -> str:
        station = self.get_station_by_alt_id(alt_id)
        return station[0][2]

    def create_csv(self):
        print(self.station_data[0])
        f = open('master_data.csv', 'w', newline='')
        writer = csv.writer(f)
        writer.writerow(['Name', '(Latitude, Longitude)', 'Lines','Alternate ID'])
        for row in self.station_data:
            writer.writerow(row)

#alt_id map format as follows (index, lines, name)

sc = Station_Coords("stationCords.csv", "stop_locations.csv")
print(f"index: {sc.get_index_by_alt_id('119S')}")
print(f"name: {sc.get_name_by_alt_id('119S')}")
sc.create_csv()