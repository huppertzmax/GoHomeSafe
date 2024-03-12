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
        raise ConnectionError("Error: CCTV data could not be loaded, "
                              "response code was not 200 but was {}".format(response.status_code))


def get_cctv_locations_all():
    return extract_cctv_coordinates_from_request(request_cctv_locations())


def get_cctv_locations_area(start_lat, start_lon, end_lat, end_lon):
    cctv_locations = get_cctv_locations_all()
    middle, distance = get_middle_and_distance_based_on_two_points(start_lat, start_lon, end_lat, end_lon)
    cctv_locations_in_area = filter_points_in_distance_of_middle_point(cctv_locations, middle, distance)
    return cctv_locations_in_area


def extract_cctv_coordinates_from_request(response_data):
    cctv_coordinates = []
    response_items = response_data.get('items')
    for element in response_items:
        cctv_coordinates.append((element.get("la"), element.get("lo")))
    return cctv_coordinates


def store_cctv_locations(cctv_locations):
    with open(CCTV_FILE_PATH, 'wb') as f:
        pickle.dump(cctv_locations, f)


def load_cctv_locations():
    with open(CCTV_FILE_PATH, 'rb') as f:
        cctv_locations = pickle.load(f)
    return cctv_locations
