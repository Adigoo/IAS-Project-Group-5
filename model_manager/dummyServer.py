from flask import Flask, jsonify, request, render_template, session, jsonify
import requests
from zipfile import ZipFile
import json

app = Flask(__name__)

@app.route('/')
def home_page():
    response = requests.post("http://127.0.0.1:5003/predict",json={'csv_filename': 'sensor.csv', 'model_name':'model1'})
    print(response.json)
    return "<h1>Dummy Home Page</h1>"

if __name__ == '__main__':
    app.run(debug = True ,port = 5004 )