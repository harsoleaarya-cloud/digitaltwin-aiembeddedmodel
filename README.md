# 🤖 AI Embedded Digital Twin

An AI-powered virtual embedded system that simulates device telemetry, injects hardware-like faults, detects anomalies using Machine Learning, and performs automatic recovery.

---

## 📌 Project Overview

This project implements a software-based **Embedded Digital Twin** of a virtual device.

Instead of requiring physical hardware, the system creates a virtual embedded device on a computer and continuously simulates parameters such as:

- CPU Load
- Memory Usage
- Temperature
- Battery Level
- Network Latency

A Machine Learning model monitors these parameters and detects abnormal operating conditions.

The system can also intentionally inject faults and demonstrate how an embedded system could detect and recover from abnormal behavior.

---

## 🧠 System Architecture

```text
              ┌──────────────────────┐
              │  Virtual Embedded    │
              │      Device          │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ Telemetry Generation │
              │ CPU / RAM / Temp /   │
              │ Battery / Network    │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  Machine Learning    │
              │   Random Forest      │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ Anomaly Detection    │
              └──────────┬───────────┘
                         │
                  Fault Detected
                         │
                         ▼
              ┌──────────────────────┐
              │ Automatic Recovery   │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   Normal Operation   │
              └──────────────────────┘


---

🚀 Key Features

1. Virtual Embedded Device

The project simulates an embedded device without requiring physical hardware.

The virtual device generates changing telemetry values for:

CPU utilization

Memory utilization

Temperature

Battery percentage

Network latency


2. Synthetic Telemetry Dataset

A dataset is generated containing normal and abnormal operating conditions.

Fault classes include:

CPU Overload

Memory Overload

High Temperature

High Network Latency

Low Battery


3. Machine Learning Fault Detection

A Random Forest Classifier is trained using telemetry features:

CPU Load
Memory Usage
Temperature
Battery
Network Latency

The model predicts whether the current device state is:

NORMAL

or

ANOMALY

4. Fault Injection

The system can intentionally introduce abnormal conditions.

Example:

Normal Temperature
       ↓
       ↓
Fault Injection
       ↓
Temperature → 90°C+
       ↓
AI detects abnormal condition

5. Automatic Recovery

After a fault is detected, the simulation activates a recovery mechanism.

The system gradually moves the simulated parameters toward normal operating values.

FAULT
  ↓
AI Detection
  ↓
Recovery Activated
  ↓
Parameters Return Toward Normal
  ↓
SYSTEM RECOVERED

6. Interactive Dashboard

A Streamlit dashboard displays:

CPU usage

Memory usage

Temperature

Battery

Network latency

AI fault probability

Device status

Live telemetry graphs



---

🛠️ Technologies Used

Technology	Purpose

Python	Core development
Scikit-learn	Machine Learning
Random Forest	Anomaly classification
Pandas	Dataset processing
Joblib	Model storage/loading
Streamlit	Interactive dashboard
Git & GitHub	Version control
VS Code	Development environment



---

📂 Project Structure

ai-embedded-digital-twin/
│
├── simulation/
│   ├── device.py
│   ├── generate_dataset.py
│   └── device_data.csv
│
├── ai_predict.py
├── dashboard.py
├── generate_dataset.py
├── train_model.py
├── fault_simulation.py
│
├── device_data.csv
├── device_data_ai.csv
├── ai_live_data.csv
│
├── digital_twin_model.pkl
├── .gitignore
└── README.md


---

⚙️ Installation

Clone the repository:

git clone https://github.com/harsoleaarya-cloud/ai-embedded-digital-twin-model.git

Enter the project directory:

cd ai-embedded-digital-twin-model

Create a virtual environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate

Install the required packages:

pip install pandas numpy scikit-learn joblib streamlit


---

▶️ Running the Project

Run the virtual device

python simulation/device.py

Run AI prediction

python ai_predict.py

Run fault injection + AI detection + recovery

python fault_simulation.py

Choose a fault when prompted.

Example:

3

for overheating.

Run the dashboard

streamlit run dashboard.py

The dashboard will open in your browser.


---

🧪 Example Fault Scenario

Normal State

CPU: ~35%
Memory: ~40%
Temperature: ~40°C
Battery: ~100%
Network: ~20 ms

Fault Injection

For an overheating scenario:

Temperature → 80–100°C

The AI model evaluates the telemetry and detects abnormal behavior.

Recovery

The recovery mechanism gradually brings the virtual device parameters back toward normal operating values.

Temperature: 95°C
       ↓
       ↓ Recovery
       ↓
Temperature: 75°C
       ↓
Temperature: 58°C
       ↓
Temperature: 46°C
       ↓
Temperature: ~40°C


---

📊 Machine Learning Pipeline

Generate Telemetry
       ↓
Create Dataset
       ↓
Label Normal/Fault Conditions
       ↓
Train Random Forest
       ↓
Save Model
       ↓
Load Model
       ↓
Analyze Live Telemetry
       ↓
Predict Anomaly


---

🎯 Why Digital Twin?

Traditional embedded-system testing often requires physical hardware and controlled fault conditions.

A software-based digital twin provides a way to experiment with:

Device behavior

Telemetry

Fault scenarios

AI-based monitoring

Recovery strategies


without requiring physical hardware for the prototype.


---

🔬 Current Limitations

This project is currently a software prototype.

The training dataset is synthetically generated rather than collected from physical embedded hardware. Therefore, the model's performance on real-world hardware telemetry has not been independently validated.

Future versions can connect the digital twin to real sensors and embedded boards to collect real telemetry.


---

🔮 Future Scope

Possible extensions include:

Real sensor integration

ESP32/Arduino integration

Real-time hardware telemetry

More advanced anomaly detection

LSTM-based time-series prediction

Edge AI deployment

Hardware-in-the-loop testing

Predictive maintenance

Cloud-based digital twin

Real-time fault classification

Automated firmware-level recovery



---

👨‍💻 Skills Demonstrated

This project demonstrates practical experience with:

Python

Embedded-system concepts

Digital Twin concepts

Machine Learning

Random Forest

Data generation and preprocessing

Anomaly detection

Fault injection

Automatic recovery

Real-time simulation

Streamlit

Git/GitHub



---

📌 Project Status

Completed Prototype ✅

The current implementation demonstrates:

Virtual Device
      +
Telemetry Simulation
      +
Machine Learning
      +
Fault Injection
      +
Anomaly Detection
      +
Automatic Recovery
      +
Real-Time Dashboard


---

📜 License

This project is intended for educational and portfolio purposes.
