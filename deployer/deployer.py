import requests
from flask import Flask, jsonify, request
import subprocess
from time import sleep
app = Flask(__name__)


@app.route('/run', methods=["POST", "GET"])
def runImg():
    print("img being Deployed....")
    print(request)
    req = request.json
   #  img_file = req.get('img_file_path')
    img_name = req.get('image')
   #  tm = str(int(time.time()))
   #  container_name = img_name+"_"+tm
   #  complete = "docker run -d --name "+container_name+" "+img_name

    complete = "sudo docker run --rm -it --network=host "+img_name

   #  change this command to run docker image...

    subprocess.Popen(complete, shell=True)
    print("container runninig")
   #  paras = {"container_name":container_name}
   #  response = requests.post(url="http://0.0.0.0:5002/recv_req",json=paras)
   #  print(response)
    return 'deployed'


@app.route('/kill', methods=["POST", "GET"])
def killImg():
    print("img being killed....")
    print(request)
    req = request.json
   #  img_file = req.get('img_file_path')
    img_name = req.get('image')
    command = "sudo docker ps | grep '"+img_name+"' | awk '{ print $1 }'"
    out = subprocess.check_output(command, shell=True)
    out = out.decode('utf-8')
    out = out.strip()
    complete = "docker kill "+out
    subprocess.Popen(complete, shell=True)

   #  subprocess.Popen(complete,shell=True)

   #  change this command to run docker image...
    complete = "sudo docker rm "+out
    print('killed.... removing')
    sleep(2)

    subprocess.Popen(complete, shell=True)
    print("container killed and removed..")

    return 'deployed'


# @app.route('/send_req', methods=['POST','GET'])
# def send_req():
#     #  a = request.json.get("a")
#     #  b = request.json.get("b")
#     paras = {"img_file_path":"./android/docker/img"}
#     print("called")
#     response = requests.post(url="http://0.0.0.0:5003/nodeman",json=paras)

#     req = response.content.decode("utf-8")
#     filepath = req["file_path"]

#     return 'deployed'

if __name__ == '__main__':
    app.run(port=9000, debug=True)
