# from app_service.app import application_DB
import random
from distutils.command.config import config
import requests
import subprocess
import os
import pytz

import sys
from datetime import datetime
import threading
import json
from flask import Flask, request, redirect, flash, render_template
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
from azurerepo2 import upload_local_file
from time import sleep
import pymongo


from azure.core.exceptions import (
    ResourceExistsError,
    ResourceNotFoundError
)

from azure.storage.fileshare import (
    ShareServiceClient,
    ShareClient,
    ShareDirectoryClient,
    ShareFileClient
)

import logging

#sys.path.append('..')
# logging.warning(sys.path)

# UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__))
ALLOWED_EXTENSIONS = set(['json'])

###
# UPLOAD_FOLDER = UPLOAD_FOLDER + "/data"
###


client = "mongodb://ias_mongo_user:ias_password@cluster0-shard-00-00.doy4v.mongodb.net:27017,cluster0-shard-00-01.doy4v.mongodb.net:27017,cluster0-shard-00-02.doy4v.mongodb.net:27017/ias_database?ssl=true&replicaSet=atlas-ybcxil-shard-0&authSource=admin&retryWrites=true&w=majority"
db_name = "ias_database"
client = pymongo.MongoClient(client)
mydb = client[db_name]
services_config_coll = mydb["services_config"]


share_name = "ias-storage"
connection_string = "DefaultEndpointsProtocol=https;AccountName=iasproject;AccountKey=QmnE09E9Cl6ywPk8J31StPn5rKPy+GnRNtx3M5VC5YZCxAcv8SeoUHD2o1w6nI1cDXgpPxwx1D9Q18bGcgiosQ==;EndpointSuffix=core.windows.net"


in_time = []
out_time = []


app = Flask(__name__)

app.config['SECRET_KEY'] = "SuperSecretKey"
app.config['MONGO_URI'] = "mongodb://ias_mongo_user:ias_password@cluster0-shard-00-00.doy4v.mongodb.net:27017,cluster0-shard-00-01.doy4v.mongodb.net:27017,cluster0-shard-00-02.doy4v.mongodb.net:27017/ias_database?ssl=true&replicaSet=atlas-ybcxil-shard-0&authSource=admin&retryWrites=true&w=majority"


mongo_db = PyMongo(app)
db = mongo_db.db

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def getCurrentTimeInIST():
    IST = pytz.timezone('Asia/Kolkata')
    # print("IST in Default Format : ", datetime.now(IST))
    datetime_ist = datetime.now(IST)
    # print(datetime_ist.strftime('%H:%M'))
    return datetime_ist.strftime("%Y-%m-%d %H:%M:%S")



def add_schedule(json_data):
    logging.warning(getCurrentTimeInIST())
    try:
        app_name = json_data["application-name"]
        logging.warning(app_name)

        

        # data = list(db.configuration.find({"application-name": app_name}))
        # logging.warning(data)
        # data = data[0]
        logging.warning(getCurrentTimeInIST())
        logging.warning(f"data['start-time'] = {json_data['start-time']}")
        start_time = json_data["start-time"]
        end_time = json_data["end-time"]
        application_name = json_data["application-name"]
        config_id = json_data['config_id']
        port_num = json_data['port_num']

        start_tuple = (application_name, start_time, config_id, port_num)
        end_tuple = (application_name, end_time, config_id, port_num)

        in_time.append(start_tuple)
        out_time.append(end_tuple)

        in_time.sort()
        out_time.sort()
        
        logging.warning(f"in_time = {in_time}\n\n")
        logging.warning(f"out_time = {out_time}\n\n")
        logging.warning(f"out_time = {out_time}")
    except Exception as er:
        logging.warning(er)
        logging.warning("error in accessing mongo db in add_schedule")



def check_in_time():
    # app_path = "../app_service/Application_repository/"
    logging.warning("thread1")
    # count_lis = 0
    while(1):
        # now = datetime.now()
        current_time = getCurrentTimeInIST()
        # logging.warning("Current Time =", current_time)
        for each_app_time in in_time:
            if(current_time == each_app_time[1]):
                service_ports = services_config_coll.find()
                deployer_service_port = service_ports[0]['deployer_service']
                # localhost_ip_address = "172.17.0.1"
                pub_ip = requests.get("http://api.ipify.org").content.decode()
                localhost_ip_address = pub_ip
                # localhost_ip_address = "localhost"
                
                logging.warning(f"sending timed request to deployer on {deployer_service_port} port for {each_app_time} \n\n\n")
                logging.warning(f"http://{localhost_ip_address}: + str(deployer_service_port) + '/run'\n\n\n")
                requests.post(
                    f"http://{localhost_ip_address}:" + str(deployer_service_port) + '/run', 
                    json={
                        "app_name": each_app_time[0],
                        "config_id": each_app_time[2],
                        "port_num": each_app_time[3]
                    }
                )
                sleep(1)


