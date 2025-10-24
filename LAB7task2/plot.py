import serial
import matplotlib.pyplot as plt
from drawnow import drawnow

ser = serial.Serial('/dev/ttyACM0', 115200)

raw_data = []
filtered_data = []

plt.ion()  # interactive mode

def make_plot():
    plt.clf()
    plt.plot(raw_data, label='Raw')
    plt.plot(filtered_data, label='Filtered')
    plt.legend()
    plt.xlabel('Sample')
    plt.ylabel('Voltage (V)')
    plt.title('STM32 ADC Moving Average Filter')

while True:
    line = ser.readline().decode('utf-8').strip()
    try:
        parts = line.split(',')
        if len(parts) == 2:
            raw = float(parts[0])
            filtered = float(parts[1])
            raw_data.append(raw)
            filtered_data.append(filtered)
            drawnow(make_plot)
    except:
        pass


