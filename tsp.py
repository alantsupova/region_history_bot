import numpy as np
from python_tsp.exact import solve_tsp_dynamic_programming
from geopy.distance import geodesic


def tsp(locations):
    distances_np = np.array(get_dictances(locations))

    return solve_tsp_dynamic_programming(distances_np)


def get_dictances(places):
    n = len(places)
    distances = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                row.append(0)
            else:
                distance = geodesic((places[i]['latitude'], places[i]['longitude']),
                                    (places[j]['latitude'], places[j]['longitude'])).km
                row.append(distance)
        distances.append(row)
    return distances

