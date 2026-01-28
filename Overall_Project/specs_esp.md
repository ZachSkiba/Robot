# 🤖 6-DOF Robotic Arm — Final Integrated Design Blueprint (Rev 4.7)

**The "Research" Edition: Data Science Ready, Python-Controlled, High Telemetry**

---

## 1️⃣ Robot Specifications

| Parameter | Value / Design |
|-----------|----------------|
| **Hardware** | FluidNC 6-Pack Controller (ESP32-Based) |
| **Firmware** | Custom "Telemetry" Sketch (C++/Arduino) — Replaces FluidNC Brain |
| **Brain (Logic)** | Python (PC/Laptop) running Kinematics & Trajectory Planning |
| **Degrees of Freedom** | 6 (Base, Shoulder, Elbow, Wrist P, Wrist R, Gripper) |
| **Data Rate** | 100Hz - 500Hz Real-time Position, Error, & Current streaming |
| **Control Loop** | Hardware-in-the-Loop (HIL) |
| **Sensors** | Absolute Magnetic Encoders (AS5600) + Motor Current Sensing |
| **Connectivity** | USB Serial (Low Latency) or Wi-Fi UDP (High Bandwidth) |

---

## 2️⃣ Mechanical Layout (The "Unbreakable" Stack)

**Core Strategy:** Identical to Rev 4.6. Mechanical stack is verified and robust.  

| Joint | Motor | Transmission | Placement | Notes |
|-------|-------|-------------|----------|-------|
| Base | NEMA 23 (3.0 Nm) | 10:1 Planetary | Base Plate | Module 1.5 gears. |
| Shoulder | NEMA 23 (3.0 Nm) | 20:1 Compound Spur | Base Plate | Metal Hub Mandatory. |
| Elbow | NEMA 17 (59 Ncm) | 20:1 Compound Spur | Upper Arm | Open Air Design. |
| Wrist P | NEMA 17 (59 Ncm) | 15:1 Planetary + Spur | Forearm | Metal 5:1 Planetary on motor. |
| Wrist R | NEMA 11 (8 Ncm) | 5:1 Spur | Wrist Plate | Standardized small motor. |
| Gripper | NEMA 11 (8 Ncm) | Worm Gear | End Effector | Self-Locking. |

---

## 3️⃣ Electronics & Control (The "6-Pack" Hardware)

**Core Strategy:** Stick with the 6-Pack board as a "Smart Interface" for Python.  

| Component | Product / Details | Integration Strategy |
|-----------|-----------------|-------------------|
| Motherboard | FluidNC 6x Controller | Acts as the I/O Interface |
| Logic Voltage | 5V / 3.3V (Auto) | No Level Shifters needed |
| Base Drivers | 2 × DM556 (External) | Wire to board's screw terminals |
| Arm Drivers | 4 × TMC2209 | Plug into slots 1–4 |
| Sensors | 2 × AS5600 (I2C) | Plug into board's I2C header |
| Power | 24V 15A PSU | Powers board directly |

---

## 4️⃣ The "Data Science" Pipeline (NEW SECTION)

**Replaces standard FluidNC configuration. This is where research happens.**

**Concept: Hardware-in-the-Loop (HIL)**  
- Python performs decision-making instead of ESP32.  

**Python Script (Mastermind)**  
- Calculates Inverse Kinematics (Angles → Steps)  
- Generates Trajectory (S-Curve / Trapezoidal)  
- Sends command: `M1:100, M2:200...`  

**ESP32 (Nervous System)**  
- Executes steps immediately  
- Reads Encoders & Motor Current  
- Streams data back to Python  

**Analysis (Pandas/Matplotlib)**  
- **Backlash Analysis:** Compare Commanded_Pos vs Encoder_Actual_Pos  
- **PID Tuning:** Optimize gains based on real-world error  
- **Vibration Analysis:** Detect oscillation using encoders  

---

## 5️⃣ Wiring Guide (Standardized)

**Thanks to the 6-Pack board, wiring is simplified:**  
- **Main Power:** 24V PSU → Green Power Terminal on 6-Pack board  
- **Small Motors:** Plug TMC2209 Drivers into Slots 1–4  
- **Big Motors:** Wire DM556s to "External Driver" terminals on Slots 5 & 6  
- **Sensors:** Wire AS5600s to I2C Header (SDA/SCL)  

---

## 6️⃣ Build Phases (Rev 4.7)

1. **Phase 1: The Firmware Swap**  
   - Do NOT use FluidNC  
   - Flash Custom Telemetry Sketch (Arduino C++) to ESP32  
   - Goal: Verify board responds to serial commands (e.g., `M1 100`) and prints sensor data  

2. **Phase 2: The Foundation**  
   - Assemble Base & Shoulder  
   - Wire DM556s  
   - Test: Use Python script to jog base 10°  

3. **Phase 3: The Arm & Sensors**  
   - Assemble Elbow + Wrist  
   - Connect AS5600 Encoders  
   - Calibration: Map raw encoder values at 0° and 90° using Python  

4. **Phase 4: The Data Loop**  
   - Run full Python Control Script  
   - Perform "Sweep Test" (move arm min → max)  
   - Save data to `.csv` and plot error curves  

---

## 💡 Final Verdict

**Rev 4.7 — "Scientist's Robot"**  

- **Mechanicals:** Robust "Tractor" design  
- **Electronics:** Clean "6-Pack" board, solves wiring issues  
- **Brain:** Python via custom telemetry firmware  
- **Telemetry:** High data rate, hardware-in-the-loop, full real-time control
