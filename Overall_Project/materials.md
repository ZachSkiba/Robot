## 🟢 Phase 0 — Materials Checklist (Simulation & Planning Only)

### Hardware
- [ ] Laptop / desktop computer  
- [ ] Notebook + pen (for sketches & derivations)  

### Software
- [ ] Python (3.10+)  
- [ ] NumPy  
- [ ] Matplotlib  
- [ ] SciPy (for numerical IK)  
- [ ] Jupyter Notebook or VS Code  
- [ ] Git  
- [ ] GitHub repository  

### Optional / Nice to Have
- [ ] MATLAB + Simulink (for cross-checking kinematics)  
- [ ] LaTeX / Markdown editor (for documentation)  

# Robotic Arm Project – Phase-by-Phase Materials List

This document lists all materials, components, and tools required for the robotic arm project. Organized by project phase, including mini-projects and preparatory work.

---

## Phase 0: Planning & Prototyping Mini-Projects

| Item | Quantity | Notes |
|------|---------|------|
| Project notebook / digital documentation | 1 | For design sketches, calculations, and testing logs |
| CAD software (Fusion 360 / SolidWorks / FreeCAD) | 1 | For link, joint, and gripper design |
| Arduino Mega / ESP32 | 1 | Initial testing microcontroller |
| Breadboard | 1 | Rapid prototyping for circuits |
| Jumper wires | 20–30 | For temporary connections |
| Test servos (SG90 or similar) | 2–3 | For proof-of-concept testing |
| Sensors (rotary encoder, IMU) | 1–2 | To test motion feedback |
| 3D printer / filament | 0.5–1 spool | For early mechanical prototypes |
| Multimeter | 1 | Voltage, current, and continuity tests |
| Basic hand tools | 1 set | Screwdrivers, pliers, hex keys |

**Mini-projects in Phase 0:**  
- Test servo motor control via Arduino/ESP32.  
- Prototype a single-joint linkage using 3D printed parts.  
- Test basic sensor feedback (rotation/angle).  

---

## Phase 1: Mechanical Structure

| Item | Quantity | Notes |
|------|---------|------|
| Aluminum/PLA/ABS sheets or rods | As required | Arm links, base, brackets |
| Screws, nuts, washers (M3, M4) | 50+ | For joints and mounts |
| Bearings (ball or sleeve) | 4–12 | Joint smooth motion |
| Shaft collars | 4–6 | Motor to joint connection |
| Base plate (metal or wood) | 1 | Stable foundation |
| End-effector mounting plate | 1 | For gripper or tool |
| 3D printer filament | 1–2 spools | PLA or ABS for link prototypes |

**Mini-projects in Phase 1:**  
- Build and test single-link joint assemblies.  
- Verify link strength and fit tolerances.  
- Test base stability with partial assembly.  

---

## Phase 2: Actuators & Motion Control

| Item | Quantity | Notes |
|------|---------|------|
| High-torque servo motors (MG996R or better) | 4–6 | Joints, torque ≥ required load |
| Stepper motors (optional) | 1–2 | Base rotation / high-precision joints |
| Motor brackets | 4–6 | Secure mounting |
| Gears, pulleys, belts (optional) | As needed | For torque transmission |
| Couplers | 2–4 | Motor shaft to joint interface |

**Mini-projects in Phase 2:**  
- Control single motor through Arduino/ESP32 with PWM.  
- Test torque and rotation range for each motor.  
- Calibrate speed and position response.  

---

## Phase 3: Electronics & Control Systems

| Item | Quantity | Notes |
|------|---------|------|
| Arduino Mega or ESP32 | 1 | Main microcontroller |
| Motor driver shields (L298N, TB6600, or similar) | 2–4 | Match motor type |
| Power supply 12V 5A+ | 1 | Stable motor and electronics power |
| Breadboard / PCB | 1–2 | Circuit prototyping |
| Jumper wires | 50+ | Signal connections |
| Capacitors, resistors, diodes | As required | Noise suppression, protection |
| Limit switches | 4–6 | Homing and safety |
| Sensors | 1–4 | Encoders, IMU, force sensors |

**Mini-projects in Phase 3:**  
- Wire one joint with motor driver and sensor.  
- Program PID control for joint.  
- Test safety stops and feedback loops.  

---

## Phase 4: Wiring & Connectivity

| Item | Quantity | Notes |
|------|---------|------|
| 22–26 AWG wires | As needed | Signal connections |
| 14–18 AWG wires | As needed | Motor power lines |
| Heat shrink tubing | 20–30 | Insulate connections |
| Terminal blocks / connectors | As needed | Secure wiring |
| USB cables | 1–2 | Programming boards |
| Ferrules / crimp terminals | As needed | Reliable connections |

**Mini-projects in Phase 4:**  
- Wire and test a single joint from motor to microcontroller.  
- Implement cable routing on partially assembled arm.  

---

## Phase 5: Tools & Assembly

| Item | Quantity | Notes |
|------|---------|------|
| Screwdrivers / hex keys | 1 set each | Mechanical assembly |
| Pliers / wire cutters / strippers | 1 each | Wiring and assembly |
| Soldering iron + solder | 1 | Permanent connections |
| Calipers / ruler | 1 | Accurate measurements |
| Drill + bits | 1 | Mounting holes |
| Thread locker | 1 small bottle | Prevent loosening screws |
| Safety gear | As required | Gloves, goggles |

**Mini-projects in Phase 5:**  
- Assemble full mechanical arm without electronics.  
- Verify range of motion and link clearances.  

---

## Phase 6: Software Development & Integration

| Item | Notes |
|------|------|
| VS Code | IDE with PlatformIO for Arduino/ESP32 |
| Arduino IDE | Optional, for firmware testing |
| PlatformIO extension | For project management & libraries |
| Python | For simulations and higher-level control |
| MATLAB / Simulink | Optional for kinematics/control simulation |
| Libraries | Servo, I2C, SPI, sensor-specific |

**Mini-projects in Phase 6:**  
- Develop individual joint control scripts.  
- Integrate multiple joints for coordinated motion.  
- Test kinematics calculations and feedback control.  

---

**Notes:**  
- Phase 0 ensures early testing reduces failures in later phases.  
- Each phase’s mini-projects act as validation steps before full assembly.  
- Quantities are approximate; adjust per number of joints, sensors, and prototypes.  
