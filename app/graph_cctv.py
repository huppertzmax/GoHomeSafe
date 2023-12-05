import osmnx as ox
from cctv import *
import os

CCTV_WEIGHT_C1 = 0.75
CCTV_WEIGHT_C2 = 0.5
CCTV_WEIGHT_C3 = 0.1
CCTV_FILE_PATH = '../cctv_edges.pkl'


def adjust_graph_weights_cctv(graph):
    print("----------- CCTV -----------")
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
        print("Stored " + str(len(cctvs)) + " CCTV edges in " + CCTV_FILE_PATH)
    cctvs = cctvs_file

    adjust_cctv_weights(graph, cctvs)
    print("Weights for " + str(len(cctvs)) + " edges were adjusted based on cctv locations")
    print("----------- END CCTV -----------")


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


def adjust_cctv_weights(graph, cctvs):
    for cctv in cctvs:
        change_weights(
            graph=graph,
            start_node=cctv.get('start_node'),
            end_node=cctv.get('end_node'),
            key=cctv.get('key'),
            c1_weight=CCTV_WEIGHT_C1,
            c2_weight=CCTV_WEIGHT_C2,
            c3_weight=CCTV_WEIGHT_C3
        )
        graph[cctv.get('start_node')][cctv.get('end_node')][cctv.get('key')]['reason'] = "cctv"


def get_cctv_locations_file(graph):
    if os.path.exists(CCTV_FILE_PATH):
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
