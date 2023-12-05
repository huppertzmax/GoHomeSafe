import osmnx as ox
import networkx as nx

LENGTH_TOLERANCE = 0.2


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
    cctv = 0
    sensors_good = 0
    sensors_bad = 0
    reasons = []
    for f,t in zip(route[1:], route[:-1]):
        data = graph.get_edge_data(f, t)[0]
        length += data.get('length')
        duration += data.get('walking_time')
        if 'reason' in data:
            reasons.append({
                "start_node": f,
                "end_node": t,
                "reason": data.get('reason')
            })
            if data.get('reason') == "loud":
                sensors_good += 1
            elif data.get('reason') == "silent":
                sensors_bad += 1
            elif data.get('reason') == "cctv":
                cctv += 1
    return length, duration, cctv, sensors_good, sensors_bad, reasons


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
    coordinates = densify_route(graph, route)
    length, duration, cctv, sensors_good, sensors_bad, reasons = calculate_route_stats(graph, route)
    route_type = 'fastest' if fastest else 'safest'
    return {
        "coordinates": coordinates,
        "length": length,
        "duration": duration,
        "type": route_type,
        "cctv": cctv,
        "sensors_good": sensors_good,
        "sensors_bad": sensors_bad,
        "reasons": reasons
    }


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
    length_fastest, duration_fastest, cctv_fastest, sensors_good_fastest, sensors_bad_fastest, reasons_fastest = calculate_route_stats(graph, route_fastest)
    length, duration, cctv, sensors_good, sensors_bad, reasons = calculate_route_stats(graph, route_safe)
    length_dif = length - length_fastest
    length_change = length_dif/length_fastest
    if length_change > LENGTH_TOLERANCE:
        return 0
    cctv_dif = cctv - cctv_fastest
    sensors_good_dif = sensors_good - sensors_good_fastest
    sensors_bad_dif = sensors_bad_fastest - sensors_bad
    score_cctv_sensors = cctv_dif + sensors_good_dif + sensors_bad_dif
    if score_cctv_sensors < 1:
        return 0
    else:
        return length_dif / score_cctv_sensors
