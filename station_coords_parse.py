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
                lines = row[4].split('-')
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
                    temp_tuple = self.find_station_index(n, lat, lon)
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
        EPSILON = 0.001
        for i in range(len(self.station_data)):
            digits_lat = Decimal(str(lat))
            digits_lat = -1*digits_lat.as_tuple().exponent
            digits_lon = Decimal(str(lon))
            digits_lon = -1*digits_lon.as_tuple().exponent
            station = self.station_data[i]
            temp_lat = float(station[1][0])
            temp_lon = float(station[1][1])
            temp_lat = round(temp_lat, digits_lat)
            temp_lon = round(temp_lon, digits_lon)
            n = station[0]
            lines = station[2]
            if abs(lat - temp_lat) < EPSILON and abs(lon - temp_lon) < EPSILON \
                or name == station[0]:
                #print(f"name: {name}, found_station: {n}")
                return (i, n, lines)
        return (-1, "", lines)

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

#alt_id map format as follows (index, lines, name)

sc = Station_Coords("stationCords.csv", "stop_locations.csv")
print(f"index: {sc.get_index_by_alt_id('119S')}")
print(f"name: {sc.get_name_by_alt_id('119S')}")