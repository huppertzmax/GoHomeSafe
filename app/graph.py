from graph_cctv import *
from graph_sensor import *


def initialize_graph(sensor_min):
    place_name = "Daejeon, South Korea"
    graph = ox.graph_from_place(place_name, network_type='walk')
    initialize_attributes(graph)
    adjust_weights(graph, sensor_min)
    return graph


def initialize_attributes(graph):
    print("Custom weights get initialized")

    meters_per_minute = calculate_travel_time()
    for u, v, k, d in graph.edges(keys=True, data=True):
        graph[u][v][k]['c1_weight'] = d['length']
        graph[u][v][k]['c2_weight'] = d['length']
        graph[u][v][k]['c3_weight'] = d['length']
        graph[u][v][k]['walking_time'] = d['length'] / meters_per_minute

    print("Custom weights were initialized")


def calculate_travel_time():
    travel_speed = 4.5
    meters_per_minute = travel_speed * 1000 / 60
    return meters_per_minute


def adjust_weights(graph, sensor_min):
    initialize_attributes(graph)
    print("Custom weights get calculated")
    adjust_graph_weights_cctv(graph)
    adjust_graph_weights_sensor(graph, sensor_min)
    print("Custom weights were calculated")
