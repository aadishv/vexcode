import logging

from flask import Flask, jsonify, request
from flask_cors import CORS  # To handle CORS issues

# Disable the Werkzeug logger (the one that shows the requests)
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)  # Only show errors,

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

n = 0


@app.route("/update", methods=["POST"])
def receive_data():
    global n
    n += 1
    # Get the JSON data from the request
    data = request.get_json()
    if len(data) > 0:
        print("Received data:", data)
    # Return a success response
    return jsonify({"message": "Data received successfully", "data": data}), 200


def start_app():
    app.run(host="127.0.0.1", port=3000, use_reloader=False)


if __name__ == "__main__":
    start_app()
