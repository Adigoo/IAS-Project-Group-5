from urllib import response
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import sensor_manager
import sensor_db
import kafka_manager
import json
import pymongo

client = "mongodb://ias_mongo_user:ias_password@cluster0-shard-00-00.doy4v.mongodb.net:27017,cluster0-shard-00-01.doy4v.mongodb.net:27017,cluster0-shard-00-02.doy4v.mongodb.net:27017/ias_database?ssl=true&replicaSet=atlas-ybcxil-shard-0&authSource=admin&retryWrites=true&w=majority"
db_name = "ias_database"
client = pymongo.MongoClient(client)
mydb = client[db_name]
services_config_coll = mydb["services_config"]


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


################################## SENSOR REGISTRATION ########################################

@app.route("/registerSensorType", methods=["POST"])
def registerSensorType():
    data = request.json
    new_type = data['sensor_type']
    # Check if the sensor type already exists
    sensor_types = sensor_manager.getAllSensorTypes()
    res = ""
    if new_type in sensor_types:
        res = "Sensor type already exists !!"
    else:
        sensor_manager.registerSensorType(data)
        res = "Sensor type registered successfully !!"

    return json.dumps({"data": res})


@app.route("/registerSensorInstance", methods=["POST"])
def registerSensorInstance():
    sensor_instance = request.json
    # Checking if the sensor type exists or not
    new_type = sensor_instance['sensor_type']
    sensor_types = sensor_manager.getAllSensorTypes()
    if new_type not in sensor_types:
        res = "Sensor type doesnot exists !!"
    else:
        sensor_manager.registerSensorInstance(sensor_instance)
        res = "Sensor instance registered successfully !!"

    return json.dumps({"data": res})

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
        print("Sensor Collection CREATED...")
        sensor_manager.register_sensors_from_json("sensor_config.json")
    else:
        print("DATABASE ALREADY EXISTS...")
        kafka_manager.produce_sensors_data()
    
    service_ports = services_config_coll.find()

    sensor_service_port = service_ports[0]['sensor_service']

    app.run(debug=True, host='0.0.0.0', port=sensor_service_port)

