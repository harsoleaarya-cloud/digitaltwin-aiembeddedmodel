import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = BASE_DIR / "device_data_ai.csv"

TOTAL_ROWS = 5000
FAULT_PROBABILITY = 0.30      # share of rows that end up faulty
MIN_FAULT_LENGTH = 5          # faults last a burst of cycles, like real ones
MAX_FAULT_LENGTH = 20

FAULT_TYPES = [
    "HIGH_CPU",
    "HIGH_MEMORY",
    "HIGH_TEMPERATURE",
    "HIGH_NETWORK_LATENCY",
    "LOW_BATTERY",
]


class VirtualDevice:
    """Same device model as device.py, with an explicit fault mode."""

    def __init__(self):
        self.cpu_load = 30.0
        self.memory_usage = 40.0
        self.temperature = 40.0
        self.battery = 100.0
        self.network_latency = 20.0

    def step_normal(self):
        """One cycle of healthy operation: small drift around nominal values."""
        self.cpu_load += random.uniform(-3, 3)
        self.memory_usage += random.uniform(-2, 2)
        self.temperature += random.uniform(-0.8, 0.8)
        self.battery -= random.uniform(0.0, 0.01)
        self.network_latency += random.uniform(-3, 3)

        # A healthy device gets recharged before it runs flat, so "low battery"
        # stays a genuinely abnormal condition rather than the normal end state.
        if self.battery < 60:
            self.battery = 100.0

        # Healthy devices are pulled back toward their nominal operating point
        self.cpu_load += (30 - self.cpu_load) * 0.10
        self.memory_usage += (40 - self.memory_usage) * 0.10
        self.temperature += (40 - self.temperature) * 0.10
        self.network_latency += (20 - self.network_latency) * 0.10

        self._clamp()

    def step_fault(self, fault_type):
        """One cycle while a fault is active. Only the affected parameters move."""
        self.step_normal()

        if fault_type == "HIGH_CPU":
            self.cpu_load = random.uniform(85, 100)
            self.temperature += random.uniform(1, 3)

        elif fault_type == "HIGH_MEMORY":
            self.memory_usage = random.uniform(85, 100)
            self.temperature += random.uniform(0.5, 2)

        elif fault_type == "HIGH_TEMPERATURE":
            self.temperature = random.uniform(78, 100)
            self.cpu_load += random.uniform(0, 5)

        elif fault_type == "HIGH_NETWORK_LATENCY":
            self.network_latency = random.uniform(120, 500)

        elif fault_type == "LOW_BATTERY":
            self.battery = random.uniform(1, 18)

        self._clamp()

    def _clamp(self):
        self.cpu_load = max(5, min(self.cpu_load, 100))
        self.memory_usage = max(10, min(self.memory_usage, 100))
        self.temperature = max(25, min(self.temperature, 100))
        self.battery = max(0, min(self.battery, 100))
        self.network_latency = max(5, min(self.network_latency, 500))

    def row(self):
        return [
            round(self.cpu_load, 2),
            round(self.memory_usage, 2),
            round(self.temperature, 2),
            round(self.battery, 2),
            round(self.network_latency, 2),
        ]


def main():
    random.seed(42)  # reproducible dataset

    device = VirtualDevice()
    timestamp = datetime.now()

    rows = []
    fault_remaining = 0
    active_fault = None

    while len(rows) < TOTAL_ROWS:

        # Decide whether to start a new fault burst
        if fault_remaining == 0 and random.random() < FAULT_PROBABILITY / 10:
            active_fault = random.choice(FAULT_TYPES)
            fault_remaining = random.randint(MIN_FAULT_LENGTH, MAX_FAULT_LENGTH)

        if fault_remaining > 0:
            device.step_fault(active_fault)
            state, fault_type, anomaly = "FAULT", active_fault, 1
            fault_remaining -= 1
            if fault_remaining == 0:
                active_fault = None
        else:
            device.step_normal()
            state, fault_type, anomaly = "NORMAL", "NORMAL", 0

        rows.append(
            [timestamp.strftime("%Y-%m-%d %H:%M:%S"), "DT-001", state]
            + device.row()
            + [fault_type, anomaly]
        )

        timestamp += timedelta(seconds=1)

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp", "device_id", "state",
            "cpu_load", "memory_usage", "temperature",
            "battery", "network_latency",
            "fault_type", "anomaly",
        ])
        writer.writerows(rows)

    faults = sum(r[-1] for r in rows)
    print(f"Wrote {len(rows)} rows to {OUTPUT_FILE}")
    print(f"  normal : {len(rows) - faults}")
    print(f"  fault  : {faults} ({faults / len(rows):.1%})")


if __name__ == "__main__":
    main()