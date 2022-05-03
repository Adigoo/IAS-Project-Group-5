import requests
import json
import random

import pymongo

client = "mongodb://ias_mongo_user:ias_password@cluster0-shard-00-00.doy4v.mongodb.net:27017,cluster0-shard-00-01.doy4v.mongodb.net:27017,cluster0-shard-00-02.doy4v.mongodb.net:27017/ias_database?ssl=true&replicaSet=atlas-ybcxil-shard-0&authSource=admin&retryWrites=true&w=majority"
db_name = "ias_database"
client = pymongo.MongoClient(client)
mydb = client[db_name]

def get_public_ip():
	vm_ips_coll = mydb["vm_ips"]
	model_vm = vm_ips_coll.find_one({"_id": "servicevm"})
	model_vm_ip = model_vm["vm_ip"]
	model_vm_ip = model_vm_ip.replace('"', "")
	model_vm_ip = model_vm_ip.replace("'", "")
	return model_vm_ip

