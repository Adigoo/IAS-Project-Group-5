from contextlib import nullcontext
from crypt import methods
import flask
from flask import Flask, render_template, request, flash, redirect, url_for
from importlib_metadata import method_cache
from flask_sqlalchemy import SQLAlchemy
from zipfile import ZipFile
import json
import os
import csv
import numpy as np
import sklearn
from werkzeug.utils import secure_filename
import pickle
from scheduler import *
from flask_login import LoginManager, login_manager, login_user, logout_user, login_required, UserMixin

app = Flask(__name__)
# old database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users.db'
# new databse
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/Users'
# create UserLogin and all entires in mysql and then run the project.
app.config['SECRET_KEY'] = 'secretKey'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


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


class ModelDb(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_name = db.Column(db.String(80), nullable=False)
    model_type = db.Column(db.String(80), nullable=False)
    input_data = db.Column(db.String(80))
    output_data = db.Column(db.String(80))
    url = db.Column(db.String(80))

    def __init__(self, model_name, model_type, input_data, output_data, url):
        self.model_name = model_name
        self.model_type = model_type
        self.input_data = input_data
        self.output_data = output_data
        self.url = url


class UserLogin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    return UserLogin.query.get(int(user_id))


@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        print(request.get_json())
        username = request.form.get('username')
        password = request.form.get('password')
        print(username)
        print(password)
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def about():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        dummy = UserLogin.query.filter_by(email=email).first()
        if dummy:
            return "User already existada"
        else:
            real = UserLogin(name=name, email=email, password=password)
            db.session.add(real)
            db.session.commit()
        return "Register Successfully!"
    return render_template('register.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/form')
def form():
    return render_template("user.html")


@app.route('/model_developer', methods=['POST', 'GET'])
def model_developer():
    return render_template('deploy_upload.html')


@app.route('/app_developer', methods=['POST', 'GET'])
def app_developer():
    return render_template("app_upload.html")


@app.route('/scheduler_upload', methods=['POST', 'GET'])
def scheduler_upload():
    return render_template("scheduler_upload.html")


@app.route('/sensor_upload', methods=['POST', 'GET'])
def sensor_upload():
    return render_template("sensor_instance_register.html")


@app.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')

    dummy = UserLogin.query.filter_by(email=email).first()
    if dummy:
        if password == dummy.password:
            login_user(dummy)
            return render_template('home.html')
    else:
        return "Invalid Credentials"
    return "The email is {} and the password is {}".format(email, password)


@app.route('/signout')
@login_required
def signout():
    logout_user()
    return "Sign out successful"


# Model Manager *************************************************
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def uploadConfig(file_path):
    model_file_name = ''
    with ZipFile(file_path, 'r') as zipObj:
        listOfiles = zipObj.namelist()
        for elem in listOfiles:
            if elem.endswith('.json'):
                if elem.endswith('model_config.json'):
                    model_file_name = elem

    if model_file_name != '':
        zip_obj = ZipFile(file_path, 'r')
        model_json_obj = zip_obj.open(model_file_name)
        json_data = json.load(model_json_obj)
        print(json_data)

        model_data = json_data['model'][0]
        name = model_data['model_name']
        type = model_data['model_type']
        input = ''
        output = ''
        url = 'localhost:5004'
        obj = ModelDb(model_name=name, model_type=type,
                      input_data=input, output_data=output, url=url)
        db.session.add(obj)
        db.session.commit()

    '''
    {'model': [{'model_name': 'modelA', 'model_type': 'type1'}]}
    model_data = []

    for j_data in json_data['model']:
        model_data.append(j_data['model_type'])
    print(model_data)'''


@app.route('/upload_model', methods=['POST', 'GET'])
def uploadModel():
    if request.method == 'POST':
        UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__))
        UPLOAD_FOLDER = UPLOAD_FOLDER + "/Model_repository"
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            ######
            #directory = str(filename)

            #path = os.path.join(UPLOAD_FOLDER, directory)

            # Create the directory
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            ######

            file.save(os.path.join(UPLOAD_FOLDER, filename))
            unzip_folder = os.path.join(UPLOAD_FOLDER, filename)
            # upload unzipped folder

            zip_ref = ZipFile(unzip_folder, 'r')
            zip_ref.extractall(UPLOAD_FOLDER)
            zip_ref.close()

            uploadConfig(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('uploadModel', filename=filename))

    return render_template('home.html')


@app.route('/predict', methods=['POST'])
def predictOutput():
    json_data = request.get_json()
    csv_file_path = json_data['csv_filename']
    model_name = json_data['model_name']
    print(csv_file_path)
    csv_file = open(csv_file_path)
    csv_reader = csv.reader(csv_file)
    rows = []
    for row in csv_reader:
        #print(type(row), row, len(row))
        rows.append(int(row[0]))

    print(rows)

    cur_directory = os.getcwd()
    new_path = cur_directory + '/Model_repository/' + \
        model_name + '/' + model_name + '.pkl'
    pickle_file = open(new_path, 'rb')
    AI_model = pickle.load(pickle_file)
    prediction_data = AI_model.predict(np.array([rows]))
    print(prediction_data[0])
    return jsonify({"predicted value": prediction_data[0]})


# ***************************************************************

# *********APP MANAGER ******************************
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


@app.route('/upload_app', methods=['GET', 'POST'])
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

    return render_template('home.html')


# ***************************************************

# **********Scheduler Manager**********************
@app.route('/scheduler_upload', methods=['GET', 'POST'])
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
                    if sensorStr[i] == data['sensors'][i]['type']:
                        continue
                    else:
                        flag = False
                        break
                if not flag:
                    return "Invalid Configuration"
                else:
                    fileobj = open("../app_service/Application_repository/" +
                                   data['application-name'] + '/config', 'w')
                    for i in data['sensors']:
                        fileobj.write(i['type'] + " ")
                    fileobj.write("\n")
                    for i in data['sensors']:
                        fileobj.write(i['location'] + " ")
                    fileobj.close()
            print(data)
            return "Request uploaded"
    return render_template('index.html')


# *************************************************

# *********User form*********************
@app.route('/form_uploader', methods=['POST', 'GET'])
def deploy_uploader():
    if request.method == 'POST':
        # try:
        #     login_flag = session['loggedin_user']
        # except Exception:
        #     error = "No Logged in User"
        #     #appinfo = getappinfostr()
        #     return render_template('index.html')

        # username = session['username_user']

        appid = request.form.get('appid')
        mtype = request.form.get('mtype')
        stype = request.form.get('stype')
        sloc = request.form.get('sloc')
        ctype = request.form.get('ctype')
        cloc = request.form.get('cloc')
        stime = request.form.get('stime')
        etime = request.form.get('etime')

        form_data = {
            "application-name": appid,
            "age": mtype,
            "start-time": stime,
            "end-time": etime,
            "sensors": [{"type": stype, "location": sloc}],
            "controllers": [{"type": ctype, "location": cloc}]
        }
        print(form_data['application-name'])
        form_json = json.dumps(form_data, indent=4)
        print(form_json)

        with open("app1.json", "w") as outfile:
            outfile.write(form_json)

        return redirect(url_for('deploy_uploader'))
    return render_template('home.html')


# **************************************
# @app.route('/demo/<id>')
# def demo(id):
#    return "Id is "+ id
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
