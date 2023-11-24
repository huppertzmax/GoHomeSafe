import osmnx as ox


def adjust_graph_weights(graph):
    print("adjustment: Not yet implemented")


def initialize_graph():
    place_name = "Daejeon, South Korea"
    graph = ox.graph_from_place(place_name, network_type='walk')
    adjust_graph_weights(graph)
    return graph
