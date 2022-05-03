from concurrent.futures import thread
from curses import meta
from flask import Flask, render_template
import threading
import api
from time import sleep
from datetime import date, datetime
now = datetime.now()

app = Flask(__name__)

present_list = set(["asdas","asdasd","asd"])
class_attention = ""
students_dict = {0 : 'Adriana Lima',1 : 'Alex Lawther',2: 'Alexandra Daddario',
3 : 'Alvaro Morte',4 : 'Amanda Crew',5 : 'Andy Samberg',
6 : 'Anne Hathaway',7 : 'Anthony Mackie',8: 'alycia dabnem carey',
9 : 'amber heard'}

average_attentiveness = 0
attentive_time = 0
fan_action = ""
temp = ""
p_action = ""

def fan_control_system():
    while(1):
        sensor_data = api.get_sensor_data("fan_control_system")
        temp = sensor_data
        prediction = api.predict("fan_control_system", sensor_data)
        response = api.controller_action("fan_control_system", prediction)
        fan_action = response
        sleep(60)

    
def peripheral_control_system():
    while(1):
        # sensor_name = "Camera_sensor"
        sensor_data = api.get_sensor_data("peripheral_control_system")

        # model_name = "StudentMD_model"
        p_action = api.predict("peripheral_control_system",sensor_data)

        result = api.controllerAction("peripheral_controller_system",p_action)
        print(result)
        # api.controllerAction(AC_action,"AC_controller")
        # api.controllerAction(Fan_action,"Fan_controller")
        # api.controllerAction(Light_action,"Light_controller")

        sleep(60)

def attendance_system():
    global average_attentiveness
    global attentive_time
    while(1):
        # sensor_name = "Camera"
        # model_name = "model1"
        predictions = []
        sensor_data = api.get_sensor_data("attendance_system")
        predictions = api.predict("attendance_system",sensor_data)
        for i in predictions:
            present_list.add(students_dict[i])

        class_attention = attention_system()
        attentive_time = now.strftime("%H:%M:%S")

        # Send notification

        sleep(60)



def attention_system():
    
    # sensor_name = "Camera"
    # model_name = "model1"
    predictions = []
    sensor_data = api.get_sensor_data("attention_system")
    for img in sensor_data:
        predictions.append(api.predict("attention_system",img))
    count_0=0
    count_1=0
    for attentive_student in predictions:
        if(attentive_student==0):
            count_0+=1
        else:
            count_1+=1
    
    average_attentiveness = count_1/(count_0+count_1)
    #send notification
    print(average_attentiveness)
    return average_attentiveness


def change_value():

    global attentive_time
    global average_attentiveness

    while(1):
        attentive_time+=1
        average_attentiveness+=1
        sleep(2)
    

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/startClass', methods = ["GET"])
def startClass():
    global attentive_time
    global average_attentiveness
    return render_template("start_class.html", attentive_time=datetime.now(), average_attentiveness=average_attentiveness)


@app.route('/endClass', methods = ["GET"])
def endclass():
    return render_template("end_class.html", present_list=present_list)


@app.route('/monitorPeripheral')
def monitorPeripheral():
    global attentive_time
    global average_attentiveness
    return render_template("monitor_peripheral.html", time_stamp=datetime.now(), action=p_action)


@app.route('/monitorFan')
def monitorFan():
    return render_template("monitor_fans.html", time_stamp=datetime.now(), temp=temp, action=fan_action)


if __name__ == "__main__":
    t1 = threading.Thread(target = fan_control_system)
    t2 = threading.Thread(target = peripheral_control_system)
    t3 = threading.Thread(target = attendance_system)
    t4 = threading.Thread(target = change_value)
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    app.run(debug=True, host="0.0.0.0", use_reloader=False,port= 5000)