def check_out_time():
    logging.warning("thread2")
    # count_lis = 0
    while(1):
        # now = datetime.now()
        # current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        current_time = getCurrentTimeInIST()
        for each_app_time in out_time:
            if(current_time == each_app_time[1]):
                logging.warning("thread2")
                service_ports = services_config_coll.find()
                deployer_service_port = service_ports[0]['deployer_service']

                # service_ports = services_config_coll.find()

                # scheduler_service_port = service_ports[0]['scheduler_service']

                


                json_to_send = {
                    "app_name": each_app_time[0],
                    "config_id": each_app_time[2]
                }
                logging.warning("sending KILL request to deployer\n\n")
                logging.warning(f"json_to_send = {json_to_send}\n\n")

                # localhost_ip_address = "172.17.0.1"
                pub_ip = requests.get("http://api.ipify.org").content.decode()
                localhost_ip_address = pub_ip
                # localhost_ip_address = "localhost"
                requests.post(
                    f"http://{localhost_ip_address}:" + str(deployer_service_port) + '/kill',
                    json=json_to_send
                )
                sleep(1)


def generate_api(data):
    # INPUT_FILE_NAME = "app.json"
    OUTPUT_FILE_NAME = "api.py"

    # input_file = open(INPUT_FILE_NAME)
    output_file = open(OUTPUT_FILE_NAME, "w")

    # data = json.load(input_file)

    # Import statements
    imports = """import requests\nimport json\nimport random\n\nimport pymongo\n"""
    output_file.write(imports)

    # For getting public ip

    get_public_ip = "\n"

    get_public_ip += 'client = "mongodb://ias_mongo_user:ias_password@cluster0-shard-00-00.doy4v.mongodb.net:27017,cluster0-shard-00-01.doy4v.mongodb.net:27017,cluster0-shard-00-02.doy4v.mongodb.net:27017/ias_database?ssl=true&replicaSet=atlas-ybcxil-shard-0&authSource=admin&retryWrites=true&w=majority"\n'
    get_public_ip += 'db_name = "ias_database"\n'
    get_public_ip += 'client = pymongo.MongoClient(client)\n'
    get_public_ip += 'mydb = client[db_name]\n'


    get_public_ip += "\n"

    get_public_ip += "def get_public_ip():\n"
    get_public_ip += '\tvm_ips_coll = mydb["vm_ips"]\n'
    get_public_ip += '\tmodel_vm = vm_ips_coll.find_one({"_id": "servicevm"})\n'
    get_public_ip += '\tmodel_vm_ip = model_vm["vm_ip"]\n'
    get_public_ip += '\tmodel_vm_ip = model_vm_ip.replace(\'"\', "")\n'
    get_public_ip += '\tmodel_vm_ip = model_vm_ip.replace("\'", "")\n'


    # get_public_ip += '\tresp = requests.get("http://api.ipify.org/").content.decode()\n'
    get_public_ip += "\treturn model_vm_ip\n\n"
    output_file.write(get_public_ip)

    # Storing URLs
    service_ports = services_config_coll.find()
    urls = "pub_ip = get_public_ip()\n"

    urls += 'sensor_url = f"http://{pub_ip}:'+ str(service_ports[0]["sensor_service"])+'/"\n'
    urls += 'model_url = f"http://{pub_ip}:'+ str(service_ports[0]["model_service"])+'/"\n'
    urls += 'controller_url = f"http://{pub_ip}:'+ str(service_ports[0]["controller_service"])+'/"\n'
    output_file.write(urls)

    definition = "def get_details(name):\n"
    for function in data["function_details"]:
    # print(function)
        details = data['function_details'][function]
        definition += '\tif name == "'+ function +'":\n'
        definition += '\t\t'+function+'_details = {'
        for key, value in details.items():
            # print(key, value)
            definition += '"' + key + '": "' +str(value) + '",'
        definition = definition[:-1] + '}\n'
        definition += '\t\treturn '+function+'_details\n\n'
    output_file.write(definition)


    sensor_data = 'def get_sensor_data(name):\n'
    sensor_data += '\tdetails = get_details(name)\n'
    sensor_data += '\tjsonObj = {"sensor_type": details["sensor_type"], "sensor_location": details["sensor_location"] }\n'
    sensor_data += '\tresponse = requests.post(url=sensor_url+'+'"getSensorInstances"'+', json=jsonObj).content\n'
    sensor_data += '\tdata = json.loads(response.decode())\n'
    sensor_data += '\tall_instances = data["sensor_instances"]\n'
    sensor_data += '\tsensor_instances = random.sample(all_instances, (details["no_of_instances"]))\n'
    sensor_data += '\tdata = []\n'
    sensor_data += '\tfor i in range(len(sensor_instances)):\n'
    sensor_data += '\t\tjsonObj = {"topic_name": sensor_instances[i]}\n'
    sensor_data += '\t\tresponse = requests.post(url=sensor_url+'+'"getSensorData"'+', json=jsonObj).content\n'
    sensor_data += '\t\tdata = json.loads(response.decode())\n'
    sensor_data += '\t\tdata = data["sensor_data"]\n'
    sensor_data += '\t\tdata.append(data[-1])\n'
    sensor_data += '\treturn data\n\n'
    # print(sensor_data)
    output_file.write(sensor_data)

    predict = 'def predict(name, data):\n'
    predict += '\tdetails = get_details(name)\n'
    predict += '\tjsonObj = {"data": data.tolist(), "model_name": details["model_name"] }\n'
    predict += '\tresponse = requests.post(url=model_url+'+'"predict"'+', json=jsonObj).content\n'
    predict += '\tdata = json.loads(response.decode())\n'
    predict += '\tprediction = data["predicted_value"]\n'
    predict += '\treturn prediction\n\n'
    # print(predict)
    output_file.write(predict)

    controller = 'def controller_action(name, data):\n'
    controller += '\tdetails = get_details(name)\n'
    controller += '\tresults = []\n'
    controller += '\tfor controller in details["controllers"]:\n'
    controller += '\t\tjsonObj = {"sensor_type": controller["controller_type"], "sensor_location": controller["controller_location"]}\n'
    controller += '\t\tresponse = requests.post(url=controller_url+'+'"getControlInstances"'+', json=jsonObj).content\n'
    controller += '\t\tdata = json.loads(response.decode())\n'
    controller += '\t\tall_instances = data["control_instances"]\n'
    controller += '\t\tinstance = all_instances[0]\n'
    controller += '\t\tjsonObj = {"sensor_type": instance["sensor_type"], "sensor_ip": instance["sensor_ip"], "sensor_port": instance["sensor_port"], "data": int(data)}\n'
    controller += '\t\tresponse = requests.post(url=controller_url+'+'"performAction"'+', json=jsonObj).content\n'
    controller += '\t\tresults.append(response.decode())\n'
    controller += '\treturn results\n\n'

    output_file.write(controller)


