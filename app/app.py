from flask import Flask, request
from routing import *
from graph import *
import os
import pickle

app = Flask('gohomesafe')


def startup():
    print("Graph initialization started")
    global graph
    file_path = '../graph_daejeon.pkl'

    if os.path.exists(file_path):
        with open('../graph_daejeon.pkl', 'rb') as f:
            graph = pickle.load(f)
    else:
        print("Graph file will be created")
        graph = initialize_graph()
        with open('../graph_daejeon.pkl', 'wb') as f:
            pickle.dump(graph, f)
    print("Graph initialization completed")


@app.route("/")
def hello_world():
    return "<p>Welcome to GoHomeSafe!</p>"


@app.route("/route")
def routing():
    args = request.args
    if validate_route_args(args):
        route_coordinates = calculate_route(graph,
                                            [float(args.get('start_lat')), float(args.get('start_lon'))],
                                            [float(args.get('end_lat')), float(args.get('end_lon'))])
        return route_coordinates
    else:
        print("Error: arguments not correct")
        return "Error"


with app.app_context():
    startup()
