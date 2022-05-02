from flask import Flask, render_template
import threading
import api
from time import sleep

app = Flask()

def fire_detection():
    sensor_data = api.getSensorData("fire_control_system")
    prediction = api.predict("fire_control_system", sensor_data)
    
    pass

def peripheral_control_system():
    while(1):
        # sensor_name = "Camera_sensor"
        sensor_data = api.get_sensor_data("peripheral_control_system")

        # model_name = "StudentMD_model"
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

def attendance_system():
        
    # sensor_name = "Camera"
    # model_name = "model1"
    predictions = []
    sensor_data = api.get_sensor_data("attendance_system")
    for img in sensor_data:
        predictions.append(api.predict("attendance_system",img))

    # Send notification


    # model_name2 = "model2"

    # get_attentiveness = api.predict(model_name2,sensor_data)

    # api.controllerAction(get_attentiveness,"Light_controller")
            


def attention_system():
    while(1):
        
        # sensor_name = "Camera"
        # model_name = "model1"
        predictions = []
        sensor_data = api.get_sensor_data("attention_system")
        for img in sensor_data:
            predictions.append(api.predict("attention_system",img))
        # model_name2 = "model2"

        # get_attentiveness = api.predict(model_name2,sensor_data)

        # api.controllerAction(get_attentiveness,"Light_controller")
                
        sleep(60)

def peripheral_control_system():
    while(1):
        
        # sensor_name = "Camera"
        # model_name = "model1"
        predictions = []
        sensor_data = api.get_sensor_data("peripheral_control_system")
        for img in sensor_data:
            predictions.append(api.predict("peripheral_control_system",img))
        # model_name2 = "model2"

        # get_attentiveness = api.predict(model_name2,sensor_data)

        # api.controllerAction(get_attentiveness,"Light_controller")
                
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