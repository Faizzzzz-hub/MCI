import serial
import matplotlib.pyplot as plt
from drawnow import *

# === Setup Serial ===
sinWaveData = serial.Serial('/dev/ttyACM0', 115200)
plt.ion()

# === Plot Styles to Rotate Through ===
plot_styles = ['r.-', 'b.-', 'g.-', 'm.-', 'c.-', 'y.-', 'k.-']

# === Data Storage ===
NUM_SAMPLES = 100
time_ms = []
cnt = 0
all_signals = []  # List of lists. all_signals[0] = Temperature, all_signals[1] = X, etc.
signals = ["Temperature", "X", "Y", "Z"]

# === Plotting Function ===
def makeFig(title, xLabel, yLabel, yLimit, *args):
    plt.clf()
    plt.title(title)
    plt.grid(True)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.ylim(yLimit[0], yLimit[1])

    for arg in args:
        plt.plot(time_ms, arg[0], arg[1], label=arg[2])

    plt.legend(loc='upper left')

# === Main Loop ===
while True:
    while sinWaveData.inWaiting() == 0:
        pass  # Wait for data

    try:
        line = sinWaveData.readline().decode().strip()
        values = line.split(',')

        # Check if we received exactly 4 values
        if len(values) != 4:
            print("Invalid data:", values)
            continue

        # First time: initialize sublists
        if len(all_signals) != len(values):
            all_signals = [[] for _ in range(len(values))]

        # Append each value to its corresponding signal list
        try:
            all_signals[0].append(int(values[0]))      # Temperature as int
            all_signals[1].append(float(values[1]))    # X as float
            all_signals[2].append(float(values[2]))    # Y as float
            all_signals[3].append(float(values[3]))    # Z as float
        except ValueError:
            print("Conversion error:", values)
            continue

        # Update time
        time_ms.append(cnt)
        cnt += 1

        # Build args for plotting
        args = []
        for i, signal in enumerate(all_signals):
            style = plot_styles[i % len(plot_styles)]
            label = signals[i]
            args.append((signal, style, label))

        # Draw plot
        title = "Gyroscope Plot"
        drawnow(lambda: makeFig(title, "Time (ms)", "Value", [-255, 255], *args))
        plt.pause(0.0001)

        # Keep only last NUM_SAMPLES samples
        if len(time_ms) > NUM_SAMPLES:
            time_ms.pop(0)
            for signal in all_signals:
                signal.pop(0)

    except Exception as e:
        print("Error:", e)

