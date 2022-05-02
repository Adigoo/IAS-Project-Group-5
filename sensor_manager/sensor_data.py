from email.mime import image
import random
import regex as re
import pymongo

client = "mongodb://ias_mongo_user:ias_password@cluster0-shard-00-00.doy4v.mongodb.net:27017,cluster0-shard-00-01.doy4v.mongodb.net:27017,cluster0-shard-00-02.doy4v.mongodb.net:27017/ias_database?ssl=true&replicaSet=atlas-ybcxil-shard-0&authSource=admin&retryWrites=true&w=majority"
attendance_images = "attendance_images"
attention_images = "attention_images"
db_name = "ias_database"

client = pymongo.MongoClient(client)
mydb = client[db_name]


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

def produceImage(instancesdb):
    images = instancesdb.find()
    imgs = []
    for img in images:
        imgs.append(img['data'])
        # print(img)
    # print(imgs)
    r = random.randint(0, len(imgs))
    return imgs[r]

