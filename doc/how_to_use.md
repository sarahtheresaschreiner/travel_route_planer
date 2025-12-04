# How to use this tool

Travelplanner is a class so you have to create an object of it:
`tp = new Travelplanner()`
You can configure it:

- Parameters: `distance_based=True, mode: int=0`
- `distance_based`: `True` means the path is searched by travelling distance. `False`means that it is searched by travelling duration.
- `mode`: weather you go by car, bike etc.
  - `0`: car
  - `1`: by foot
  - `2`: with the bicycle

## Configuration options

You have a list of options how to use the planner:

- `add_spot(adress)` add a spot you want to visit.
- `change_spot(i, adress)` change the adress saved at a specific index
- `set_start(i)` declare where you want to start (optional)
- `set_end(i)` declare where you want to end (optional)

## Calculating

For calculating call `calculate()`. If you want the programm to print the path, you have to write `calculate(True)` (default is `False`).
