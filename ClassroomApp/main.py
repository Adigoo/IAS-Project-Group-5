from flask import Flask, render_template
import threading
import api
from time import sleep
from datetime import datetime
now = datetime.now()
import json
app = Flask(__name__)

def fire_detection():
    pass

def student_motion_detect():
    while(1):
        sensor_name = "Camera_sensor"
        sensor_data = api.get_sensor_data(sensor_name)

        model_name = "StudentMD_model"
        StudentMD_pred_data = api.predict(sensor_data,model_name)

        PC_action = StudentMD_pred_data['pc']
        AC_action = StudentMD_pred_data['ac']
        Fan_action = StudentMD_pred_data['fan']
        Light_action = StudentMD_pred_data['light']

        api.controllerAction(PC_action,"PC_controller")
        api.controllerAction(AC_action,"AC_controller")
        api.controllerAction(Fan_action,"Fan_controller")
        api.controllerAction(Light_action,"Light_controller")

        sleep(60)

attentive_time=0
average_attentiveness = 0

def change_value():

    global attentive_time
    global average_attentiveness

    for i in range(0,5):
        attentive_time+=1
        average_attentiveness+=1
        sleep(2)
    

def attention_detection():
    global average_attentiveness
    global attentive_time

    while(1):
        sensor_name = "Camera"
        model_name = "model1"
        sensor_data = api.get_sensor_data(sensor_name)
        
        image_name_list = api.predict(model_name,sensor_data)
        model_name2 = "model2"

        get_attentiveness = api.predict(model_name2,sensor_data)
        
        api.controllerAction(get_attentiveness,"Light_controller")

        count_0=0
        count_1=0
        for attentive_student in get_attentiveness:
            if(attentive_student==0):
                count_0+=1
            else:
                count_1+=1
        
        average_attentiveness = count_1/(count_0+count_1)
        attentive_time = now.strftime("%H:%M:%S")

        sleep(60)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/attendance')
def attendance():    
    pass

@app.route('/get_attentive')
def get_attentive():
    data={'attentive':attentive_time, 'average_attentiveness':average_attentiveness}
    jsonstring = json.dump(data)
    return jsonstring


    
@app.route('/attention')
def attention():
    global attentive_time
    global average_attentiveness
    return render_template("attention.html", attentive_time=attentive_time, average_attentiveness=average_attentiveness)

@app.route('/peripherals')
def peripherals():
    pass


if __name__ == "__main__":
    # t1 = threading.Thread(target = fire_detection)
    # t2 = threading.Thread(target = student_motion_detect)
    # t3 = threading.Thread(target = attention_detection)
    
    app.run(port = 5050)
    t4 = threading.Thread(target = change_value())
    
    