from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Store the latest sensor data
last_data = {
    "sensor1": {"distance": "No Data", "occupied": False},
    "sensor2": {"distance": "No Data", "occupied": False}
}

@app.route('/api/sensors', methods=['GET'])
def get_sensor_data():
    return jsonify(last_data)

@app.route('/api/sensors', methods=['POST'])
def update_sensor_data():
    global last_data
    if request.is_json:
        data = request.get_json()
        last_data = data
        return jsonify({"status": "success"}), 200
    return jsonify({"error": "Invalid JSON"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, ssl_context=(
        '/etc/letsencrypt/live/parkingsensor.duckdns.org/fullchain.pem',
        '/etc/letsencrypt/live/parkingsensor.duckdns.org/privkey.pem'
    ))
