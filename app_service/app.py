from flask import Flask, request, url_for, render_template, jsonify, session, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from werkzeug.utils import secure_filename
from zipfile import ZipFile
import requests
import json
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:0548@localhost/app'
app.config['SECRET_KEY'] = "SuperSecretKey"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

ALLOWED_EXTENSIONS = set(['zip'])


class application_DB(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appName = db.Column(db.String(500), nullable=False, unique=True)
    modelType = db.Column(db.String(500), nullable=False)
    sensorType = db.Column(db.String(5000), nullable=False)
    controllerSensorType = db.Column(db.String(5000), nullable=False)

    def __init__(self, appName, modelType, sensorType, controllerSensorType):
        self.appName = appName
        self.modelType = modelType
        self.sensorType = sensorType
        self.controllerSensorType = controllerSensorType


@app.route('/')
def print_val():
    return "hello"


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_Zip(file_path):
    countjson = 0
    countpy = 0
    with ZipFile(file_path, 'r') as zipObj:
        listOfiles = zipObj.namelist()
        for elem in listOfiles:
            if elem.endswith('.json'):
                countjson += 1
            if elem.endswith('.py'):
                countpy += 1
    if (countjson != 2 or countpy != 1):
        return 0
    return 1


def update_DB(file_path):
    file_name = ""
    with ZipFile(file_path, 'r') as zipObj:
        listOfiles = zipObj.namelist()
        for elem in listOfiles:
            if elem.endswith('application.json'):
                file_name = elem
    zip_obj = ZipFile(file_path, 'r')
    if file_name != "":
        json_obj = zip_obj.open(file_name)
        json_data = json.load(json_obj)
        app_name = json_data['app_name']
        model_type = json_data['model_type']
        sensor_data = ""
        controller_data = ""
        for j_data in json_data['sensor']:
            sensor_data += j_data['sensor_type']+" "
        for j_data in json_data['controller']:
            controller_data += j_data['sensor_type']+" "
        try:
            obj = application_DB(appName=app_name, modelType=model_type,
                                 sensorType=sensor_data, controllerSensorType=controller_data)
            db.session.add(obj)
            db.session.commit()
        except:
            os.remove(file_path)


@app.route('/upload', methods=['GET', 'POST'])
def upload_application():
    if request.method == 'POST':
        UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__))
        UPLOAD_FOLDER = UPLOAD_FOLDER + "/Application_repository"
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if(not os.path.exists(UPLOAD_FOLDER)):
                os.makedirs(UPLOAD_FOLDER)
            try:
                path = os.path.join(UPLOAD_FOLDER, filename)
                print(path.split('.'))
                file.save(path)
                zip_ref = ZipFile(path, 'r')
                zip_ref.extractall(UPLOAD_FOLDER)
                zip_ref.close()
                # os.remove(path)
            except:
                return redirect(request.url)
            if(validate_Zip(os.path.join(UPLOAD_FOLDER, filename)) == 0):
                os.remove(os.path.join(UPLOAD_FOLDER, filename))
                return redirect(request.url)
            update_DB(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('upload_application', filename=filename))

    return render_template('index.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=8082)
