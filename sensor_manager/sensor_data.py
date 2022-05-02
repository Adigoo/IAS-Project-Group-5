from email.mime import image
import random
import regex as re
import pymongo
import numpy as np

client = "mongodb://ias_mongo_user:ias_password@cluster0-shard-00-00.doy4v.mongodb.net:27017,cluster0-shard-00-01.doy4v.mongodb.net:27017,cluster0-shard-00-02.doy4v.mongodb.net:27017/ias_database?ssl=true&replicaSet=atlas-ybcxil-shard-0&authSource=admin&retryWrites=true&w=majority"
db_name = "ias_database"

client = pymongo.MongoClient(client)
mydb = client[db_name]
instancesdb = mydb["attendance_images"]


def produceData(sensor_type):
    if re.match('^temp', sensor_type):
        return produceTempData()
    elif re.match('^light', sensor_type):
        return produceLightData()
    elif re.match('^camera', sensor_type):
        return produceImage()

def produceTempData():
    temp = random.randint(0, 30)
    return temp

def produceLightData():
    brightness = random.randint(0, 10)
    return brightness

def produceImage():
    rand = random.randint(0, 90)
    images = instancesdb.find({"id": rand})
    for i in images:
        img = i["data"]
        return img
        
# produceImage()

