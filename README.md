🧠 NEUROAID – EOG-Based Assistive Communication System

NEUROAID is a hybrid hardware–software assistive system that uses Electrooculography (EOG) signals to enable communication and control for motor-impaired users through eye blinks.

The project focuses on low-cost, non-invasive healthcare technology, inspired by Brain–Computer Interface (BCI) concepts but designed for real-world usability and affordability.

📌 Project Overview

Conventional assistive communication systems either rely on physical switches or expensive EEG-based interfaces.
NEUROAID addresses this gap by using vertical eye movement (EOG) as a single biosignal input to control a row-column scanning interface, enabling full alphanumeric communication using only eye blinks.

The system is designed to work reliably in non-clinical, noisy environments such as homes or rehabilitation centers.

🔧 Hardware Components

Arduino Uno / Nano

EOG signal acquisition circuit

AD620 instrumentation amplifier

LM358 operational amplifier (filtering & gain)

Disposable Ag/AgCl electrodes (3-electrode configuration)

USB power supply

Circuit details are provided in circuit_diagram.png.

🧠 Software Components
Firmware (Arduino – C++)

Real-time ADC sampling

Adaptive baseline tracking for blink detection

Noise-robust signal thresholding

Serial data transmission to host system

Application Layer (Python)

EOG signal visualization

Blink event detection

Row-column scanning interface for text entry

🏗️ System Architecture
Eye Movement
   ↓
EOG Analog Front-End (AD620 + LM358)
   ↓
Arduino (Adaptive Blink Detection)
   ↓
Python Interface (Scanning & Control)

✨ Key Innovations

Adaptive baseline tracking to handle signal drift and noise

Single-channel EOG control for full keyboard navigation

Low-cost hardware design using generic analog components

Non-invasive and portable, suitable for assistive healthcare use

🚀 How to Use

Upload eog_circuit.ino to the Arduino

Connect electrodes as per circuit diagram

Run the Python interface:

python bci_scanner.py


Use eye blinks to navigate the scanning interface

🎯 Applications

Assistive communication for motor-impaired users

Rehabilitation and accessibility systems

Human–Computer Interaction (HCI) research

Low-cost healthcare technology

📄 Documentation

SYCSA_16_PATENT.docx – Patent and technical documentation

circuit_diagram.png – Hardware schematic

👤 Authors

Ananya Choudhari
Arya Bharat Patil
Aryan Bhat
Ankush Kumar

Department of Computer Engineering
Vishwakarma Institute of Technology, Pune
