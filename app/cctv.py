import requests
from geopy.distance import geodesic


def request_cctv_locations():
    api_url = 'https://www.seogu.go.kr/seoguAPI/3660000/getCctvLifeSecrty'
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        data = data.get('response').get('body')
        return data
    else:
        print("Error: CCTV data could not be loaded")


def get_cctv_locations_all():
    return jsonfiy_locations(request_cctv_locations())


def get_cctv_locations_area(start_lat, start_lon, end_lat, end_lon):
    # @TODO change back to normal when adjusting user interface
    start = (start_lat, start_lon)
    end = (end_lat, end_lon)
    middle = ((start_lat + end_lat)/2, (start_lon + end_lon)/2)
    distance_start = geodesic(start, middle).meters
    distance_end = geodesic(end, middle).meters
    distance = distance_start if distance_start <= distance_end else distance_end
    cctv_locations = list_cctv_coordinates(request_cctv_locations())

    cctv_locations = filter_cctvs_in_area(cctv_locations, middle, distance)
    return cctv_locations


def list_cctv_coordinates(data):
    cctv_coordinates = []
    response_items = data.get('items')
    for element in response_items:
        cctv_coordinates.append((element.get("la"), element.get("lo")))
    return cctv_coordinates


def filter_cctvs_in_area(cctvs, middle, distance):
    cctvs_in_area = []
    for cctv in cctvs:
        if geodesic(middle, cctv).meters <= distance:
            cctvs_in_area.append(cctv)
    return cctvs_in_area


def jsonfiy_locations(data):
    amount = data.get('totalCnt')
    response_items = data.get('items')
    cctv_list = []
    for element in response_items:
        e = {"lat": element.get("la"), "lon": element.get("lo")}
        cctv_list.append(e)
    return {"count": amount, "cctvs": cctv_list}