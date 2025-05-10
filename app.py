from flask import Flask, render_template
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
    print(f'arduino try:{arduino}')
    time.sleep(2)
except Exception as e:
    print('except')
    arduino = None
    print(f"Error connecting to serial port: {e}")

@app.route('/')
def index():
    global last_distance, last_occupied

    if arduino:
        try:
            arduino.reset_input_buffer()
            time.sleep(0.2)
            line = arduino.readline().decode().strip()
            print(f"Serial Line: {line}")

            if line.startswith("Distance:"):
                value = line.split(":")[1].strip().replace("cm", "").strip()
                if value.isdigit():
                    distance = f"{value} cm"
                    is_occupied = int(value) > 0

                    # Update only if changed
                    if distance != last_distance:
                        last_distance = distance
                        last_occupied = is_occupied
        except Exception as e:
            print(f"Error reading serial: {e}")

    return render_template("index.html", distance=last_distance, is_occupied=last_occupied)



# 🟡 Add this to start the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
