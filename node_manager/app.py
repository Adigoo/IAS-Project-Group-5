import logging
from flask_pymongo import PyMongo
from flask import Flask, request, jsonify
import threading
import json
import time
import pymongo
import requests
import sys
import socket

client = "mongodb://ias_mongo_user:ias_password@cluster0-shard-00-00.doy4v.mongodb.net:27017,cluster0-shard-00-01.doy4v.mongodb.net:27017,cluster0-shard-00-02.doy4v.mongodb.net:27017/ias_database?ssl=true&replicaSet=atlas-ybcxil-shard-0&authSource=admin&retryWrites=true&w=majority"
db_name = "ias_database"
client = pymongo.MongoClient(client)
mydb = client[db_name]
nodes_collection = mydb["nodes_collection"]
services_config_coll = mydb["services_config"]

app = Flask(__name__)
app.config['DEBUG'] = True

app.config['MONGO_URI'] = "mongodb://ias_mongo_user:ias_password@cluster0-shard-00-00.doy4v.mongodb.net:27017,cluster0-shard-00-01.doy4v.mongodb.net:27017,cluster0-shard-00-02.doy4v.mongodb.net:27017/ias_database?ssl=true&replicaSet=atlas-ybcxil-shard-0&authSource=admin&retryWrites=true&w=majority"


mongo_db = PyMongo(app)
db = mongo_db.db


#####################################################################
#####################################################################
#####################################################################
#####################################################################
#####################################################################

def json_deserializer(data):
    return json.dumps(data).decode('utf-8')


def json_serializer(data):
    return json.dumps(data).encode("utf-8")


@app.route('/getNode', methods=['POST', 'GET'])
def getNode():

    # f=open("node.json")

    # 3
    service_ports = services_config_coll.find()

    node_service_port = service_ports[0]['node_service']

    logging.warning("REACHED TILL DATA array")

    data = []
    try:
        
        vm_ips_coll = mydb["vm_ips"]
        model_vm = vm_ips_coll.find_one(
            {"_id": "modelvm"}
        )

        logging.warning(f"model_vm = {model_vm}")
        # logging.warning(f"model_vm = {model_vm.keys()}")
        logging.warning(f'model_vm["vm_ip"] = {model_vm["vm_ip"]}')

        app_vm = vm_ips_coll.find_one(
            {"_id": "appvm"}
        )

        # print(actual_config)
        model_vm_ip = model_vm["vm_ip"]
        logging.warning(f'model_vm["vm_ip"] = {model_vm["vm_ip"]}')
        model_vm_ip = model_vm_ip.replace('"', '')
        model_vm_ip = model_vm_ip.replace("'", '')
        # to remove redundant double quotes
        app_vm_ip = app_vm["vm_ip"]
        logging.warning(f'app_vm["vm_ip"] = {app_vm["vm_ip"]}')
        app_vm_ip = app_vm_ip.replace('"', '')
        app_vm_ip = app_vm_ip.replace("'", '')

        # data = [model_vm_ip, app_vm_ip]
        data.append(model_vm_ip)
        data.append(app_vm_ip)

        logging.warning(f"data = {data}")
    except Exception as er:
        logging.warning(er)
        logging.warning("SOME exception occurred")
        pass

    node_list = list()

    for node_ip in data:
        # logging.warning(node['ip'])
        # logging.warning(node['port'])
        logging.warning(f"node_ip = {node_ip}")

        # node_ip = node['ip']
        node_port = "5000"
        node_list.append(f"http://{node_ip}:{node_port}")
    # 3
    logging.warning(f"node_list = {node_list}")

    loads = {}
    # data=json.load(f)
    # ni=data["node"]
    # logging.warning(ni)
    for item in node_list:
        logging.warning(f"trying to get loads")
        rgl = item+"/getLoad"
        req = requests.get(url=rgl).json()
        cl = str(req['cpu_load'])
        cm = str(req['mem_load'])
        tup = (cm, cl)
        loads[item] = tup
    
    srt = sorted([(value, key) for (key, value) in loads.items()])
    # logging.warning()



    rdf = srt[0]
    ke = list(loads.keys())
    logging.warning(ke[0])
    logging.warning(f"Deploy on {ke[0]} file=sys.stderr")
    logging.warning(cl+"\t"+cm)
    return ke[0]

@app.route("/addNode", methods=['POST', 'GET'])
def addNode():
    data  = request.get_json()
    new_node_ip = data["ip"]
    new_node_port = data["port"]
    data['_id'] = data["ip"]
    # nodes_collection = mydb["nodes_collection"]
    nodes_collection.insert_one(data)
    return "added successfully"

if __name__ == "__main__":
    # logging.warning(f"resp = {get_node_for_deployment().decode()}")

    # getNode()

    service_ports = services_config_coll.find()
    node_service_port = service_ports[0]['node_service']
    app.run(debug=True,use_reloader=False, host='0.0.0.0', port=node_service_port)
