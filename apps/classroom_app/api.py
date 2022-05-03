import requests
import json
import random

def get_public_ip():
	resp = requests.get("http://api.ipify.org/").content.decode()
	return resp

pub_ip = get_public_ip()
sensor_url = f"http://{pub_ip}:5000/"
model_url = f"http://{pub_ip}:5003/"
controller_url = f"http://{pub_ip}:5002/"

def get_details(name):
	# if name == "attendance_system":
	# 	attendance_system_details = {"sensor_type": "camera","sensor_location": "vindhya-block","no_of_instances": "2","model_name": "attendance_prediction_model","controllers": "[{'controller_type': 'fan', 'controller_location': 'vindhya-block'}, {'controller_type': 'light', 'controller_location': 'vindhya-block'}]"}
	# 	return attendance_system_details

	# if name == "attention_system":
	# 	attention_system_details = {"sensor_type": "camera","sensor_location": "vindhya-block","no_of_instances": "2","model_name": "attention_prediction_model"}
	# 	return attention_system_details
	pass

def get_sensor_data(name):
	# details = get_details(name)
	# jsonObj = {"sensor_type": details["sensor_type"], "sensor_location": details["sensor_location"] }
	# response = requests.post(url=sensor_url+"getSensorInstances", json=jsonObj).content
	# data = json.loads(response.decode())
	# all_instances = data["sensor_instances"]
	# sensor_instances = random.sample(all_instances, str(details["no_of_instances"]))
	# data = []
	# for i in range(len(sensor_instances)):
	# 	jsonObj = {"topic_name": sensor_instances[i]}
	# 	response = requests.post(url=sensor_url+"getSensorData", json=jsonObj).content
	# 	data = json.loads(response.decode())
	# 	data = data["sensor_data"]
	# 	data.append(data[-1])
	# return data
	pass

def predict(name, data):
	# details = get_details(name)
	# jsonObj = {"data": data.tolist(), "model_name": details["model_name"] }
	# response = requests.post(url=model_url+"predict", json=jsonObj).content
	# data = json.loads(response.decode())
	# prediction = data["predicted_value"]
	# return prediction
	pass

def controller_action(name, data):
	# details = get_details(name)
	# results = []
	# for controller in details["controllers"]:
	# 	jsonObj = {"sensor_type": controller["controller_type"], "sensor_location": controller["controller_location"]}
	# 	response = requests.post(url=controller_url+"getControlInstances", json=jsonObj).content
	# 	data = json.loads(response.decode())
	# 	all_instances = data["control_instances"]
	# 	instance = all_instances[0]
	# 	jsonObj = {"sensor_type": instance["sensor_type"], "sensor_ip": instance["sensor_ip"], "sensor_port": instance["sensor_port"], "data": int(data)}
	# 	response = requests.post(url=controller_url+"performAction", json=jsonObj).content
	# 	results.append(response.decode())
	# return results
	pass

