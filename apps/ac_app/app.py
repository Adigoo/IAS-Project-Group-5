from crypt import methods
import api
import numpy as np
from time import sleep
import logging
from flask import Flask
# data_file = open('application.json')
# data = json.load(data_file)
# sd = data['sensor']
app = Flask(__name__)

# while(1):
    # 1
@app.route("/make_app_prediction", methods=["GET"])
def make_app_prediction():
    data = api.getSensorData()
    temperature = data
    data = np.reshape(np.array(data), (-1, 1))

        
        #2
    prediction = api.predict(data)

        #3
    output = api.controllerAction(prediction[0])
    logging.warning("Temperature is:", temperature, "and action taken:", output)
    #sleep(60)

if __name__ == '__main__':
    
    app.run(debug=True, host='0.0.0.0', port=5000)