@app.route("/schedule_model_request", methods=["POST"])
def schedule_model_request():
    received_json = request.get_json()
    # fpath = received_json['fpath']
    # app_name = received_json['app_name']
    # config = received_json['config']
    logging.warning(received_json)

    service_ports = services_config_coll.find()
    deployer_service_port = service_ports[0]['deployer_service']

    logging.warning(
        f"sending immediate request to deployer on {deployer_service_port} port for {received_json['model_name']} \n\n\n"
    )
    
    pub_ip = requests.get("http://api.ipify.org").content.decode()
    localhost_ip_address = pub_ip
    # localhost_ip_address = "localhost"

    logging.warning(f"http://{localhost_ip_address}: + str(deployer_service_port) + '/run'\n\n\n")
    requests.post(
        f"http://{localhost_ip_address}:" + str(deployer_service_port) + '/run', 
        json=received_json
    )
    # pass

    return "Sent immdidate model Request to deployer"

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            logging.warning("scheduler flash('No file part')")
            return redirect(request.url)
        
        file = request.files['file']
        
        
        if file.filename == '':
            flash('No selected file')
            logging.warning("scheduler no selected file")
            return redirect(request.url)

        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            logging.warning(request.files)
            json_data = json.loads(request.files['file'].read().decode('utf-8'))
            generate_api(json_data)

            logging.warning(json_data)
            app_config = list(db.application.find({"_id": json_data['application-name']}))[0]
            flag = True
            if json_data['application-name'] == app_config['_id']:
                # for i in range(len(app_config['sensor'])):
                #     if app_config['sensor'][i]['sensor_type'] != json_data['sensor_details']['sensor_type'][i]:
                #         flag = False
                #         break
                logging.warning(flag)
                if flag:
                    logging.warning("Sensors matched now uploading")
                    retval = None
                    try:
                        retval = db.configuration.insert_one(json_data)
                        logging.warning(f"retval.inserted_id = {retval.inserted_id}")

                        json_data["config_id"] = str(retval.inserted_id)
                    except Exception as er:
                        logging.warning(er)
                        
                    upload_local_file(connection_string, request.files['file'].read(), share_name, 'application_repo/'+ filename.split('.')[0]+ '/'+ filename)
                    # add_schedule(filename.split('.')[0])
                    api_file = open("api.py", "r")
                    upload_local_file(connection_string, api_file.read(), share_name, 'application_repo/'+ filename.split('.')[0]+ '/api.py')

                    app_instance_port =random.randint(50000,50007)
                    json_data['port_num'] = app_instance_port
                    logging.warning(json_data)
                    add_schedule(json_data)

    

    return render_template('index.html')


if __name__ == "__main__":

    t1 = threading.Thread(target=check_in_time)
    t2 = threading.Thread(target=check_out_time)
    t1.start()
    t2.start()

    service_ports = services_config_coll.find()

    scheduler_service_port = service_ports[0]['scheduler_service']

    app.run(debug=True,use_reloader=False, host="0.0.0.0", port=scheduler_service_port)