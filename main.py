from nyct_gtfs import NYCTFeed
import config 
import csv

#location_status = 'STOPPED_AT', 'INCOMING_AT', 'IN_TRANSIT_TO'
class Live_Feed:
    def __init__(self):
        self.feed = NYCTFeed("A", config.MTA_API)
        #parse stop_locations.csv
        self.id_map = {}
        with open("stop_locations.csv", "r") as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)
            for row in csv_reader:
                self.id_map[row[0]] = row[1]

    def train_status(self, line: str, station: str, status: str):
        self.feed = NYCTFeed(line, config.MTA_API)
        self.feed.refresh()
        trains = self.feed.trips

        incoming_trains = set()

        for train in trains:
            if train.location_status == status \
                and train.route_id == line \
                and self.id_map[train.stop_time_updates[0].stop_id] == station:
                incoming_trains.add(train)
        return incoming_trains

    #given a station on a line return all trains in transit to station
    #stopped at the station or incoming to the station
    #returns tuples of status and direction
    def trains_to_station(self, line:str, station: str):
        self.feed = NYCTFeed(line, config.MTA_API)
        self.feed.refresh()
        trains = self.feed.trips

        incoming_trains = set()

        for train in trains:
            if train.route_id == line and \
                self.id_map[train.stop_time_updates[0].stop_id] == station:
                incoming_trains.add((train.location_status, train.direction))
        return incoming_trains


lf = Live_Feed()
s = lf.trains_to_station("7", "Grand Central-42 St")
print(s)


