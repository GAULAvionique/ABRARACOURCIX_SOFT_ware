import serial
import time
import random

COM_PORT = "COM5"
BAUDRATE = 115200

try:
    ser = serial.Serial(COM_PORT, BAUDRATE, timeout=1)
    print(f"Opened {COM_PORT} for test data...")
except Exception as e:
    print(f"Error opening {COM_PORT}: {e}")
    exit(1)

timestamp = 0

try:
    while True:
        timestamp += 100

        gyro_val = random.uniform(-180.0, 180.0)

        line = f"T_{timestamp};G_{gyro_val:.4f}\n"

        ser.write(line.encode())

        print(f"Sent: {line.strip()}")

        time.sleep(0.1)
except KeyboardInterrupt:
    print("Stopping test sender...")
finally:
    ser.close()
