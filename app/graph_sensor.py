from sensor import *

SENSOR_WEIGHT_POSITIVE = 0.75
SENSOR_WEIGHT_NEGATIVE = 1.25


def adjust_graph_weights_sensor(graph, sensor_min):
    # @TODO change according to graph_cctv.py
    sensors = load_sensor_locations()
    count_pos, count_neg = adjust_sensor_weights(graph, sensors, sensor_min)
    print("----------- SENSORS -----------")
    print(len(sensors))
    print(sensors)
    print("Weights for " + str(len(sensors)) + " edges were adjusted based on sensor data")
    print(str(count_pos) + " of them safe and " + str(count_neg) + " of them unsafe")
    print("----------- END SENSORS -----------")


def adjust_sensor_weights(graph, sensors, sensor_min):
    count_pos = 0
    count_neg = 0
    for sensor in sensors:
        c_weight = graph[sensor.get('start_node')][sensor.get('end_node')][sensor.get('key')]['c_weight']
        sensor_value = get_sensor_value(sensor.get('sensor_id'))
        if sensor_value > sensor_min:
            weight = SENSOR_WEIGHT_POSITIVE
            reason = "loud"
            count_pos = count_pos + 1
        else:
            weight = SENSOR_WEIGHT_NEGATIVE
            reason = "silent"
            count_neg = count_neg + 1
        c_weight = c_weight * weight
        graph[sensor.get('start_node')][sensor.get('end_node')][sensor.get('key')]['c_weight'] = c_weight
        graph[sensor.get('start_node')][sensor.get('end_node')][sensor.get('key')]['reason'] = reason
    return count_pos, count_neg
