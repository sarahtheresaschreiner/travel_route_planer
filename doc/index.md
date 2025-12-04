# Travel Planner

Find the optimal route over a list of spots you want to visit, and optional choose a start- and endpoint.
[How to use it](./how_to_use.md)

## General Idea

- Python module
- Takes Spots as input and returns the optimal route rated by eather minimal distance or time

## Techniacal idea

- Use a directed graph with adjacency matrix, weighted edges (eather distance or time)
- Store the weight in the matrix

## Building the graph data structure

- I decided to build a graph myself to practice working with this data structure and get a deper understanding.
- **Matrix:**
  - Stored value is the weight
  - `[from][to]`

## Which Modules/APIs to use?

- I decided to use **geopy** for getting the coordinates (longitude & latitude) with Nominatim. It is easy to use and does not need very detailed input and also does not has a strict syntax on the input, which is very User friendly.
- For calculating the distance between two points I decided to use **routingpy** with **Valhalla**. It is ideal because it offers the option to create a matrix with the distance of a *list of locations* to a *list of other locations*.
  - I chose a community hosted endpoint [https://valhalla.openstreetmap.de/](https://valhalla.openstreetmap.de/), eventhough it is slower than other options, but for this small project it works good enough and doesn't exceed the limits.

## The Algorithm

I needed an algorithm, that would find the shortest path in the graph visiting all vertices. The first part of it (shortest path in a graph), wasn't a problem. I looked at allgorithms like Dijkstra and Bellmann-Ford. But all this algorithms did not visit all vertices. I thought about a few options (cf. *algorithm ideas*). So I googled my problem and turns out the path I'm searching is called Hamilton path. Knowing that I googled further and it seemed like my problem is similar to the *travelling salesman problem* (shortest hamiltonian circle, starting and ending at the same point, instead of different points as in my project). That was the moment I realised my problem is NP-Complete/NP-Hard (the sources said different).
At that moment I wanted to throw the project in the bin, because there was no way that this project would work as I imagined it. But I decided to complete it, eventhough the heart of project wouldn't work.

### My algorithm

- Iterating over every possible order and doing linear search for finding which order has the smallest length (travelling time/distance)
- This runs in 0(n!)-Time, n being the amount of spots that are visited

#### Getting all paths to iterate over

I used a recursive function, that eather adds the next possible spot to the order or goes back to the spot before and changes it. It does this aswell if it detects that the path is full, it compares it to the shortest allready found path and if its shorter the new path is saved as the new best path:

```python
def path(self, bPath, bLength, path, marked, n=0, i=1):
        if self.no_more_paths(i):
            return bPath, bLength
        
        if n >= len(self.nodes):
            marked, path, n, i = self.go_back(marked, path, n, i)
        elif marked[n] is False:
            path, marked = self.add(path, marked, n, i)
            n = 0
        else:
            n = self.go_next(n)
        if self.is_full_path(path):
            i-=1
            bPath, bLength = self.save_path(bPath, bLength, path, i)
            marked, path, n, i = self.go_back(marked, path, n, i)
        
        return self.path(bPath, bLength, path, marked, n, i)
```

- `no_more_paths()` detects if there is no more path to find
- `go_back` goes one step back to the vertex before the current one.
- `add` adds the current vertex to the path
- `go_next` goes to the next spot in the path
- `is_full_path` checks if the path is complete
- `save_path` checks if the path is shorter than the one before and if yes it saves it
- **The parameters:**
  - `bPath` is the best Path, found yet. At the start it is `None`
  - `bLength` is the length (travelling distance/duration) of bPath. At the start it's `infinite`
  - `path` is the current path, were `-1` is used as empty
  - `marked[]` saves if a vertex is allready in the order
  - `n` is the next value, that will be checked
  - `i` is the index of the path your currently looking at

### Algorithm ideas

Before I found out that there was no solution, I had a few ideas, which would have worked in some cases but not in every case:

1. An idea was to use Dijkstra Algorithm to find the shortest path and then add the ones who aren't used into the position that would add the least distatnce to the route
2. The other idea I had, was to start at one vertex and then allways go to the vertex that is the nearest.
