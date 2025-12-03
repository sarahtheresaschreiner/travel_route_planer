from json.encoder import INFINITY
from sysconfig import get_path
from node import Node
from routingpy import Valhalla

class Graph:
    def __init__(self, spots, distance_based, profile):
        self.profile = profile
        self.nodes = spots                                  # list/dynamic array, accessing through index
        self.matrix = self.set_matrix(distance_based)
    """ self.profile = 0
        self.nodes = [(0,1),(1,2),(3,5)]
        self.matrix = [[0,1,30],
                       [40,0,1],
                       [20,19,0]] """

        
    def set_matrix(self, distance_based):
        client = Valhalla(base_url="https://valhalla1.openstreetmap.de")
        matrix = client.matrix(locations=self.nodes, profile=self.profile)                      # [from][to] ([col][row], [x][y])
        distance= client.directions(locations=self.nodes[:2], profile=self.profile).distance
        print(distance)                                                                                       # print
        if distance_based:
            return matrix.distances
        else:
            return matrix.durations
        
    def to_string(self):                    # anders rum eigentlich, hier: row=from, col=to
        s = "Coords: \n"
        for a, b in self.nodes:
            s+= f"[{a}, {b}], "
        s+="\n"
        for x in self.matrix:
            s+="["
            for y in x:
                s+=f"{y}, "
            s+=f"], \n"
        return s  

    
    def shortest_path(self, start=None, end=None):            # giving the shortest of all posibile paths           # path: list, saving the indexes as int
        aPath = [-1] * len(self.nodes)
        marked = [False] * len(self.nodes)
        if end is not None:
            aPath[len(self.nodes)-1] = end
            marked[end] = True
        if start is not None:
            aPath[0] = start
            marked[start] = True
        else:
            bPath=None
            bLength = INFINITY
            for i in range(len(self.nodes)):
                if i != 0:
                    marked[i-1]= False
                marked[i] = True
                aPath[0] = i
                bPath, bLength = self.path(bPath, bLength, aPath, marked)
            return bPath, bLength
        return self.path(None, INFINITY, aPath, marked)       # iter over start

    def printL(self, path):
        s = "["
        for v in path:
            s+= f"{v},"
        print(s+']')
        
    def add(self, path, marked, n, i):
        path[i] = n
        marked[n] = True
        return path, marked
    
    def save_path(self, bPath, bLength, path, i):
        length = self.length(path)
        if length < bLength:
            bPath = path.copy()
            
            bLength = length
            return bPath, length
        return bPath,bLength
    
    def length(self, path):
        l = 0
        for i in range(len(path)-1) :
             l += self.matrix[path[i]][path[i+1]]
        return l
    
    def is_full_path(self, path):                                           # wenn weder der letzte noch der vorletzte -1 sind, ist keiner -1
        last = len(self.nodes)-1
        if path[last] == -1 or path[last-1] == -1:
            return False
        return True
    
    def go_back(self, marked, path, n, i):
        marked[path[i]] = False
        marked[path[i-1]] = False
        path[i] = -1
        i -= 1
        n = path[i] + 1
        return marked, path, n, i
        
    def go_next(self, n):
        return n+1   
    
    def no_more_paths(self, i):
        if i <= 0:
            return True
        return False
        
    def path(self, bPath, bLength, path, marked, n=0, i=1):         # giving the shortes path for a specific start node, optional specific end node
        if self.no_more_paths(i):
            return bPath, bLength
        
        if n >= len(self.nodes):
            marked, path, n, i = self.go_back(marked, path, n, i)
        elif marked[n] is False:
            path, marked = self.add(path, marked, n, i)
            i+= 1                                                                       # standard wert wenn man zum nächsten weiter geht
            n = 0
        else:
            n = self.go_next(n)
        if self.is_full_path(path):
            i-=1
            bPath, bLength = self.save_path(bPath, bLength, path, i)
            marked, path, n, i = self.go_back(marked, path, n, i)
        
        return self.path(bPath, bLength, path, marked, n, i)
