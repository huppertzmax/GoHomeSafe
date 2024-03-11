import osmnx as ox
from cctv import *
import os

CCTV_WEIGHT_C1 = 0.75
CCTV_WEIGHT_C2 = 0.5
CCTV_WEIGHT_C3 = 0.1
CCTV_FILE_PATH = '../cctv_edges.pkl'


def adjust_graph_weights_cctv(graph):
    # TODO clean up logging
    print("----------- CCTV -----------")

    cctv_file_data = get_cctv_locations_file(graph)
    cctv_api_data = get_cctv_locations_all()

    new_cctv_locations = find_not_stored_cctv_locations(cctv_file_data, cctv_api_data)
    no_longer_run_cctv_locations = find_stored_but_no_longer_running_cctv_locations(cctv_file_data, cctv_api_data)
    print("There are " + str(len(new_cctv_locations)) + " new CCTV locations, which are not yet stored")
    print("There are " + str(len(no_longer_run_cctv_locations)) + "old CCTV locations stored, which are no longer "
                                                                  "running")

    # @TODO add functionality: removing no longer running CCTV locations form local file
    # remove_old_cctv_locations(graph, no_longer_run_cctv_locations)
    cctvs = add_and_store_new_cctv_locations(graph, cctv_file_data, new_cctv_locations)

    adjust_cctv_weights(graph, cctvs)
    print("Weights for " + str(len(cctvs)) + " edges were adjusted based on cctv locations")
    print("----------- END CCTV -----------")


def get_cctv_locations_file(graph):
    if os.path.exists(CCTV_FILE_PATH):
        cctv_edges = load_cctv_locations()
    else:
        print("Creation of CCTV locations file started")
        cctv_edges = compute_osm_edge_of_cctvs(graph, get_cctv_locations_all())
        store_cctv_locations(cctv_edges)
        print("Creation of CCTV locations file completed")
    print("Number of CCTV cameras: ", len(cctv_edges))
    return cctv_edges


def add_and_store_new_cctv_locations(graph, cctvs_file, cctvs_new):
    if len(cctvs_new) > 0:
        cctvs_new = compute_osm_edge_of_cctvs(graph, cctvs_new)
        cctvs_file.append(cctvs_new)
        store_cctv_locations(cctvs_file)
        print("Stored " + str(len(cctvs_file)) + " CCTV edges in " + CCTV_FILE_PATH)
    return cctvs_file


def find_not_stored_cctv_locations(cctvs_file, cctvs_api):
    cctvs_file = {item['cctv'] for item in cctvs_file}
    cctvs_new = [cctv for cctv in cctvs_api if cctv not in cctvs_file]
    return cctvs_new


def find_stored_but_no_longer_running_cctv_locations(cctvs_file, cctvs_api):
    cctvs_file = {item['cctv'] for item in cctvs_file}
    cctvs_old = [cctv for cctv in cctvs_file if cctv not in cctvs_api]
    return cctvs_old


def adjust_cctv_weights(graph, cctvs):
    for cctv in cctvs:
        change_weights_between_nodes(
            graph=graph,
            start_node=cctv.get('start_node'),
            end_node=cctv.get('end_node'),
            key=cctv.get('key'),
            c1_weight=CCTV_WEIGHT_C1,
            c2_weight=CCTV_WEIGHT_C2,
            c3_weight=CCTV_WEIGHT_C3
        )
        graph[cctv.get('start_node')][cctv.get('end_node')][cctv.get('key')]['reason'] = "cctv"


def compute_osm_edge_of_cctvs(graph, cctvs):
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
