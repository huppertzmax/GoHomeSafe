from graph_cctv import *


def initialize_graph():
    place_name = "Daejeon, South Korea"
    graph = ox.graph_from_place(place_name, network_type='walk')
    initialize_custom_graph_attributes(graph)
    return graph


def initialize_custom_graph_attributes(graph):
    print("Custom weights get initialized")

    meters_per_minute = calculate_travel_time()
    for u, v, k, d in graph.edges(keys=True, data=True):
        graph[u][v][k]['c1_weight'] = d['length']
        graph[u][v][k]['c2_weight'] = d['length']
        graph[u][v][k]['c3_weight'] = d['length']
        graph[u][v][k]['walking_time'] = d['length'] / meters_per_minute

    adjust_graph_weights_cctv(graph)
    print("Custom weights were initialized")


def calculate_travel_time():
    travel_speed = 4.5
    meters_per_minute = travel_speed * 1000 / 60
    return meters_per_minute
