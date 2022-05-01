from flask import Flask, render_template
import threading
import api
from time import sleep

app = Flask()

def fire_detection():
    pass

def student_motion_detect():
    
    pass

def attention_detection():
    while(1):
        sensor_name = "Camera"
        model_name = "model1"
        sensor_data = api.get_sensor_data(sensor_name)
        image_name_list = api.predict(model_name,sensor_data)
        model_name2 = "model2"
        get_attentiveness = api.predict(model_name2,sensor_data)        
        sleep(60)
    

app.route('/')
def home():
    return render_template("index.html")

app.route('/attendance')
def attendance():
    pass

app.route('/attention')
def attention():
    pass

app.route('/peripherals')
def peripherals():
    pass


if __name__ == "__main__":
    t1 = threading.Thread(target = fire_detection)
    t2 = threading.Thread(target = student_motion_detect)
    t3 = threading.Thread(target = attention_detection)
    
    app.run(port=5000)