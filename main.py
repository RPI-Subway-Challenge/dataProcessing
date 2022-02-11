from NYC_Rest import NYC_Rest_API
from station_coords_parse import Station_Coords

api = NYC_Rest_API()
sc = Station_Coords("stationCords.csv", "stop_locations.csv")

i = 0
for station in sc.station_data:
    #station is [name, (lat, lon), lines, alt_id]

    if len(station) > 3:
        #print(f"alt_id: {station[3]}")
        #print(f"i: {i}")
        i+=1
    else:
        print(f"name: {station[0]}, coords: {station[1][0]}, {station[1][1]}")