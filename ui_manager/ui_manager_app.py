import os
from flask import Flask, render_template, request, flash, redirect, url_for, session
import requests
import socket
import random
import json
import sensor_type_validator
import sensor_instance_validator

import flask
from flask import Flask, render_template, request, flash, redirect, url_for
from importlib_metadata import method_cache
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager, login_user, logout_user, login_required, UserMixin


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users.db'

app.config['SECRET_KEY'] = 'secretKey'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


class UserLogin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def get_id(self):
        return self.id

    def is_active(self):
        return self.is_active

    def activate_user(self):
        self.is_active = True

    def get_username(self):
        return self.username

    def get_email(self):
        return self.email


@login_manager.user_loader
def load_user(user_id):
    return UserLogin.query.get(int(user_id))


# APIS

@app.route("/")
def root():
    return render_template('login.html')


# signup
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        print("in register post")
        username = request.form.get('username')
        # roll = request.form.get('roll')
        email = request.form.get('email')
        password = request.form.get('password')

        print(username, email, password)

        does_user_exist = UserLogin.query.filter_by(username=username).first()
        if does_user_exist:
            print("Signup failed")

            return render_template('register.html', error="username exists.")
        else:
            real = UserLogin(username=username, email=email, password=password)
            db.session.add(real)
            db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')


# signup_success


@app.route("/signup_success")
def signup_success():
    pass


@app.route("/login", methods=["GET", "POST"])
def login():
    print("in login method")
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username, password)

        check_user = UserLogin.query.filter_by(username=username).first()
        print(f"check_user = {check_user}")
        if(check_user is not None):
            # if current_user.is_authenticated:
            #     resp['msg'] = 'Already logged in.'
            #     resp['role'] = check_user.urole
            #     return redirect()
            print("checking password")
            if(check_user.password == password):
                login_user(check_user)
                print("password match")
                # resp['msg'] = 'Logged in successfully'
                # resp['role'] = check_user.urole
                return redirect(url_for('home'))
            else:
                # resp['msg'] = 'Incorrect password'
                # resp['role'] = 'not logged in'
                return render_template('login.html', error=error)
        else:
            # resp['msg'] = "No such User exists"
            # resp['role'] = 'not logged in'
            return render_template('login.html', error=error)

    else:
        return render_template('login.html', error=error)


# logout
@app.route("/logout")
@login_required
def logout():
    print("in logout")
    logout_user()
    return redirect(url_for('login'))


# home

@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    return render_template('home.html')


# sensor_type_upload
@app.route("/sensor_type_upload", methods=["GET", "POST"])
@login_required
def sensor_type_upload():
    if request.method == "POST":
        print("IN SENSOR TYPE UPLOAD REQUEST")
        uploaded_file = request.files['customFile']
        # uploaded_file = request.form.get('customFile')

        try:
            shutil.rmtree("temp/")
        except Exception:
            pass

        os.mkdir("temp")

        if uploaded_file.filename != '':

            name = "temp/" + uploaded_file.filename
            uploaded_file.save(name)
            with open(name, "r") as read_content:
                print("FILE CONTENT")
                print(json.load(read_content))

            validation_result = sensor_type_validator.sensor_type_validator(
                name)
            if(validation_result):
                # I can have a message here too
                return render_template('sensor_type_upload.html', message=("Validation successful"))
            else:
                return render_template('sensor_type_upload.html', error=("Validation Failed"))

        else:
            return render_template('sensor_type_upload.html', error="No file choosen")

    return render_template('sensor_type_upload.html')


@app.route("/sensor_instance_upload", methods=["GET", "POST"])
@login_required
def sensor_instance_upload():
    if request.method == "POST":
        print("IN SENSOR INSTANCE UPLOAD REQUEST")
        uploaded_file = request.files['customFile']
        # uploaded_file = request.form.get('customFile')

        try:
            shutil.rmtree("temp/")
        except Exception:
            pass

        os.mkdir("temp")

        if uploaded_file.filename != '':

            name = "temp/" + uploaded_file.filename
            uploaded_file.save(name)
            with open(name, "r") as read_content:
                print("FILE CONTENT")
                print(json.load(read_content))

            validation_result = sensor_instance_validator.sensor_instance_validator(
                name)
            if(validation_result):
                # I can have a message here too
                return render_template('sensor_instance_upload.html', message=("Validation successful"))
            else:
                return render_template('sensor_instance_upload.html', error=("Validation Failed"))

        else:
            return render_template('sensor_type_upload.html', error="No file choosen")

    return render_template('sensor_instance_upload.html')


# controller_type_upload
@app.route("/controller_type_upload", methods=["GET", "POST"])
@login_required
def controller_type_upload():
    return render_template('controller_type_upload.html')


# controller_instance_upload
@app.route("/controller_instance_upload", methods=["GET", "POST"])
@login_required
def controller_instance_upload():
    return render_template('controller_instance_upload.html')


# model_upload
@app.route("/model_upload", methods=["GET", "POST"])
@login_required
def model_upload():
    return render_template('model_upload.html')


# app_upload
@app.route("/app_upload", methods=["GET", "POST"])
@login_required
def app_upload():
    return render_template('app_upload.html')


# configuration_upload
@app.route("/configuration_upload", methods=["GET", "POST"])
@login_required
def configuration_upload():
    return render_template('configuration_upload.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
