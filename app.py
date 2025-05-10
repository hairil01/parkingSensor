from flask import Flask, render_template
import serial
import time

app = Flask(__name__)

SERIAL_PORT = 'COM4'
BAUD_RATE = 9600

last_data = {
    "sensor1": {"distance": "No Data", "occupied": False},
    "sensor2": {"distance": "No Data", "occupied": False}
}

try:
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Allow time for Arduino to reset
except Exception as e:
    arduino = None
    print(f"Error connecting to serial port: {e}")

@app.route('/')
def index():
    global last_data

    if arduino:
        try:
            for _ in range(4):  # Read a few lines to catch both sensors
                line = arduino.readline().decode().strip()
                print(f"Serial Line: {line}")

                if "Sensor 1 Distance" in line:
                    value = line.split(":")[1].replace("cm", "").strip()
                    if value.isdigit():
                        distance = f"{value} cm"
                        occupied = int(value) >0   # Occupied if object ≤ 5 cm
                        last_data["sensor1"] = {"distance": distance, "occupied": occupied}

                elif "Sensor 2 Distance" in line:
                    value = line.split(":")[1].replace("cm", "").strip()
                    if value.isdigit():
                        distance = f"{value} cm"
                        occupied = int(value) >0
                        last_data["sensor2"] = {"distance": distance, "occupied": occupied}

        except Exception as e:
            print(f"Error reading serial: {e}")

    return render_template("index.html", data=last_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
