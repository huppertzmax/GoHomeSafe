import osmnx as ox
import networkx as nx

LENGTH_TOLERANCE = 0.2


def calculate_route(graph, start, end, fastest):
    start = get_nodes(graph, start)
    end = get_nodes(graph, end)
    route_fastest = nx.shortest_path(graph, start, end, weight="length")
    if fastest:
        route = route_fastest
    else:
        route_c1 = nx.shortest_path(graph, start, end, weight="c1_weight")
        route_c2 = nx.shortest_path(graph, start, end, weight="c2_weight")
        route_c3 = nx.shortest_path(graph, start, end, weight="c3_weight")
        route = select_safest_route(graph, route_fastest, route_c1, route_c2, route_c3)
    coordinates = interpolate_coordinates_of_route(graph, route)
    length, duration, cctv, reasons = calculate_route_stats(graph, route)
    route_type = 'fastest' if fastest else 'safest'
    return {
        "coordinates": coordinates,
        "length": length,
        "duration": duration,
        "type": route_type,
        "cctv": cctv,
        "reasons": reasons
    }


def interpolate_coordinates_of_route(graph, route):
    """
        This function interpolates the coordinates between all nodes of a given route
    :param graph: ox graph on which the route is located
    :param route: list of osm nodes in the graph representing the route
    :return: list of all coordinates between all nodes of the route
    """
    interpolated_coordinates = []
    for n1, n2 in zip(route[:-1], route[1:]):
        lon = graph.nodes[n1]['x']
        lat = graph.nodes[n1]['y']
        data = graph.get_edge_data(n1, n2)

        if data[0].get('geometry') is not None:
            lats, lons = data[0]['geometry'].xy
            for x, y in zip(list(lats), list(lons)):
                interpolated_coordinates.append([x, y])
        else:
            interpolated_coordinates.append([lon, lat])
    lon = graph.nodes[route[-1]]['x']
    lat = graph.nodes[route[-1]]['y']
    interpolated_coordinates.append([lon, lat])
    return remove_duplicates_of_interpolated_coordinates(interpolated_coordinates)


def remove_duplicates_of_interpolated_coordinates(interpolated_coordinates):
    route_coordinates = []
    last_coordinate = None
    while len(interpolated_coordinates) > 0:
        current_coordinate = interpolated_coordinates.pop()
        if current_coordinate != last_coordinate:
            route_coordinates.append(current_coordinate)
        last_coordinate = current_coordinate
    route_coordinates.reverse()
    return route_coordinates


def get_nodes(graph, coordinates):
    return ox.distance.nearest_nodes(graph, coordinates[0], coordinates[1])


def calculate_route_stats(graph, route):
    length = 0
    duration = 0
    cctv = 0
    reasons = []
    for node1, node2 in zip(route[1:], route[:-1]):
        data = graph.get_edge_data(node1, node2)[0]
        length += data.get('length')
        duration += data.get('walking_time')
        if 'reason' in data:
            reasons.append({
                "start_node": node1,
                "end_node": node2,
                "reason": data.get('reason')
            })
            if data.get('reason') == "cctv":
                cctv += 1
    return length, duration, cctv, reasons


def select_safest_route(graph, route_fastest, route_c1, route_c2, route_c3):
    score_c1 = calculate_route_score(graph, route_fastest, route_c1)
    score_c2 = calculate_route_score(graph, route_fastest, route_c2)
    score_c3 = calculate_route_score(graph, route_fastest, route_c3)
    print("Scores calculated: c1: " + str(score_c1) + " c2: " + str(score_c2) + " c3: "+ str(score_c3))
    if score_c1 >= score_c2 and score_c1 >= score_c3:
        print("Route based on weights of c1")
        return route_c1
    elif score_c2 >= score_c1 and score_c2 >= score_c3:
        print("Route based on weights of c2")
        return route_c2
    print("Route based on weights of c3")
    return route_c3


def calculate_route_score(graph, route_fastest, route_safe):
    length_fastest, duration_fastest, cctv_fastest, reasons_fastest = calculate_route_stats(graph, route_fastest)
    length, duration, cctv, reasons = calculate_route_stats(graph, route_safe)
    length_dif = length - length_fastest
    length_change = length_dif/length_fastest
    if length_change > LENGTH_TOLERANCE:
        return 0
    score_cctv = cctv - cctv_fastest
    if score_cctv < 1:
        return 0
    else:
        return length_dif / score_cctv
