from flask import Flask, jsonify
from flask_cors import CORS
from serial_reader import get_sensor_data

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

@app.route('/api/sensors')
def sensors():
    return jsonify(get_sensor_data())

if __name__ == '__main__':
    app.run(port=5000, debug=True)
