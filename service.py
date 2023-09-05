import csv
from geopy.distance import geodesic

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
        distance = get_distance(my_lon, my_lat, float(place['longitude']), float(place['latitude']))
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
            distance = get_distance(my_lon, my_lat, float(place['longitude']), float(place['latitude']))
            if distance < closest_distance and place not in closest_places:
                closest_place = place
                closest_distance = distance
        if closest_place:
            closest_places.append(closest_place)
    return closest_places