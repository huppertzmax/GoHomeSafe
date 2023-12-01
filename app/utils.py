from geopy.distance import geodesic


def get_middle_and_distance(start_lat, start_lon, end_lat, end_lon):
    start = (start_lat, start_lon)
    end = (end_lat, end_lon)
    middle = ((start_lat + end_lat) / 2, (start_lon + end_lon) / 2)
    distance_start = geodesic(start, middle).meters
    distance_end = geodesic(end, middle).meters
    distance = distance_start if distance_start <= distance_end else distance_end
    return middle, distance


def filter_in_area(points, middle, distance):
    points_in_area = []
    for point in points:
        if geodesic(middle, (point[0], point[1])).meters <= distance:
            points_in_area.append(point)
    return points_in_area


def validate_args(args):
    keys_to_check = ["start_lat", "start_lon", "end_lat", "end_lon"]
    type_check = True
    key_check = all(key in args for key in keys_to_check)
    for key in keys_to_check:
        try:
            float(args.get(key))
        except ValueError:
            type_check = False
    return key_check and type_check