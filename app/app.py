from flask import Flask, request
from flask_cors import CORS
from routing import *
from graph import *
from cctv import *
from sensor import *
from utils import *
import os
import pickle

app = Flask('gohomesafe')
cors = CORS(app)


def startup():
    print("Graph initialization started")
    global graph
    global SENSOR_MIN
    # TODO rename variable
    SENSOR_MIN =  0.2
    file_path = '../graph_daejeon.pkl'

    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            graph = pickle.load(f)
        initialize_custom_graph_attributes(graph, SENSOR_MIN)
    else:
        print("Graph file will be created")
        graph = initialize_graph(SENSOR_MIN)
        with open(file_path, 'wb') as f:
            pickle.dump(graph, f)
    print("Graph initialization completed")


@app.route("/route")
def get_route(fastest=False):
    args = request.args
    if validate_coordinate_args(args):
        start_coordinates, end_coordinates = extract_start_and_end_coordinates(args)
        route_coordinates = calculate_route(graph, start_coordinates, end_coordinates, fastest)
        return route_coordinates
    else:
        raise ValueError("Error while trying to calculate route due to invalid arguments")


@app.route("/route/fastest")
def get_fastest_route():
    return get_route(fastest=True)


@app.route("/cctv/area")
def get_cctv_locations_in_area():
    args = request.args
    if validate_coordinate_args(args):
        start_coordinates, end_coordinates = extract_start_and_end_coordinates(args)
        # TODO maybe change back lat lon order
        start_lon, start_lat = start_coordinates
        end_lon, end_lat = end_coordinates
        return get_sensor_locations_area(start_lat, start_lon, end_lat, end_lon, SENSOR_MIN)
    else:
        raise ValueError("Error while trying to get all cctv locations in an area due to invalid arguments")


@app.route("/sensor/area")
def get_sensor_locations_in_area():
    args = request.args
    if validate_coordinate_args(args):
        start_coordinates, end_coordinates = extract_start_and_end_coordinates(args)
        start_lon, start_lat = start_coordinates
        end_lon, end_lat = end_coordinates
        return get_sensor_locations_area(start_lat, start_lon, end_lat, end_lon, SENSOR_MIN)
    else:
        raise ValueError("Error while trying to get all sensor locations in an area due to invalid arguments")


@app.route("/cctv/all")
def get_all_cctv_locations():
    return get_cctv_locations_all()


@app.route("/sensor/all")
def get_all_sensor_locations():
    return get_sensor_locations_all(SENSOR_MIN)


with app.app_context():
    startup()
