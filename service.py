import pandas as pd
from geopy.distance import geodesic
import csv
import tsp


def draw_route(route):
    m = folium.Map(location=[route[0]['longitude'], route[0]['latitude']], zoom_start=12)
    points = []
    for place in route:
        folium.Marker([place['longitude'], place['latitude']]).add_to(m)
        points.append([place['longitude'], place['latitude']])
    m.save('map.html')


def get_distance(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).km


def get_nearest_place(my_lon, my_lat):
    places = []
    with open('places.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            places.append(row)
    closest_place = None
    closest_distance = float('inf')
    for place in places:
        distance = get_distance(my_lon, my_lat, float(place['longitude']),
                                float(place['latitude']))
        if distance < closest_distance:
            closest_place = place
            closest_distance = distance
    return closest_place


def get_nearest_places(my_lon, my_lat, n):
    places = []
    with open('places.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            places.append(row)
    closest_places = []
    for i in range(n):
        closest_place = None
        closest_distance = float('inf')
        for place in places:
            distance = get_distance(my_lon, my_lat, float(place['longitude']),
                                    float(place['latitude']))
            if distance < closest_distance and place not in closest_places:
                closest_place = place
                closest_distance = distance
        if closest_place:
            closest_places.append(closest_place)
    return closest_places


def get_simple_route(my_lon, my_lat, n):
    places = []
    with open('places.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            places.append(row)
    closest_places = []
    closest_place = None
    closest_distance = float('inf')
    for place in places:
        distance = get_distance(my_lon, my_lat, float(place['longitude']),
                                float(place['latitude']))
        if distance < closest_distance and place not in closest_places:
            closest_place = place
            closest_distance = distance
    if closest_place:
        closest_places.append(closest_place)
    for i in range(n - 1):
        closest_place = None
        closest_distance = float('inf')
        for place in places:
            distance = get_distance(places[-1]['longitude'], places[-1]['latitude'],
                                    float(place['longitude']), float(place['latitude']))
            if distance < closest_distance and place not in closest_places:
                closest_place = place
                closest_distance = distance
        if closest_place:
            closest_places.append(closest_place)
    return closest_places


def get_circle_route(my_lon, my_lat, n):
    places = []
    with open('places.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            places.append(row)
    closest_places = []
    closest_places.append({'longitude': my_lon, 'latitude': my_lat})
    for i in range(n):
        closest_place = None
        closest_distance = float('inf')
        for place in places:
            distance = get_distance(my_lon, my_lat, float(place['longitude']),
                                    float(place['latitude']))
            if distance < closest_distance and place not in closest_places:
                closest_place = place
                closest_distance = distance
        if closest_place:
            closest_places.append(closest_place)
    order, route = tsp.tsp(closest_places)
    res = list()
    for o in order:
        res.append(closest_places[o])
    return res
