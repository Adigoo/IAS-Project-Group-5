from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import sensor_manager
import sensor_db
import kafka_manager
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


################################## SENSOR REGISTRATION ########################################

# @app.route("/registerSensorType", methods=["POST"])
# def registerSensorType():
#     sensor_type = request.json
#     sensor_manager.registerSensorType(sensor_type)
#     return json.dumps({"data": "Registered Sensor Type successfully"})


@app.route("/registerSensorInstance", methods=["POST"])
def registerSensorInstance():
    sensor_instance = request.json
    sensor_manager.registerSensorInstance(sensor_instance)
    return json.dumps({"data": "Registered Sensor Instance successfully"})

################################# GET A SENSOR DATA ###########################################

@app.route("/getSensorData", methods=["POST"])
def getSensorData():
    topic_name = request.json['topic_name']
    sensor_data = sensor_manager.getSensorData(topic_name)
    jsonObj = {
        "sensor_data": sensor_data
    }
    return json.dumps(jsonObj)


################################ GET SENSOR DETAILS USING LOCATION #############################

@app.route("/getSensorTypes", methods=["POST"])
def getSensorTypes():
    sensor_location = request.json['sensor_location']
    sensor_types = sensor_manager.getSensorTypes(sensor_location)
    jsonObj = {
        "sensor_types": sensor_types
    }
    return json.dumps(jsonObj)


@app.route("/getSensorInstances", methods=["POST"])
def getSensorInstances():
    sensor_type = request.json['sensor_type']
    sensor_location = request.json['sensor_location']
    sensor_instances = sensor_manager.getSensorInstances(sensor_type, sensor_location)
    jsonObj = {
        "sensor_instances": sensor_instances
    }
    return json.dumps(jsonObj)


############################### GET ALL SENSOR DETAILS #############################################

@app.route("/getAllSensorTypes", methods=["GET", "POST"])
def getAllSensorTypes():
    sensor_types = sensor_manager.getAllSensorTypes()
    jsonObj = {
        "sensor_types": sensor_types
    }
    return json.dumps(jsonObj)

@app.route("/getAllSensorInstances", methods=["GET", "POST"])
def getAllSensorInstances():
    sensor_instances = sensor_manager.getAllSensorInstances()
    jsonObj = {
        "sensor_instances": sensor_instances
    }
    return json.dumps(jsonObj)


################################### MAIN #############################################################

if __name__ == "__main__":
    if sensor_db.databaseExists() == False:
        print("DATABASE CREATED...")
        sensor_manager.register_sensors_from_json("sensor_config.json")
    else:
        print("DATABASE ALREADY EXISTS...")
        kafka_manager.produce_sensors_data()

    app.run(host="0.0.0.0",port=5000, debug=True)
