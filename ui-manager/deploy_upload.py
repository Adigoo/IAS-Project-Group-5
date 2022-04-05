from flask import Flask, jsonify, request, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
import requests
from flask import Flask, request, redirect, url_for, flash, render_template
import os
from werkzeug.utils import secure_filename
from zipfile import ZipFile
import json
from flask_login import LoginManager, UserMixin
import csv
import pickle
import numpy as np
import sklearn

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///model_info.db'
db = SQLAlchemy(app)

ALLOWED_EXTENSIONS = set(['zip'])


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


@app.route('/')
def home_page():
    return render_template('deploy_upload.html')


# @app.route('/model_url', methods=['POST', 'GET'])
# def send_URL():
#     if request.method == 'GET':
#         return "Sending URL for given model type..."
#     json_data = request.get_json()
#     model_type = json_data['model_type']
#     return "http://demo_url"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# def validateZip():
#     pass


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

    return render_template('index.html')


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


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=5003)
