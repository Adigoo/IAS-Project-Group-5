import sys
from flask import Flask, request

app = Flask(__name__)

@app.route("/performAction", methods=["POST", "GET"])
def performAction():
    data = request.json
    if data['data'] == 0:
        return "Turn Off light"
    else:
        return "Turn On light"

if __name__ == "__main__":
    port = sys.argv[1]
    app.run(port=port, host="0.0.0.0", debug=True)