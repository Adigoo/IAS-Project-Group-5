from urllib import response
from itsdangerous import json
import requests

def getData(topic_name):
    response = requests.post("http://localhost:5000/getSensorData", json={
        "topic_name": topic_name
    })
    print(response.json)

getData()