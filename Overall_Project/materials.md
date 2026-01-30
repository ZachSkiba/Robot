# 🟢 Phase 0 — Materials Checklist (Simulation & Planning Only)

## Hardware
- Laptop / desktop computer  
- Notebook + pen (for sketches & derivations)  

✅ No physical hardware added — this is correct and intentional.

## Software
- Python (3.10+)  
- NumPy  
- Matplotlib  
- SciPy (for numerical IK / optimization)  
- Jupyter Notebook or VS Code  
- Git  
- GitHub repository  

➕ Added (required by architecture):  
- PySerial (MCU protocol simulation)  
- Gamepad / HID Python library (PS5 input simulation)  

## Optional / Nice to Have
- MATLAB + Simulink (for cross-checking kinematics)  
- LaTeX / Markdown editor (for documentation)  

---

# Robotic Arm Project – Phase-by-Phase Materials List

This document lists all materials, components, and tools required for the robotic arm project. Organized by project phase, including mini-projects and preparatory work.

---

## Phase 0: Planning & Prototyping Mini-Projects

| Item | Quantity | Notes |
|------|---------|------|
| Project notebook / digital documentation | 1 | For design sketches, calculations, and testing logs |
| CAD software (Fusion 360 / SolidWorks / FreeCAD) | 1 | For link, joint, and gripper design |
| ❌ Arduino Mega / ESP32 | — | Removed — Phase 0 is virtual-only |
| ❌ Breadboard | — | Removed — no hardware prototyping in Phase 0 |
| ❌ Jumper wires | — | Removed — hardware-gated |
| ❌ Test servos (SG90 or similar) | — | Removed — architecture uses steppers only |
| ❌ Sensors (rotary encoder, IMU) | — | Removed — simulated sensors only |
| ❌ 3D printer / filament | — | Removed — no physical builds in Phase 0 |
| Multimeter | 1 | Optional verification tool only |
| Basic hand tools | 1 set | Optional, not required |

**Mini-projects in Phase 0:**  
- Virtual single-joint dynamics simulation (stepper model).  
- Virtual sensor feedback and logging validation.  
- FK / IK validation in simulation.  

---

## Phase 1: Mechanical Structure

| Item | Quantity | Notes |
|------|---------|------|
| Aluminum / steel structural members | As required | Final arm links and brackets |
| Screws, nuts, washers (M3, M4) | 50+ | For joints and mounts |
| Bearings (ball or crossed roller) | 4–12 | Joint smooth motion |
| Shaft collars | 4–6 | Motor to joint connection |
| Base plate (metal) | 1 | Rigid, grounded |
| End-effector mounting plate | 1 | Tool interface |
| 3D printer filament | 1–2 spools | Optional — non-load-bearing parts only |

**Mini-projects in Phase 1:**  
- Dry-fit mechanical joints (no power).  
- Verify link alignment and tolerances.  

---

## Phase 2: Actuators & Motion Control

| Item | Quantity | Notes |
|------|---------|------|
| ❌ High-torque servos | — | Removed — not used anywhere in Rev 5.2 |
| NEMA 23 stepper motors | 2 | J1, J2 |
| NEMA 17 stepper motors | 2 | J3, J4 |
| NEMA 11 stepper motors | 2 | J5, J6 |
| Gearboxes (planetary / worm) | 6 | Per joint spec |
| Gravity assist spring | 1 | Mandatory for J3 |
| Shaft couplers | 6 | Motor-to-gearbox |

**Mini-projects in Phase 2:**  
- Single-joint motion under load.  
- Thermal and current envelope validation.  

---

## Phase 3: Electronics & Control Systems

| Item | Quantity | Notes |
|------|---------|------|
| Teensy 4.1 | 1 | Motion core |
| ESP32-C3 | 1 | Wi-Fi telemetry |
| DM556T drivers | 2 | J1, J2 |
| TMC2209 drivers | 4 | J3–J6 |
| 24 V power supply (15 A) | 1 | Headroom required |
| Physical E-stop (NC) | 1 | Logic-independent |
| Safety relay | 1 | Cuts EN or 24 V |
| Encoders (AS5600 / AS5048A) | 1–6 | Phase dependent |

**Mini-projects in Phase 3:**  
- Watchdog + heartbeat validation.  
- E-stop dominance testing.  

---

## Phase 4: Wiring & Connectivity

| Item | Quantity | Notes |
|------|---------|------|
| Shielded motor cables | As needed | Especially J1/J2 |
| Shielded twisted-pair encoder cables | As needed | Mandatory |
| Differential I²C converters | 2–3 | PCA9615 / LTC4311 |
| Ferrite beads | 6–10 | EMI suppression |
| Drag chains | 1–2 | Moving cables |
| Heat shrink tubing | 20–30 | Insulation |

**Mini-projects in Phase 4:**  
- EMI robustness testing.  
- Encoder reliability verification.  

---

## Phase 5: Tools & Assembly

| Item | Quantity | Notes |
|------|---------|------|
| Screwdrivers / hex keys | 1 set | Mechanical assembly |
| Wire strippers / cutters | 1 each | Wiring |
| Soldering iron + solder | 1 | Permanent joints |
| Calipers | 1 | Precision measurement |
| Oscilloscope (≥50 MHz) | 1 | Step timing validation |
| Bench power supply | 1 | Current-limited |
| Safety gear | As required | Mandatory |

---

## Phase 6: Software Development & Integration

| Item | Notes |
|------|------|
| VS Code + PlatformIO | Firmware |
| Python | Planning, logging, judgment |
| HID / Gamepad libraries | PS5 controller |
| NumPy / SciPy / Pandas | Metrics |
| Matplotlib / Plotly | Visualization |

**Mini-projects in Phase 6:**  
- Trajectory validation and replay.  
- Health verdict system implementation.