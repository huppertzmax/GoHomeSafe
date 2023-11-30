from flask import Flask, request
from flask_cors import CORS
from routing import *
from graph import *
from cctv import *
import os
import pickle

app = Flask('gohomesafe')
cors = CORS(app)


def startup():
    print("Graph initialization started")
    global graph
    file_path = '../graph_daejeon.pkl'

    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            graph = pickle.load(f)
        adjust_graph_weights_cctv(graph)
    else:
        print("Graph file will be created")
        graph = initialize_graph()
        with open(file_path, 'wb') as f:
            pickle.dump(graph, f)
    print("Graph initialization completed")


@app.route("/")
def hello_world():
    return "<p>Welcome to GoHomeSafe!</p>"


@app.route("/route")
def routing(fastest=False):
    args = request.args
    if validate_route_args(args):
        route_coordinates = calculate_route(graph,
                                            [float(args.get('start_lon')), float(args.get('start_lat'))],
                                            [float(args.get('end_lon')), float(args.get('end_lat'))],
                                            fastest)
        return route_coordinates
    else:
        print("Error: arguments not correct")
        return "Error"


@app.route("/route/fastest")
def routing_fastest():
    return routing(True)


@app.route("/cctv/all")
def cctv_locations_all():
    return get_cctv_locations_all()


@app.route("/cctv/area")
def cctv_locations_area():
    args = request.args
    if validate_route_args(args):
        return get_cctv_locations_area(float(args.get('start_lat')), float(args.get('start_lon')),
                                       float(args.get('end_lat')), float(args.get('end_lon')))
    else:
        print("Error: arguments not correct")
        return "Error"


with app.app_context():
    startup()
