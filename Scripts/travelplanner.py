from graph import Graph
from geopy.geocoders import Nominatim
from time import sleep

class Travelplanner:
    def __init__(self, distance_based=True, mode: int=0):
        self.distance_based = distance_based
        self.spots = []
        self.adress = []
        self.start = None
        self.end = None
        self.geolocator = Nominatim(user_agent="my_geocoder")
        if 0 <= mode <= 2:
            self.mode = mode
        else:
            raise Exception (f"{mode} is out of range for 0-2")
        self.profile = ["auto", "pedestrian", "bicycle"]
        self.g = None
    
    def location(self, adress: str):
        sleep(1)
        location = self.geolocator.geocode(adress)
        if location:
            return [location.latitude, location.longitude]
        else:
            raise Exception("No location found")

    def change_spot(self, i, adress: str):
        l = len(self.spots)
        if  l == 0 or l <= i:
            raise Exception("Index out of Bounds")
        else:
            self.spots[i] = self.location(adress)
    
    def add_spot(self, adress: str):
        self.spots.append(self.location(adress))
        self.adress.append(adress)
    
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
    
    def calculate(self, plot=False):
        g = Graph(self.spots, self.distance_based, self.profile[self.mode])
        shortest_path, length = g.shortest_path(self.start, self.end)
        if plot:
            print('Best Path:')
            g.printL(shortest_path)
            print(length)
            self.print_order(shortest_path)
            self.plot_map(shortest_path)
        return shortest_path, length
    
    def print_order(self, path):
        s='Recommended route\n'
        for i in path:
            s+=f"{self.adress[i]}: {self.spots[i]}\n"
        print(s)
        