import osmnx as ox
from cctv import *
import os
import pickle

cctv_file_path = '../cctv_edges.pkl'
CCTV_WEIGHT = 0.75


def initialize_graph():
    place_name = "Daejeon, South Korea"
    graph = ox.graph_from_place(place_name, network_type='walk')
    initialize_attributes(graph)
    adjust_graph_weights_cctv(graph)
    return graph


def initialize_attributes(graph):
    print("Custom weights get initialized")

    meters_per_minute = calculate_travel_time()
    for u, v, k, d in graph.edges(keys=True, data=True):
        graph[u][v][k]['c_weight'] = d['length']
        graph[u][v][k]['walking_time'] = d['length'] / meters_per_minute

    print("Custom weights were initialized")


def calculate_travel_time():
    travel_speed = 4.5
    meters_per_minute = travel_speed * 1000 / 60
    return meters_per_minute


def adjust_graph_weights_cctv(graph):
    cctvs_file = get_cctv_locations_file(graph)
    cctvs_api = get_cctv_locations_all()
    cctvs_new = find_not_stored_cctv_locations(cctvs_file, cctvs_api)
    print("There are " + str(len(cctvs_new)) + " new CCTV locations")
    cctvs_old = find_stored_not_existing_cctv_locations(cctvs_file, cctvs_api)
    print("There are " + str(len(cctvs_old)) + " old CCTV locations which are not longer existing")

    # @TODO add functionality
    # remove_old_cctv_locations(graph, cctvs_old)
    if len(cctvs_new) > 0:
        cctvs = add_new_cctv_locations(graph, cctvs_file, cctvs_new)
        store_cctv_locations(cctvs)
        print("Stored " + str(len(cctvs)) + " CCTV edges in " + cctv_file_path)
    cctvs = cctvs_file

    # @TODO
    check_and_adjust_weights(graph, cctvs)
    print("Weights for " + str(len(cctvs)) + " edges were adjusted")


def find_not_stored_cctv_locations(cctvs_file, cctvs_api):
    cctvs_file = {item['cctv'] for item in cctvs_file}
    cctvs_new = [cctv for cctv in cctvs_api if cctv not in cctvs_file]
    return cctvs_new


def find_stored_not_existing_cctv_locations(cctvs_file, cctvs_api):
    cctvs_file = {item['cctv'] for item in cctvs_file}
    cctvs_old = [cctv for cctv in cctvs_file if cctv not in cctvs_api]
    return cctvs_old


def add_new_cctv_locations(graph, cctvs_file, cctvs_new):
    cctvs_new = compute_cctv_edges(graph, cctvs_new)
    cctvs_file.append(cctvs_new)
    return cctvs_file


def check_and_adjust_weights(graph, cctvs):
    for cctv in cctvs:
        length = graph[cctv.get('start_node')][cctv.get('end_node')][cctv.get('key')]['length']
        c_weight = length * CCTV_WEIGHT
        graph[cctv.get('start_node')][cctv.get('end_node')][cctv.get('key')]['c_weight'] = c_weight
        # print(graph[cctv.get('start_node')][cctv.get('end_node')][cctv.get('key')])


def store_cctv_locations(cctv_locations):
    with open(cctv_file_path, 'wb') as f:
        pickle.dump(cctv_locations, f)


def load_cctv_locations():
    with open(cctv_file_path, 'rb') as f:
        cctv_edges = pickle.load(f)
    return cctv_edges


def get_cctv_locations_file(graph):
    if os.path.exists(cctv_file_path):
        cctv_edges = load_cctv_locations()
    else:
        print("Computing of edges started")
        cctv_edges = compute_cctv_edges(graph, get_cctv_locations_all())
        store_cctv_locations(cctv_edges)
        print("Computing of edges completed")
    print(len(cctv_edges))
    print(cctv_edges)
    return cctv_edges


def compute_cctv_edges(graph, cctvs):
    # @TODO change to get_cctv_locations_all()
    # cctvs = get_cctv_locations_area(36.358312, 127.363987, 36.349862, 127.367356)
    # print(len(cctvs))
    count = 0
    cctv_edges = []
    for cctv in cctvs:
        u, v, k = ox.distance.nearest_edges(graph, cctv[1], cctv[0])
        data = graph[u][v][k]
        cctv_edges.append({"cctv": cctv, "start_node": u, "end_node": v,
                           "key": k, "osmid": data.get('osmid')})
        count = count + 1
        print(count)
    return cctv_edges


def test_edges(graph):
    print(get_cctv_locations_area(36.358312, 127.363987, 36.349862, 127.367356))
    cctv_edges = get_cctv_locations_file(graph)
    print('test')
    cctvs = []
    for c in cctv_edges:
        cctvs.append({"cctv": [c.get('cctv')[0], c.get('cctv')[1]], "start_node": str(c.get('start_node')),
                      "end_node": str(c.get('end_node'))})  # ,
        # "key": c.get('key'), "osmid": c.get('osmid'),
        # "length": c.get('length'),
        # "c_weight": c.get('c_weight')})
    print(cctvs)
    return {"cctvs": cctvs}
