from urllib import response
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from itsdangerous import json
import control_db
import control_manager
import requests

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


################################## SENSOR REGISTRATION ########################################

@app.route("/performAction", methods=["GET", "POST"])
def performAction():
    instance = request.json
    url = "http://" + instance["sensor_ip"] + ":" + str(instance["sensor_port"]) +"/"
    if instance["sensor_type"] == "fan":
        url += "fanAction"
    elif instance["sensor_type"] == "ac":
        url += "acAction"
    response = requests.post(url, json={
        "data": instance["data"]
    }).content
    return response.decode()

@app.route("/getControlInstances", methods=["POST"])
def getControlInstances():
    sensor_type = request.json['sensor_type']
    sensor_location = request.json['sensor_location']
    control_instances = control_manager.get_control_instances(sensor_type, sensor_location)
    jsonObj = {
        "control_instances": control_instances
    }
    return json.dumps(jsonObj)

################################### MAIN #############################################################

if __name__ == "__main__":
    if control_db.databaseExists() == False:
        print("DATABASE CREATED...")
        control_manager.register_controllers_from_json("control_config.json")
    
    app.run(host="0.0.0.0",port=6000, debug=True)
