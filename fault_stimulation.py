import time
import random
import joblib
from pathlib import Path

# Load AI model
BASE_DIR = Path(__file__).resolve().parent
MODEL_FILE = BASE_DIR / "digital_twin_model.pkl"

model = joblib.load(MODEL_FILE)

print("============================================================")
print("        AI EMBEDDED DIGITAL TWIN")
print("        FAULT DETECTION + AUTO RECOVERY")
print("============================================================")

print("\nChoose fault:")
print("1. CPU OVERLOAD")
print("2. MEMORY OVERLOAD")
print("3. OVERHEATING")
print("4. NETWORK FAILURE")
print("5. BATTERY FAILURE")

choice = input("\nEnter fault number (1-5): ")

# Normal values
cpu = 35.0
memory = 40.0
temperature = 40.0
battery = 100.0
network_latency = 20.0


def ai_check():
    features = [[
        cpu,
        memory,
        temperature,
        battery,
        network_latency
    ]]

    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0]

    if 1 in model.classes_:
        index = list(model.classes_).index(1)
        fault_probability = probability[index] * 100
    else:
        fault_probability = 0

    return prediction, fault_probability


# ---------------------------------------------------------
# NORMAL OPERATION
# ---------------------------------------------------------

print("\n========== NORMAL OPERATION ==========")

for i in range(5):

    cpu += random.uniform(-2, 2)
    memory += random.uniform(-1, 1)
    temperature += random.uniform(-0.5, 0.5)
    battery -= random.uniform(0.01, 0.05)
    network_latency += random.uniform(-2, 2)

    prediction, probability = ai_check()

    print(
        f"CPU: {cpu:.1f}% | "
        f"Memory: {memory:.1f}% | "
        f"Temp: {temperature:.1f}°C | "
        f"Battery: {battery:.1f}% | "
        f"Network: {network_latency:.1f} ms | "
        f"AI: {probability:.1f}%"
    )

    time.sleep(0.5)


# ---------------------------------------------------------
# FAULT
# ---------------------------------------------------------

print("\n============================================================")
print("                 ⚠ FAULT INJECTED")
print("============================================================")

for i in range(5):

    if choice == "1":
        cpu = random.uniform(85, 100)
        temperature += random.uniform(1, 3)

    elif choice == "2":
        memory = random.uniform(85, 100)
        temperature += random.uniform(1, 2)

    elif choice == "3":
        temperature = random.uniform(80, 100)
        cpu += random.uniform(0, 3)

    elif choice == "4":
        network_latency = random.uniform(150, 500)

    elif choice == "5":
        battery = random.uniform(1, 15)

    else:
        print("Invalid choice.")
        exit()

    prediction, probability = ai_check()

    print(
        f"\nFAULT | CPU: {cpu:.1f}% | "
        f"Memory: {memory:.1f}% | "
        f"Temp: {temperature:.1f}°C | "
        f"Battery: {battery:.1f}% | "
        f"Network: {network_latency:.1f} ms"
    )

    print(f"AI FAULT PROBABILITY: {probability:.1f}%")

    time.sleep(0.5)


# ---------------------------------------------------------
# AUTOMATIC RECOVERY
# ---------------------------------------------------------

print("\n============================================================")
print("             🛠 AUTOMATIC RECOVERY")
print("============================================================")

print("AI detected abnormal system behaviour.")
print("Recovery mechanism activated...\n")

for i in range(10):

    # Gradually return every parameter toward normal

    cpu += (35 - cpu) * 0.25
    memory += (40 - memory) * 0.25
    temperature += (40 - temperature) * 0.25
    battery += (100 - battery) * 0.10
    network_latency += (20 - network_latency) * 0.25

    prediction, probability = ai_check()

    print(
        f"Recovery {i+1:02d} | "
        f"CPU: {cpu:.1f}% | "
        f"Memory: {memory:.1f}% | "
        f"Temp: {temperature:.1f}°C | "
        f"Battery: {battery:.1f}% | "
        f"Network: {network_latency:.1f} ms | "
        f"Fault: {probability:.1f}%"
    )

    time.sleep(0.5)


print("\n============================================================")
print("             ✅ SYSTEM RECOVERED")
print("============================================================")

print(
    f"Final State → "
    f"CPU: {cpu:.1f}% | "
    f"Memory: {memory:.1f}% | "
    f"Temperature: {temperature:.1f}°C | "
    f"Battery: {battery:.1f}% | "
    f"Network: {network_latency:.1f} ms"
)

print("\nDigital Twin simulation completed successfully.")