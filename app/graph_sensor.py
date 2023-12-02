from sensor import *

SENSOR_WEIGHT_POSITIVE_C1 = 0.75
SENSOR_WEIGHT_POSITIVE_C2 = 0.5
SENSOR_WEIGHT_POSITIVE_C3 = 0.1
SENSOR_WEIGHT_NEGATIVE_C1 = 1.25
SENSOR_WEIGHT_NEGATIVE_C2 = 1.5
SENSOR_WEIGHT_NEGATIVE_C3 = 1.75


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
        sensor_value = get_sensor_value(sensor.get('sensor_id'))
        if sensor_value > sensor_min:
            change_weights(
                graph=graph,
                start_node=sensor.get('start_node'),
                end_node=sensor.get('end_node'),
                key=sensor.get('key'),
                c1_weight=SENSOR_WEIGHT_POSITIVE_C1,
                c2_weight=SENSOR_WEIGHT_POSITIVE_C2,
                c3_weight=SENSOR_WEIGHT_POSITIVE_C3
            )
            reason = "loud"
            count_pos += 1
        else:
            change_weights(
                graph=graph,
                start_node=sensor.get('start_node'),
                end_node=sensor.get('end_node'),
                key=sensor.get('key'),
                c1_weight=SENSOR_WEIGHT_NEGATIVE_C1,
                c2_weight=SENSOR_WEIGHT_NEGATIVE_C2,
                c3_weight=SENSOR_WEIGHT_NEGATIVE_C3
            )
            reason = "silent"
            count_neg += 1
        graph[sensor.get('start_node')][sensor.get('end_node')][sensor.get('key')]['reason'] = reason
    return count_pos, count_neg
