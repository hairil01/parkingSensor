import serial
import time

SERIAL_PORT = 'COM4'  # Change this based on your OS and port
BAUD_RATE = 9600

# Keep track of last sensor data
last_data = {
    "sensor1": {"distance": "No Data", "occupied": False},
    "sensor2": {"distance": "No Data", "occupied": False}
}

def get_sensor_data():
    global last_data  # access the previous data

    new_data = {
        "sensor1": {"distance": "No Data", "occupied": False},
        "sensor2": {"distance": "No Data", "occupied": False}
    }

    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as arduino:
            time.sleep(1)
            for _ in range(4):
                line = arduino.readline().decode().strip()
                if "Sensor 1 Distance" in line:
                    value = int(line.split(":")[1].replace("cm", "").strip())
                    new_data["sensor1"] = {"distance": f"{value} cm", "occupied": value > 0}
                elif "Sensor 2 Distance" in line:
                    value = int(line.split(":")[1].replace("cm", "").strip())
                    new_data["sensor2"] = {"distance": f"{value} cm", "occupied": value > 0}
    except Exception as e:
        print(f"Serial read error: {e}")
        return last_data  # fallback to previous data on error

    # Check if new data is different
    if new_data != last_data:
        last_data = new_data  # update stored data
        print("Sensor data updated.")
    else:
        print("No changes in sensor data.")

    return last_data

