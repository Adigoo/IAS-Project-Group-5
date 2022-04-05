import requests
import subprocess
#from app_service.app import application_DB
import os
import sys
from datetime import datetime
import threading
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, redirect, flash, render_template
from werkzeug.utils import secure_filename
from time import sleep
sys.path.append('..')
print(sys.path)

UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__))
ALLOWED_EXTENSIONS = set(['json'])
app_path = "../app_service/Application_repository/"
###
UPLOAD_FOLDER = UPLOAD_FOLDER + "/data"
###

in_time = [("A2", "2022-04-02 14:21:30"),
           ("A3", "2022-04-02 14:21:45"), ("A1", "2022-04-02 14:21:55")]
out_time = [("A3", "2022-04-02 14:21:48"),
            ("A1", "2022-04-02 14:21:57"), ("A2", "2022-04-02 14:21:59")]


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../app_service/application_info.db'
app.config['SECRET_KEY'] = "SuperSecretKey"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def add_schedule(filepath):
    f = open(filepath)
    data = json.load(f)
    print(data)

    start_time = data["start-time"]
    end_time = data["end-time"]
    application_name = data["application-name"]

    start_tuple = (application_name, start_time)
    end_tuple = (application_name, end_time)

    in_time.append(start_tuple)
    out_time.append(end_tuple)

    in_time.sort()
    out_time.sort()
    print(in_time)
    return


def createDockerFiles(fpath, aname):
    os.chdir(fpath)
    f = open("Dockerfile", "w+")
    f.write("FROM python:3.8-slim-buster")
    f.write("WORKDIR /"+"aname")
    f.write("COPY ./requirements.txt /var/www/requirements.txt")
    f.write("RUN pip3 install -r /var/www/requirements.txt")
    f.write("COPY . .")
    f.write("EXPOSE 6001")
    f.write("CMD ['python3','-m','flask','run']")

    file = open("requirements.txt", "w+")
    file.write("Flask>=2.0.2\nsklearn\npickle-mixin\nnumpy")


def createDockerImage(fpath, fname):
    os.chdir(fpath)
    command_ = "docker build -t "+fname+" ."
    subprocess.Popen(command_, shell=True)
    sleep(300)


def check_in_time():
    print("thread1")
    count_lis = 0
    while(1):
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        # print("Current Time =", current_time)
        for each_app_time in in_time:
            if(current_time == each_app_time[1]):
                app_path = app_path+"each_app_time[0]"
                createDockerFiles(app_path, each_app_time[0])
                createDockerImage(app_path, each_app_time[0])
                print("Deploy", each_app_time[0])
                requests.post("http://localhost//5000/run",
                              json={'image': each_app_time[0]})
                count_lis += 1
                if(count_lis == len(in_time)):
                    return 0
                sleep(1)


def check_out_time():
    print("thread2")
    count_lis = 0
    while(1):
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")

        for each_app_time in out_time:
            if(current_time == each_app_time[1]):
                print("Deployment time of ", each_app_time[0], " ends")
                requests.post("http://localhost//5000/kill",
                              json={'image': each_app_time[0]})
                count_lis += 1
                if(count_lis == len(out_time)):
                    return 0
                sleep(1)


if __name__ == "__main__":
    t1 = threading.Thread(target=check_in_time)
    t2 = threading.Thread(target=check_out_time)
    t1.start()
    t2.start()

    app.run(debug=True, port=8002)
