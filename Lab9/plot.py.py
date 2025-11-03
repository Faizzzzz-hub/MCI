import serial
import time
import re

# --- Configuration ---
PORT = "/dev/ttyACM0"  # STM32 UART port on Linux
BAUDRATE = 115200
TIMEOUT = 1            # seconds

# --- Regular expression to parse the line ---
line_pattern = re.compile(r"GyroX=([-\d.]+) dps, AccY=([-\d.]+) g")

def parse_line(line):
    match = line_pattern.search(line)
    if match:
        gx = float(match.group(1))
        ay = float(match.group(2))
        return gx, ay
    return None, None

def main():
    with serial.Serial(PORT, BAUDRATE, timeout=TIMEOUT) as ser:
        time.sleep(2)  # Wait for STM32 to initialize
        print("Connected to STM32. Reading data...\n")
        try:
            while True:
                line = ser.readline().decode("utf-8", errors="ignore").strip()
                if line:
                    gx, ay = parse_line(line)
                    if gx is not None and ay is not None:
                        print(f"Gyro X: {gx:.3f} dps, Acc Y: {ay:.3f} g")
        except KeyboardInterrupt:
            print("\nExiting...")

if __name__ == "__main__":
    main()

