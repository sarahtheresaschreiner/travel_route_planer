from turtle import delay
from graph import Graph
from geopy.geocoders import Nominatim
from time import sleep

class Travelplanner:
    def __init__(self, distance_based=True, mode: int=0):
        self.distance_based = distance_based
        self.spots = []
        self.start = None
        self.end = None
        self.geolocator = Nominatim(user_agent="my_geocoder")
        if 0 <= mode <= 2:
            self.mode = mode
        else:
            raise Exception (f"{mode} is out of range for 0-2")
        self.profile = ["auto", "pedestrian", "bicycle"]
        self.g = None
    
    def location(self, address: str):
        sleep(1)
        location = self.geolocator.geocode(address)
        if location:
            return [location.longitude, location.latitude]
        else:
            raise Exception("No location found")

    def change_spot(self, i, address):
        l = len(self.spots)
        if  l == 0 or l <= i:
            raise Exception("Index out of Bounds")
        else:
            self.spots[i] = self.location(address)
    
    def add_spot(self, address: str):
        self.spots.append(self.location(address))
    
    def set_start(self, i):
        l = len(self.spots)
        if  l == 0 or l <= i:
            raise Exception("Index out of Bounds")
        else:
            self.start = i
    
    def set_end(self, i):
        l = len(self.spots)
        if  l == 0 or l <= i:
            raise Exception ("Index out of Bounds")
        else:
            self.end = i
    
    def calculate(self):
        g = Graph(self.spots, self.distance_based, self.profile[self.mode])
        print(g.to_string())
        shortest_path, length = g.shortest_path(self.start, self.end)
        print('Best Path:')
        g.printL(shortest_path)
        print(length)