import osmnx as ox
import networkx as nx


def densify_coordinates(graph, route):
    dense_coordinates = []
    for n1, n2 in zip(route[:-1], route[1:]):
        lon = graph.nodes[n1]['x']
        lat = graph.nodes[n1]['y']
        data = graph.get_edge_data(n1, n2)

        if data[0].get('geometry') is not None:
            lats, lons = data[0]['geometry'].xy
            for x, y in zip(list(lats), list(lons)):
                dense_coordinates.append([x, y])
        else:
            dense_coordinates.append([lon, lat])
    lon = graph.nodes[route[-1]]['x']
    lat = graph.nodes[route[-1]]['y']
    dense_coordinates.append([lon, lat])
    return dense_coordinates


def densify_route(graph, route):
    dense_coordinates = densify_coordinates(graph, route)
    route_coordinates = []
    last_cord = None
    while len(dense_coordinates) > 0:
        current_cord = dense_coordinates.pop()
        if current_cord != last_cord:
            route_coordinates.append(current_cord)
        last_cord = current_cord
    route_coordinates.reverse()
    return route_coordinates


def get_nodes(graph, coordinates):
    return ox.distance.nearest_nodes(graph, coordinates[0], coordinates[1])


def calculate_route_stats(graph, route):
    length = 0
    duration = 0
    for f,t in zip(route[1:], route[:-1]):
        data = graph.get_edge_data(f, t)[0]
        length += data.get('length')
        duration += data.get('walking_time')
    return length, duration


def calculate_route(graph, start, end, fastest):
    start = get_nodes(graph, start)
    end = get_nodes(graph, end)
    if fastest:
        route = nx.shortest_path(graph, start, end, weight="length")
    else:
        route = nx.shortest_path(graph, start, end, weight="c_weight")
    coordinates = densify_route(graph, route)
    length, duration = calculate_route_stats(graph, route)
    route_type = 'fastest' if fastest else 'safest'
    return {"coordinates": coordinates, "length": length, "duration": duration, "type": route_type}
