import sys
import random

class KNN: 
    def __init__(self, coordinates: list):
        self.coords = coordinates
        #keep track of bucket num
        self.coord_map = {}
        #loop through all coords and find min_x, min_y, max_x, max_y
        self.min_x = 0
        self.max_x = -100
        self.min_y = 100
        self.max_y = 0
        for coord in self.coords:
            self.coord_map[coord] = -1
            if coord[0] < self.min_x:
                self.min_x = coord[0]
            if coord[0] > self.max_x:
                self.max_x = coord[0]
            if coord[1] < self.min_y:
                self.min_y = coord[1]
            if coord[1] > self.max_y: 
                self.max_y = coord[1]
    
    def dist(self, loc_1: tuple, loc_2: tuple):
        return ((loc_2[0] - loc_1[0])**2 + (loc_2[1] - loc_1[1])**2) ** 0.5

    #generate n random centers
    def random_centers(self, n_neighbors: int) -> list:
        centers = []
        for i in range(n_neighbors):
            x = random.uniform(self.min_x, self.max_x)
            y = random.uniform(self.min_y, self.max_y)
            centers.append((x,y))
        return centers

    def closest_center(self, loc: tuple, centers: list)-> tuple:
        closest = (0,0)
        min_dist = 1000
        for center in centers:
            temp_dist = self.dist(loc, center)
            if temp_dist < min_dist:
                closest = center
                min_dist = self.dist(loc, center)
        return closest

    #given a list of coordinates, generate center
    def generate_center(self, coords: list) -> tuple:
        total_x = 0
        total_y = 0
        for coord in coords:
            total_x += coord[0]
            total_y += coord[1]
        length = len(coords)
        if length == 0:
            return (0,0)
        return (total_x/ length, total_y / length)

    #returns n_neighbors groups of coordinates
    def find_knn(self, n_neighbors: int) -> list:
        centers = self.random_centers(n_neighbors)
        changes = 1
        buckets = [ [] for i in range(len(centers))]

        while changes > 0:
            changes = 0
            for coord in self.coords:
                new_center = centers.index(self.closest_center(coord, centers))
                current_center = self.coord_map[coord]
                if current_center != new_center:
                    if current_center > -1:
                        buckets[current_center].remove(coord)
                    buckets[new_center].append(coord)
                    changes += 1
                    self.coord_map[coord] = new_center
            #readjust the centers
            for i in range(len(centers)):
                centers[i] = self.generate_center(coords=buckets[i])
        #print(centers)

        return buckets

# coords = [(-80,40), (-79,41), (-71, 44), (-72,45), (-78.5, 43.2), (-69, 44), (-73, 43)]
# cv = KNN(coords)

# print(cv.find_knn(n_neighbors = 2))