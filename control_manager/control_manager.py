import control_db
import json
import requests

def perform_action(sensor_type, sensor_location):
    ip, port = control_db.get_ip_and_port(sensor_type, sensor_location)
    response = requests.get('http://localhost:'+str(port)+'/performAction').content
    # print(response)
    return response.decode()

def register_control_instance(instance):
    control_db.register_control_instance(instance)

def register_controllers_from_json(path):
    f = open(path)
    controllers = json.load(f)
    for instance in controllers['control_instances']:
        register_control_instance(instance)

def get_control_instances(sensor_type, sensor_location):
    return control_db.get_control_instances(sensor_type, sensor_location)