import csv
import json
from station_coords_parse import Station_Coords 

sc = Station_Coords("stationsCords.csv", "stop_locations.csv")

file = open('data.txt')

csvreader = csv.reader(file)

#key is station
#val is dict: key is "lineN/S", val is array of times
data = {}

header = next(csvreader)
print(header)

for row in csvreader: 
    #trip id
    trip_id = row[0]
    trip = trip_id.split('..')
    if "Weekday" in trip[0] and len(trip) > 1:
        line = trip[0][len(trip[0])-1]
        #print(trip[1])
        direction = trip[1][0]
        #print(f"line: {line}")
        #print(f"Direction: {direction}")
        line_dir = line+ "_" + direction
        #time
        time = row[1]
        #station id
        alt_id = row[3]
        id = sc.get_index_by_alt_id(alt_id)
        if id >= 0:
            if id not in data:
                data[id]= {}
                data[id][line_dir] = [time]
            else:
                if line_dir in data[id]:
                    data[id][line_dir].append(time)
                else:
                    data[id][line_dir] = [time]

with open("times.json", "w") as output:
    json.dump(data, output)