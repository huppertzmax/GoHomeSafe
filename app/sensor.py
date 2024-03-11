from utils import *
import uuid
import pickle
from graph_sensor import *


SENSOR_MOCK_FILE_PATH = '../sensor_mock.pkl'
SENSOR_AMOUNT = 300


def request_sensor_locations():
    # @TODO change with actual sensor api
    return load_sensor_locations()


def get_sensor_locations_all(sensor_min):
    return list_sensor_coordinates(request_sensor_locations(), sensor_min)


# @TODO fix bug with sensor min
def get_sensor_locations_area(start_lat, start_lon, end_lat, end_lon, sensor_min):
    sensor_locations = get_sensor_locations_all(sensor_min)
    middle, distance = get_middle_and_distance_based_on_two_points(start_lat, start_lon, end_lat, end_lon)
    sensor_locations = filter_points_in_distance_of_middle_point(sensor_locations, middle, distance)
    return sensor_locations


def list_sensor_coordinates(data, sensor_min):
    sensor_coordinates = []
    for element in data:
        sensor_coordinates.append((element.get('sensor')[0], element.get('sensor')[1], is_safe(element, sensor_min)))
    return sensor_coordinates


def load_sensor_locations():
    with open(SENSOR_MOCK_FILE_PATH, 'rb') as f:
        cctv_edges = pickle.load(f)
    return cctv_edges


def is_safe(sensor, sensor_min):
    value = get_sensor_value(sensor.get("sensor_id"))
    if value > sensor_min:
        return 1
    else:
        return 0


def get_sensor_value(sensor_id):
    # @TODO change to requesting actual value
    if sensor_id == uuid.UUID('d0f352a8-1134-41e7-a5f6-48bb7d6b25ce'):
        return 0.1
    return random.random()


# @TODO remove after actual sensor data is available
''' def create_sensor_mock_data(graph):
    edges = graph.edges(keys=True, data=True)
    edges_list = list(edges)
    edges_picked = random.choices(edges_list, k=SENSOR_AMOUNT)
    sensors = []
    for edge in edges_picked:
        start_coordinates = (graph.nodes[edge[0]]['y'], graph.nodes[edge[0]]['x'])
        print(start_coordinates)
        end_coordinates = (graph.nodes[edge[1]]['y'], graph.nodes[edge[1]]['x'])
        print(end_coordinates)
        middle = ((start_coordinates[0]+end_coordinates[0])/2, (start_coordinates[1]+end_coordinates[1])/2)
        print(middle)
        sensors.append({
            "sensor": [middle[0], middle[1]],
            "sensor_id": uuid.uuid4(),
            "start_node": edge[0],
            "end_node": edge[1],
            "key": edge[2],
            "osmid": edge[3].get('osmid')
        })
        print(edge)

    print(sensors)
    print(len(sensors))
    with open(SENSOR_MOCK_FILE_PATH, 'wb') as f:
        pickle.dump(sensors, f)
    print("dumped")
    return len(edges)
'''