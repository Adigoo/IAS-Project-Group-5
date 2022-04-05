import requests
import subprocess
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
from app_service.app import application_DB
# print(sys.path)

UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__))
ALLOWED_EXTENSIONS = set(['json'])

###
UPLOAD_FOLDER = UPLOAD_FOLDER + "/data"
###

in_time = [("A2", "2022-04-02 14:21:30"),
           ("A3", "2022-04-02 14:21:45"), ("A1", "2022-04-02 14:21:55")]
out_time = [("A3", "2022-04-02 14:21:48"),
            ("A1", "2022-04-02 14:21:57"), ("A2", "2022-04-02 14:21:59")]


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:0548@localhost/app'
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
    print(os.getcwd())
    os.chdir(os.path.realpath(fpath))
    print(os.getcwd())
    file = open("requirements.txt", "w+")
    file.write("Flask>=2.0.2\nsklearn\npickle-mixin\nnumpy\nrequests")
    f = open("Dockerfile", "w+")
    f.write("FROM python:3.8-slim-buster")
    f.write("\nWORKDIR /"+aname)
    f.write("\nCOPY ./requirements.txt /var/www/requirements.txt")
    f.write("\nRUN pip3 install -r /var/www/requirements.txt")
    f.write("\nCOPY . .")
    f.write("\nEXPOSE 6001")
    f.write('\nCMD ["python3","-m","flask","run"]')


def createDockerImage(fpath, fname):
    # os.chdir(fpath)
    command_ = "echo 0548 | sudo -S docker build -t " + fname + " ."
    subprocess.Popen(command_, shell=True)
    sleep(100)


def check_in_time():
    app_path = "../app_service/Application_repository/"
    print("thread1")
    count_lis = 0
    while(1):
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        # print("Current Time =", current_time)
        for each_app_time in in_time:
            if(current_time == each_app_time[1]):
                app_path = app_path+each_app_time[0]+"/"
                copy_cmd = "cp ../api.py "+app_path+""
                subprocess.Popen(copy_cmd, shell=True)
                createDockerFiles(app_path, each_app_time[0])
                createDockerImage(app_path, each_app_time[0])
                print("Deploy", each_app_time[0])
                requests.post("http://localhost:9000/run",
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
                requests.post("http://localhost:9000/kill",
                              json={'image': each_app_time[0]})
                count_lis += 1
                if(count_lis == len(out_time)):
                    return 0
                sleep(1)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            directory = str(filename.split('.')[0])
            path = os.path.join(UPLOAD_FOLDER, directory)
            os.makedirs(path)
            file.save(os.path.join(path, filename))
            print(filename, directory)

            # file.save("../app_service/Application_repository/"+directory+"/"+filename)
            cpy_cmd = "cp data/"+directory+"/" + filename + \
                " ../app_service/Application_repository/"+directory+"/"+filename
            subprocess.Popen(cpy_cmd, shell=True)

            add_schedule(os.path.join(path, filename))
            print("Upload complete")
            json_obj = open('./data/' + file.filename.split('.')
                            [0] + '/' + file.filename)
            data = json.load(json_obj)
            app_obj = application_DB.query.filter_by(
                appName=data['application-name']).first()
            if app_obj:
                sensorStr = app_obj.sensorType.split()
                flag = True
                for i in range(len(sensorStr)):
                    if sensorStr[i] == data['sensor_details']['sensor_type'][i]:
                        continue
                    else:
                        flag = False
                        break
                if not flag:
                    return "Invalid Configuration"
                # else:
                #     fileobj = open("../app_service/Application_repository/" +
                #                    data['application-name'] + '/config', 'w')
                #     i = data['sensor_details']
                #     for j in i['sensor_type']:
                #         fileobj.write(j + " ")
                #     fileobj.write("\n")
                #     fileobj.write(i['sensor_location'])
                #     fileobj.write("\n")
                #     fileObj.write(i['no_of_instances'])
                #     fileobj.close()
            print(data)
            return "Request uploaded"
    return render_template('index.html')


if __name__ == "__main__":
    t1 = threading.Thread(target=check_in_time)
    t2 = threading.Thread(target=check_out_time)
    t1.start()
    t2.start()

    app.run(debug=True, port=8003)
