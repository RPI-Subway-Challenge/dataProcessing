from NYC_Rest import NYC_Rest_API
from station_coords_parse import Station_Coords

api = NYC_Rest_API()
sc = Station_Coords("stationCords.csv", "stop_locations.csv")

i = 0
for i in range(len(sc.station_data)):
    #station is [name, (lat, lon), lines, alt_id]
    station = sc.station_data[i]
    print(f"name: {station[0]}")
    N_times = api.arrival_times(str(station[3])+'N')
    S_times = api.arrival_times(str(station[3])+'S')
    sc.station_data[i].append(N_times)
    sc.station_data[i].append(S_times)
    # print(f"N_Arrivals: {str(len(N_times))}")
    # print(f"S_Arrivals: {str(len(S_times))}")

sc.create_csv()