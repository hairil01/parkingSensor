from flask import Flask, jsonify
import serial
import time

#open terminal 
#python app.py


app = Flask(__name__)

SERIAL_PORT = 'COM3'
BAUD_RATE = 9600
last_distance = "No Data"
last_occupied = False


try:
    print('try')
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f'arduino',arduino)
    time.sleep(2)
except Exception as e:
    print('error')
    arduino = None
    print(f"Error connecting to serial port: {e}")

@app.route('/api/data')
def get_sensor_data():
    global last_data

    if arduino:
        try:
            for _ in range(4):
                line = arduino.readline().decode().strip()
                print(f"Serial Line: {line}")

                if "Sensor 1 Distance" in line:
                    value = line.split(":")[1].replace("cm", "").strip()
                    if value.isdigit():
                        distance = f"{value} cm"
                        occupied = int(value) > 0
                        last_data["sensor1"] = {"distance": distance, "occupied": occupied}

                elif "Sensor 2 Distance" in line:
                    value = line.split(":")[1].replace("cm", "").strip()
                    if value.isdigit():
                        distance = f"{value} cm"
                        occupied = int(value) > 0
                        last_data["sensor2"] = {"distance": distance, "occupied": occupied}
        except Exception as e:
            print(f"Error reading serial: {e}")

    return jsonify(last_data)

# 🟡 Add this to start the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
