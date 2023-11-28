import osmnx as ox


def adjust_graph_weights(graph):
    print(graph[4937770573][4943607248][0])
    graph[4937770573][4943607248][0]['c_weight'] = graph[4937770573][4943607248][0]['c_weight'] * 100.00
    print(graph[4937770573][4943607248][0])
    print("adjustment: Not yet implemented")


def calculate_travel_time():
    travel_speed = 4.5
    meters_per_minute = travel_speed * 1000 / 60
    return meters_per_minute


def initialize_attributes(graph):
    print("Custom weights get initialized")

    meters_per_minute = calculate_travel_time()
    for u, v, k, d in graph.edges(keys=True, data=True):
        graph[u][v][k]['c_weight'] = d['length']
        graph[u][v][k]['walking_time'] = d['length'] / meters_per_minute

    print("Custom weights were initialized")


def initialize_graph():
    place_name = "Daejeon, South Korea"
    graph = ox.graph_from_place(place_name, network_type='walk')
    initialize_attributes(graph)
    adjust_graph_weights(graph)
    return graph
