from flask import Flask, render_template
import threading
import api
from time import sleep

app = Flask()

def fire_detection():
    while( True ):
        model_name = "Temp_detect_model"

        sensor_name = "temp_detect"
        temp_sensor_data = api.get_sensor_data( sensor_name )
        
        data = {
            "data" : {
                "temp" : temp_sensor_data['data']
            }
        }
        pred_data = api.predict( data, model_name )
        
        controller_name = "fire_alarm_controller"
        api.controller_action( pred_data, controller_name )
        sleep( 60 )


def student_motion_detect():
    
    pass

def attention_detection():
    pass

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