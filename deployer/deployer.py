import logging
from platform import node
import requests
from flask import Flask, jsonify, request
import subprocess
from time import sleep
import pymongo
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

# from rich import print

client = "mongodb://ias_mongo_user:ias_password@cluster0-shard-00-00.doy4v.mongodb.net:27017,cluster0-shard-00-01.doy4v.mongodb.net:27017,cluster0-shard-00-02.doy4v.mongodb.net:27017/ias_database?ssl=true&replicaSet=atlas-ybcxil-shard-0&authSource=admin&retryWrites=true&w=majority"
db_name = "ias_database"
client = pymongo.MongoClient(client)
mydb = client[db_name]
services_config_coll = mydb["services_config"]

app = Flask(__name__)


app.config['SECRET_KEY'] = "SuperSecretKey"
app.config['MONGO_URI'] = "mongodb://ias_mongo_user:ias_password@cluster0-shard-00-00.doy4v.mongodb.net:27017,cluster0-shard-00-01.doy4v.mongodb.net:27017,cluster0-shard-00-02.doy4v.mongodb.net:27017/ias_database?ssl=true&replicaSet=atlas-ybcxil-shard-0&authSource=admin&retryWrites=true&w=majority"


mongo_db = PyMongo(app)
db = mongo_db.db


@app.route('/run', methods=["POST", "GET"])
def runImg():
    print("got request from scheduler")
    recieved_json = request.get_json()
    print(recieved_json)
    service_ports = services_config_coll.find()
    node_service_port = service_ports[0]['node_service']

    print("sending request to node manager")
    resp = requests.get("http://localhost:" +
                        str(node_service_port) + "/getNode").content.decode()

    node_endpoint = resp

    #url = req['url']
    print(f"got back from node manager, response =  {node_endpoint}")
    recieved_json['url'] = node_endpoint
    print(recieved_json)
    recieved_json['fpath'] = 'application_repo/' + recieved_json['app_name']
    print("hello", recieved_json)

    actual_config = db.configuration.find_one(
        {"_id": ObjectId(recieved_json["config_id"])})
    print(f"actual_config = {actual_config}")

    recieved_json["config"] = actual_config

    if '_id' in recieved_json["config"]:
        del recieved_json["config"]['_id']

    # SENDING REQUEST TO NODE
    print(f"node_endpoint = {node_endpoint}")

    url_to_request = f"{node_endpoint}/runapp"
    print(f"url_to_request = {url_to_request}")
    res = requests.post(url=url_to_request,
                        json=recieved_json).json()
    recieved_json['pID'] = res['pID']

    print(f"recieved_json['pID'] = {recieved_json['pID']}")
    # recieved_json["config_id"] = recieved_json["config_id"])
    try:
        db.deployer_log.insert_one(recieved_json)
    except:
        pass
    return 'Requests to the node for deploying'


@app.route('/kill', methods=["POST", "GET"])
def killImg():
    print("In KILL request")
    if request.method == 'POST':
        received_json = request.get_json()
        if received_json is None:
            print("Go GOa GOne\n\n")
            print("Go GOa GOne\n\n")
            print("Go GOa GOne\n\n")
            print("Go GOa GOne\n\n")
            print("Go GOa GOne\n\n")
            print("Go GOa GOne\n\n")
            print("Go GOa GOne\n\n")
            print("Go GOa GOne\n\n")

        logging.debug(f"received_json = {received_json}")
        # data = db.deployer_log.find_one(
        # {"app_name": received_json['app_name']})

        configuration_document = db.deployer_log.find_one(
            {"config_id": received_json["config_id"]})
        pid_to_kill = configuration_document["pID"]
        url_of_node = configuration_document["url"]

        # url = received_json['url']
        logging.debug("got KILL request")
        logging.debug("got KILL request")
        logging.debug("got KILL request")
        logging.debug("got KILL request")
        print(f"recieved_json = {received_json}")
        # print(f"data = {received_json}")
        db.deployer_log.delete_one({'app_name': received_json['app_name']})
        res = requests.post(url=url_of_node + "/killapp",
                            json={'proID': pid_to_kill})
        print(res.content)

    return "Killed"


if __name__ == '__main__':

    service_ports = services_config_coll.find()

    deployer_service_port = service_ports[0]['deployer_service']

    app.run(debug=True, host='0.0.0.0', port=deployer_service_port)
