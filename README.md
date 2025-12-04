# Travel planner using Graph

Pyton  module for getting the shortest path/order for visiting every spot you want to visit.

## Why is it useful?

This project came to live after I faced the problem it solves myself. I was in Berlin this summer and wanted to make a tour visiting a list of Sightseeing spots. I was looking at Google Maps, and i could add various spots, and it would give me a route. But it couldn't give me advice in which order to visit the tourist attractions. This way I had to search it myself, which was very painful. My tool solves this problem. You can say which spots you want to visit and you get a recommended order with even coordinats if you want.

## Which Modules/APIs to use?

- I decided to use **geopy** for getting the coordinates (longitude & latitude) with Nominatim. It is easy to use and does not need very detailed input and also does not has a strict syntax on the input, which is very User friendly.
- For calculating the distance between two points I decided to use **routingpy** with **Valhalla**. It is ideal because it offers the option to create a matrix with the distance of a *list of locations* to a *list of other locations*.
  - I chose a community hosted endpoint [https://valhalla.openstreetmap.de/](https://valhalla.openstreetmap.de/), eventhough it is slower than other options, but for this small project it works good enough and doesn't exceed the limits.
  