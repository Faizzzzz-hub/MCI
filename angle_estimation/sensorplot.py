import serial
import matplotlib.pyplot as plt
from drawnow import *

# === Setup Serial ===
ser = serial.Serial('/dev/ttyACM0', 115200)   # Change PORT if needed
plt.ion()

acc_vals = []
gyro_vals = []
angle_vals = []
err_vals = []
time_vals = []

count = 0

# === Plot Function ===
def makeFig():
    plt.clf()
    plt.title("Live Accel, Gyro, Filtered Angle")
    plt.grid(True)
    plt.xlabel("Sample Number")
    plt.ylabel("Degrees")

    plt.plot(time_vals, acc_vals, 'r.-', label='acc angle')
    plt.plot(time_vals, gyro_vals, 'g.-', label='gyro rate')
    plt.plot(time_vals, angle_vals, 'b.-', label='filtered angle')
    plt.plot(time_vals, err_vals, 'k.-', label='error')

    plt.legend(loc='upper left')

# === Main Loop ===
while True:
    while ser.in_waiting == 0:
        pass

    try:
        line = ser.readline().decode().strip()

        # Example line:
        # angF=2.35  acc=1.22  gyro=0.50  err=3.10
        parts = line.replace("=", " ").split()

        # parts becomes:
        # ['angF', '2.35', 'acc', '1.22', 'gyro', '0.50', 'err', '3.10']

        # Extract numbers by index
        angle = float(parts[1])
        acc = float(parts[3])
        gyro = float(parts[5])
        err = float(parts[7])

        # Store data
        angle_vals.append(angle)
        acc_vals.append(acc)
        gyro_vals.append(gyro)
        err_vals.append(err)

        time_vals.append(count)
        count += 10  # because STM32 prints every 10 ms

        drawnow(makeFig)
        plt.pause(0.0001)

        # Limit buffer size
        if len(angle_vals) > 500:
            angle_vals.pop(0)
            acc_vals.pop(0)
            gyro_vals.pop(0)
            err_vals.pop(0)
            time_vals.pop(0)

    except Exception as e:
        print("Error:", e)

