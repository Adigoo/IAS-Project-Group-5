import random
import regex as re

def produceData(sensor_type):
    if re.match('^temp', sensor_type):
        return produceTempData()
    elif re.match('^light', sensor_type):
        return produceLightData()
    elif re.match('^humidity', sensor_type):
        return produceHumidityData()
    
def produceTempData():
    temp = random.randint(0, 30)
    return temp

def produceLightData():
    brightness = random.randint(0, 10)
    return brightness

def produceHumidityData():
    humidity = random.randint(20, 100)
    return humidity
