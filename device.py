import random
import time
import csv
from pathlib import Path
from datetime import datetime, timedelta

import joblib
import pandas as pd


# ============================================================
# AI EMBEDDED DIGITAL TWIN
# ============================================================

print("============================================================")
print("        AI EMBEDDED DIGITAL TWIN")
print("============================================================")


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

MODEL_FILE = BASE_DIR / "digital_twin_model.pkl"
CSV_FILE = BASE_DIR / "ai_live_data.csv"


# ============================================================
# LOAD AI MODEL
# ============================================================

try:
    model = joblib.load(MODEL_FILE)
    print("✓ AI model loaded successfully")
except FileNotFoundError:
    print("✗ AI model not found!")
    print(f"Expected location: {MODEL_FILE}")
    print("Make sure digital_twin_model.pkl is in the main project folder.")
    exit()


# ============================================================
# DIGITAL TWIN DEVICE
# ============================================================

class VirtualEmbeddedDevice:

    def __init__(self):

        self.device_id = "DT-001"

        self.state = "NORMAL"

        # Initial device parameters
        self.cpu_load = 30.0
        self.memory_usage = 40.0
        self.temperature = 40.0
        self.battery = 100.0
        self.network_latency = 20.0

        self.fault_injected = False

    # --------------------------------------------------------
    # UPDATE DEVICE
    # --------------------------------------------------------

    def update(self):

        # Normal variation
        self.cpu_load += random.uniform(-3, 3)
        self.memory_usage += random.uniform(-2, 2)
        self.temperature += random.uniform(-0.8, 0.8)
        self.battery -= random.uniform(0, 0.05)
        self.network_latency += random.uniform(-3, 3)

        # Keep values within realistic limits
        self.cpu_load = max(5, min(self.cpu_load, 95))
        self.memory_usage = max(10, min(self.memory_usage, 95))
        self.temperature = max(25, min(self.temperature, 90))
        self.battery = max(0, min(self.battery, 100))
        self.network_latency = max(5, min(self.network_latency, 100))

    # --------------------------------------------------------
    # SENSOR TASK
    # --------------------------------------------------------

    def sensor_task(self):

        self.temperature += random.uniform(-0.5, 0.5)

        self.temperature = max(25, min(self.temperature, 90))

    # --------------------------------------------------------
    # CONTROL TASK
    # --------------------------------------------------------

    def control_task(self):

        # Simulated embedded control task
        if self.cpu_load > 85:
            self.state = "HIGH LOAD"

    # --------------------------------------------------------
    # COMMUNICATION TASK
    # --------------------------------------------------------

    def communication_task(self):

        self.network_latency += random.uniform(-1, 1)

        self.network_latency = max(5, min(self.network_latency, 100))

    # --------------------------------------------------------
    # AI FAULT PREDICTION
    # --------------------------------------------------------

    def ai_prediction(self):

        data = pd.DataFrame([{
            "cpu_load": self.cpu_load,
            "memory_usage": self.memory_usage,
            "temperature": self.temperature,
            "battery": self.battery,
            "network_latency": self.network_latency
        }])

        prediction = model.predict(data)[0]

        probability = model.predict_proba(data)[0]

        normal_probability = probability[0] * 100
        fault_probability = probability[1] * 100

        if prediction == 1:
            self.state = "FAULT DETECTED"
        else:
            self.state = "NORMAL"

        return normal_probability, fault_probability

    # --------------------------------------------------------
    # DIAGNOSTIC TASK
    # --------------------------------------------------------

    def diagnostic_task(self):

        if self.state == "FAULT DETECTED":

            print("⚠ AI WARNING: Potential device fault detected!")

        else:

            print("✓ Diagnostic: Device operating normally")


# ============================================================
# CSV FILE
# ============================================================

if not CSV_FILE.exists():

    with open(CSV_FILE, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "timestamp",
            "device_id",
            "state",
            "cpu_load",
            "memory_usage",
            "temperature",
            "battery",
            "network_latency",
            "normal_probability",
            "fault_probability"
        ])


# ============================================================
# CREATE DEVICE
# ============================================================

device = VirtualEmbeddedDevice()

print()
print("Device ID:", device.device_id)
print("✓ Digital Twin initialized")
print("✓ AI fault detection enabled")
print()
print("Starting live simulation...")
print("Press CTRL+C to stop.")
print()
print("============================================================")


# ============================================================
# SIMULATION
# ============================================================

current_time = datetime.now()

for cycle in range(30):

    # --------------------------------------------------------
    # Update virtual device
    # --------------------------------------------------------

    device.update()

    device.sensor_task()

    device.control_task()

    device.communication_task()

    # --------------------------------------------------------
    # AI prediction
    # --------------------------------------------------------

    normal_probability, fault_probability = device.ai_prediction()

    # --------------------------------------------------------
    # Diagnostics
    # --------------------------------------------------------

    device.diagnostic_task()

    # --------------------------------------------------------
    # Display
    # --------------------------------------------------------

    print(
        f"Time: {current_time.strftime('%H:%M:%S')} | "
        f"Device: {device.device_id} | "
        f"State: {device.state} | "
        f"CPU: {device.cpu_load:.2f}% | "
        f"Memory: {device.memory_usage:.2f}% | "
        f"Temperature: {device.temperature:.2f}°C | "
        f"Battery: {device.battery:.2f}% | "
        f"Network: {device.network_latency:.2f} ms | "
        f"AI Fault: {fault_probability:.1f}%"
    )

    # --------------------------------------------------------
    # Save data
    # --------------------------------------------------------

    with open(CSV_FILE, "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            current_time.strftime("%Y-%m-%d %H:%M:%S"),
            device.device_id,
            device.state,
            round(device.cpu_load, 2),
            round(device.memory_usage, 2),
            round(device.temperature, 2),
            round(device.battery, 2),
            round(device.network_latency, 2),
            round(normal_probability, 2),
            round(fault_probability, 2)
        ])

    current_time += timedelta(seconds=1)

    time.sleep(1)


# ============================================================
# END
# ============================================================

print()
print("============================================================")
print("AI DIGITAL TWIN SIMULATION COMPLETED")
print("============================================================")
print(f"Live dataset saved to: {CSV_FILE}")
print("AI predictions were recorded.")
print("============================================================")