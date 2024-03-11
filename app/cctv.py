import requests
from utils import *
import pickle


CCTV_FILE_PATH = '../cctv_edges.pkl'


def request_cctv_locations():
    api_url = 'https://www.seogu.go.kr/seoguAPI/3660000/getCctvLifeSecrty'
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json().get('response').get('body')
    else:
        print("Error: CCTV data could not be loaded")


def get_cctv_locations_all():
    return list_cctv_coordinates(request_cctv_locations())


def get_cctv_locations_area(start_lat, start_lon, end_lat, end_lon):
    cctv_locations = get_cctv_locations_all()
    middle, distance = get_middle_and_distance_based_on_two_points(start_lat, start_lon, end_lat, end_lon)
    cctv_locations = filter_points_in_distance_of_middle_point(cctv_locations, middle, distance)
    return cctv_locations


def list_cctv_coordinates(data):
    cctv_coordinates = []
    response_items = data.get('items')
    for element in response_items:
        cctv_coordinates.append((element.get("la"), element.get("lo")))
    return cctv_coordinates


def store_cctv_locations(cctv_locations):
    with open(CCTV_FILE_PATH, 'wb') as f:
        pickle.dump(cctv_locations, f)


def load_cctv_locations():
    with open(CCTV_FILE_PATH, 'rb') as f:
        cctv_edges = pickle.load(f)
    return cctv_edges
