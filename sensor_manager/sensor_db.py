import json
from pydoc_data.topics import topics
from sys import api_version
import pymongo
import threading
import sensor_data
from pydoc import doc

client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = client["SensorDatabase"]
instancesdb = mydb["SensorInstances"]
# types = mydb["SensorTypes"]

# Deprecated
# def register_sensor_type(sensor_type):
#     types = mydb["SensorTypes"]
#     types.insert_one(sensor_type)

################################ DATABASE CREATION and DROPPING ################################

def databaseExists():
    databases = client.list_database_names()
    if 'SensorDatabase' in databases:
        return True
    else:
        return False
        # register_sensors_from_json('sensor_config.json')


def drop_db():
    instancesdb.drop()
    client.drop_database("SensorDatabase")


def getCount(collectionObj):
    '''Returns no.of documents in the given collection object'''
    return collectionObj.count_documents({})

################################ REGISTRATION OF SENSORS ########################################

def register_sensor_instance(sensor_instance):
    '''Stores the given sensor_instance in the collection'''
    count = getCount(instancesdb)
    sensor_instance['_id'] = count+1
    instancesdb.insert_one(sensor_instance)
    topic_name = sensor_instance["sensor_type"] + '_' + str(sensor_instance['_id'])
    return topic_name

################################# RETRIEVING DETAILS OF ALL SENSORS ######################

def get_all_sensor_types():
    sensor_types = set()
    for document in instancesdb.find():
        sensor_types.add(document['sensor_type'])
    sensor_types = list(sensor_types)
    return sensor_types


def get_all_sensor_instances():
    sensor_instances = []
    for document in instancesdb.find():
        # instance = {"sensor_type": document['sensor_type'], "id": document['_id']}
        sensor_instances.append(document)
    return sensor_instances

############################### RETRIEVING BASED ON LOCATION ############################

def get_sensor_types(sensor_location):
    sensor_types = set()
    for document in instancesdb.find():
        if document['sensor_location'] == sensor_location:
            sensor_types.add(document['sensor_type'])
    sensor_types = list(sensor_types)
    return sensor_types
    

def get_sensor_instances(sensor_type, sensor_location):
    sensor_instances = []
    for document in instancesdb.find():
        if document['sensor_type'] == sensor_type and document['sensor_location'] == sensor_location:
            sensor_name = document['sensor_type'] + '_' + str(document['_id'])
            sensor_instances.append(sensor_name)
    return sensor_instances

#################################################################################################

# drop_db()
# register_sensors_from_json('sensor_config.json')
