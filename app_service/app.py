from flask import Flask, request, url_for, render_template, jsonify, session, flash, redirect
from flask_pymongo import PyMongo
from io import BytesIO
from werkzeug.utils import secure_filename
from zipfile import ZipFile
import requests
import json
import os

from azurerepo2 import create_directory, upload_local_file

from azure.core.exceptions import (
    ResourceExistsError,
    ResourceNotFoundError
)

from azure.storage.fileshare import (
    ShareServiceClient,
    ShareClient,
    ShareDirectoryClient,
    ShareFileClient
)

share_name = "ias-storage"
connection_string = "DefaultEndpointsProtocol=https;AccountName=iasproject;AccountKey=QmnE09E9Cl6ywPk8J31StPn5rKPy+GnRNtx3M5VC5YZCxAcv8SeoUHD2o1w6nI1cDXgpPxwx1D9Q18bGcgiosQ==;EndpointSuffix=core.windows.net"

# Create a ShareServiceClient from a connection string
service_client = ShareServiceClient.from_connection_string(connection_string)

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://ias_mongo_user:ias_password@cluster0.doy4v.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
app.config['SECRET_KEY'] = "SuperSecretKey"

mongo_db = PyMongo(app)
db = mongo_db.db

ALLOWED_EXTENSIONS = set(['zip'])

@app.route('/')
def print_val():
    return "hello"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_Zip(zipObj):
    countjson = 0
    countpy = 0
    listOfiles = zipObj.namelist()
    for elem in listOfiles:
        if elem.endswith('.json'):
            countjson += 1
        if elem.endswith('.py'):
            countpy += 1
    if (countjson != 1 or countpy != 1):
        return 0
    return 1


@app.route('/upload', methods=['GET', 'POST'])
def upload_application():
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
            share_client = ShareClient.from_connection_string(connection_string, share_name)
            flag = True
            for item in list(share_client.list_directories_and_files('application_repo')):
                print(item['name'])
                if item["is_directory"]:
                    print("Directory:", item["name"])
                    if item["name"] == filename.split('.')[0]:
                        flag = False
            if flag:
                zipfile = ZipFile(file._file)
                if validate_Zip(zipfile):
                    create_directory(connection_string, share_name, 'application_repo/' + filename.split('.')[0])
                    print(zipfile.namelist())
                    fileslist = zipfile.namelist()[1:]
                    for name in fileslist:
                        print(name)
                        newfile = zipfile.read(name)
                        print('application_repo/' + name)
                        upload_local_file(connection_string, newfile, share_name, 'application_repo/' + name)
                        #print(name.split)
                        if name.split('/')[1] == "application.json": 
                            json_data = json.loads(newfile.decode('utf-8'))
                            print(json_data)
                            json_data['_id'] = json_data['app_name']
                            db.application.insert_one(json_data)
                else:
                    return "Improper Zip format"
            else:
                return "Application with similar name already exists."
            return redirect(url_for('upload_application'))

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=8082)
