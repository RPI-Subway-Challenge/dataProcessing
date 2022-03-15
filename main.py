from knn import KNN
from station_coords_parse import Station_Coords
from google_dir import Google_API

#coords = [(-80,40), (-79,41), (-71, 44), (-72,45)]

sc = Station_Coords("stationCords.csv", "stop_locations.csv")

coords = sc.get_all_coords()
print(len(coords))

cv = KNN(coords)
buckets = cv.find_knn(n_neighbors=250)

google = Google_API()

filename = "walking_distance.txt"
total = 0
with open(filename, 'w') as file:
    for bucket in buckets:
    #output file 
    #index_1, index_2, seconds
        if len(bucket) > 1:
            total += len(bucket)
            print(total)
            for i in range(0, len(bucket) - 1):
                station_i = bucket[i]
                index_i = sc.get_index_from_coord(station_i)

                for j in range(1, len(bucket)):
                    station_j = bucket[j]
                    index_j = sc.get_index_from_coord(station_j)

                    s = google.find_walking_seconds(station_i, station_j)
                    print(f"{index_i}, {index_j}, {s}", file=file)
                    #print(f"station 1: {sc.station_data[index_i][0]}, station2: {sc.station_data[index_j][0]}")

