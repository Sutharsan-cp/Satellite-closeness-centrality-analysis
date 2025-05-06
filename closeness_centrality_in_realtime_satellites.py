import turtle
from skyfield.api import load, wgs84, EarthSatellite
import time
import networkx as nx
import numpy as np

def haversine(coord1, coord2):
    R = 6371  # Earth radius in kilometers
    lat1, lon1 = np.radians(coord1)
    lat2, lon2 = np.radians(coord2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    return R * c  

screen = turtle.Screen()
screen.setup(720, 360)
screen.setworldcoordinates(-180, -90, 180, 90)
screen.bgpic("C:/Users/lokhe/OneDrive/Documents/Loki/CLG FLDR/Sem3/SCIENTIFIC COMPUTING LAB/world.png") 

screen.register_shape("C:/Users/lokhe/OneDrive/Documents/Loki/CLG FLDR/Sem3/SCIENTIFIC COMPUTING LAB/iss.gif")  
screen.register_shape("C:/Users/lokhe/OneDrive/Documents/Loki/CLG FLDR/Sem3/SCIENTIFIC COMPUTING LAB/eo1.gif")  
screen.register_shape("C:/Users/lokhe/OneDrive/Documents/Loki/CLG FLDR/Sem3/SCIENTIFIC COMPUTING LAB/geoeye.gif")  
screen.register_shape("C:/Users/lokhe/OneDrive/Documents/Loki/CLG FLDR/Sem3/SCIENTIFIC COMPUTING LAB/insat.gif") 

satellites = {
    'ISS': turtle.Turtle(),
    'EO-1': turtle.Turtle(),
    'GeoEye': turtle.Turtle(),
    'INSAT': turtle.Turtle()
}

satellites['ISS'].shape("C:/Users/lokhe/OneDrive/Documents/Loki/CLG FLDR/Sem3/SCIENTIFIC COMPUTING LAB/iss.gif")
satellites['EO-1'].shape("C:/Users/lokhe/OneDrive/Documents/Loki/CLG FLDR/Sem3/SCIENTIFIC COMPUTING LAB/eo1.gif")
satellites['GeoEye'].shape("C:/Users/lokhe/OneDrive/Documents/Loki/CLG FLDR/Sem3/SCIENTIFIC COMPUTING LAB/geoeye.gif")
satellites['INSAT'].shape("C:/Users/lokhe/OneDrive/Documents/Loki/CLG FLDR/Sem3/SCIENTIFIC COMPUTING LAB/insat.gif")  

for satellite in satellites.values():
    satellite.penup()

ts = load.timescale()
# TLE- Two Line Element
#00075A represents year 2000 and 075 number of  launch in that year
tle_data = {
    'EO-1': [
        "EO-1", #represents Name of the satellite like keyword
        "1 26619U 00075A   23310.40850000  .00000036  00000-0  18182-4 0  9998", #1st pare represents serialcode 
        "2 26619  98.1900 352.6785 0001247 264.4800  95.5190 14.57183959573349" #this line represents the orbit information
    ],
    'GeoEye': [
        "GeoEye-1",
        "1 33331U 08044A   23311.23514929  .00000089  00000-0  10673-4 0  9999",
        "2 33331  97.8942  24.9366 0001461  89.1429 270.9842 15.24449795613689"
    ],
    'ISS': [
        "ISS",
        "1 25544U 98067A   23311.02404121  .00002671  00000-0  62614-5 0  9992",
        "2 25544  51.6446  88.9176 0003456  51.0359 309.0498 15.50190458306719"
    ],
    'INSAT': [
        "INSAT-3A",
        "1 26620U 00076A   23311.55555555  .00000036  00000-0  18182-4 0  9999",
        "2 26620  36.0000  48.5678 0001234  75.2560 284.7390 15.50190458306719"
    ]
}

satellites_objects = {name: EarthSatellite(tle[1], tle[2], tle[0], ts) for name, tle in tle_data.items()}

nasa_position = (-77.0369, 38.9072) 
ahem_position = (-122.177, 37.425)  
isro_position = (77.5946, 12.9716)  

graph = nx.Graph()

for name in satellites:
    graph.add_node(name)
graph.add_node("NASA")
graph.add_node("Ahem Research Center")
graph.add_node("ISRO")

for name in satellites:
    graph.add_edge(name, "NASA")
    graph.add_edge(name, "Ahem Research Center")
    graph.add_edge(name, "ISRO")

def update_position(satellite_name, turtle_obj):
    satellite = satellites_objects[satellite_name]
    t = ts.now()
    geocentric = satellite.at(t)
    subpoint = wgs84.subpoint(geocentric)
    
    lat = subpoint.latitude.degrees
    lon = subpoint.longitude.degrees
    
    turtle_obj.goto(lon, lat)
    
    turtle_obj.clear()
    turtle_obj.write(f"{satellite_name}\nLat: {lat:.2f}, Lon: {lon:.2f}", 
                      align="center", font=("Arial", 10, "normal"))

def draw_line(start, end):
    turtle.penup()
    turtle.goto(start)
    turtle.pendown()
    turtle.goto(end)
    turtle.penup()

def draw_edges():
    # Draw edge from NASA to each satellite
    for name, turtle_obj in satellites.items():
        draw_line(nasa_position, turtle_obj.position())
    
    for name, turtle_obj in satellites.items():
        draw_line(ahem_position, turtle_obj.position())
    
    for name, turtle_obj in satellites.items():
        draw_line(isro_position, turtle_obj.position())

def calculate_closeness_centrality():
    distances_nasa = []
    distances_ahem = []
    distances_isro = []

    for satellite in satellites_objects.values():
        t = ts.now()
        geocentric = satellite.at(t)
        subpoint = wgs84.subpoint(geocentric)
        
        sat_position = (subpoint.latitude.degrees, subpoint.longitude.degrees)
        
        distance_to_nasa = haversine(sat_position, nasa_position)
        distance_to_ahem = haversine(sat_position, ahem_position)
        distance_to_isro = haversine(sat_position, isro_position)
        
        distances_nasa.append(distance_to_nasa)
        distances_ahem.append(distance_to_ahem)
        distances_isro.append(distance_to_isro)

    nasa_closeness = len(distances_nasa) / sum(distances_nasa) if sum(distances_nasa) > 0 else 0

    ahem_closeness = len(distances_ahem) / sum(distances_ahem) if sum(distances_ahem) > 0 else 0

    isro_closeness = len(distances_isro) / sum(distances_isro) if sum(distances_isro) > 0 else 0

    return nasa_closeness, ahem_closeness, isro_closeness

while True:
    if screen._root is None:  
        break  

    turtle.clear()

    turtle.penup()
    turtle.goto(nasa_position)
    turtle.dot(10, "blue")
    turtle.write("NASA", align="right")

    turtle.penup()
    turtle.goto(ahem_position)
    turtle.dot(10, "green")
    turtle.write("Ahem Research Center", align="right")

    turtle.penup()
    turtle.goto(isro_position)
    turtle.dot(10, "red")
    turtle.write("ISRO", align="right")

    for name, turtle_obj in satellites.items():
        update_position(name, turtle_obj)

    draw_edges()

    nasa_closeness, ahem_closeness, isro_closeness = calculate_closeness_centrality()
    print(f"Closeness Centrality - NASA: {nasa_closeness:.7f}, Ahem: {ahem_closeness:.7f}, ISRO: {isro_closeness:.7f}")

    time.sleep(5)

turtle.bye()
