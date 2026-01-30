# 🦾 Robotic Arm Project – Mini-Projects (Phase 0)

## Overview
Phase 0 consists of **mini-projects** designed to unlock core skills, verify hardware/software behavior, and build confidence before assembling the full robotic arm. These are **training wheels**, not portfolio projects. The goal is:

> “Can we handle the hardware and code safely and reliably without panic?”

Mini-projects are **short, focused, and stop immediately once objectives are met**.

---

## Mini-Projects

### **Mini-Project A (Mandatory) – Single-Axis Smart Joint**
- **Objective:** Command a single joint reliably, log data, and visualize performance.
- **Components:** 1 motor, 1 microcontroller (Teensy 4.1 / Arduino / ESP32), 1 sensor (encoder/step count), Python interface.
- **Learning Outcomes:**
  - Motor behavior & PID tuning  
  - Sensor noise handling  
  - Safe hardware debugging  
  - Soft limits, E-stop, and halt condition enforcement
- **Completion Criteria:**  
  - Motor reaches commanded positions reliably  
  - Error vs time plots match expectations  
  - Joint performance report completed
- **Timeframe:** 5–7 days

---

### **Mini-Project B (Strongly Recommended) – Controller → Motor**
- **Objective:** Implement human-in-the-loop control and trajectory logging.
- **Components:** PS5 controller, motor + driver (reuse from Mini-Project A), logging system.
- **Learning Outcomes:**
  - Smooth joystick-controlled motion  
  - Motor saturation and limits  
  - Trajectory replay & logging  
  - Safety overrides validation (E-stop, limits)
- **Completion Criteria:**  
  - Motor moves smoothly with joystick  
  - Recorded trajectories replay accurately  
  - Safety limits are never violated
- **Timeframe:** 3–4 days

---

### **Mini-Project C (Optional) – 2-Link Arm in Python**
- **Objective:** Build kinematic intuition without hardware.
- **Components:** Python-only simulation (2 joints), FK + IK algorithms, visualization.
- **Learning Outcomes:**
  - Forward/inverse kinematics  
  - Trajectory visualization and validation  
  - Data ready for 6-DOF scaling
- **Completion Criteria:**  
  - FK/IK produce correct positions  
  - Motion plots match expected trajectories
- **Timeframe:** 2–3 days

---

## Goals
- Unlock critical skills for full 6-DOF arm development.  
- Verify that **fundamental systems** (motor, sensor, controller) behave predictably.  
- Build confidence in wiring, motor control, PID tuning, and plotting.  
- Produce reusable artifacts (plots, logs, code, reports) for Phase 1.  
- Strictly limit scope: stop immediately once objectives are achieved.  

---

## Assumptions
- Microcontroller and Python environment are functional.  
- Motor and sensor behave predictably for single-joint tests.  
- PID control suffices for single-joint stabilization.  
- Data logging and plotting are feasible in real-time or post-processing.  
- Mini-projects are skill unlocks, not optimized or production-ready systems.  

---

## Constraints
- Stop mini-projects **once learning objectives are met**.  
- Use **only one joint** for Mini-Project A; simulate **2 joints** for Mini-Project C.  
- Avoid over-optimization, ML, full-arm builds, or complex simulations.  
- Motor current and sensor signals must remain within datasheet limits.  
- Hardware and software must be safe to handle.  
- Mini-projects should not exceed 1–2 weeks per project.

---

## Materials

### **General / Shared**
- Teensy 4.1 or Arduino Mega / ESP32 (1)  
- USB cable (Micro-USB / USB-C) (1)  
- Breadboard (1)  
- Jumper wires (20–30)  
- Computer with Python + libraries: `matplotlib`, `numpy`, `pyserial`  
- Power supply (5–24V, 2–5A)  
- Basic tools: screwdriver, pliers, wire strippers  
- Multimeter (1)  

### **Mini-Project A – Single-Axis Smart Joint**
- Stepper motor (NEMA 17 recommended) (1)  
- Motor driver (TMC2209 / L298N / TB6600) (1)  
- Encoder (AS5600 or similar) (1)  
- Screws, nuts, washers (few)  
- Small platform or bracket (1)  
- Heat shrink tubing / insulation as needed  
- Optional: 3D-printed motor mount  

### **Mini-Project B – Controller → Motor**
- PS5 controller (1)  
- USB dongle or Bluetooth adapter (1)  
- Reuse motor + driver from Mini-Project A  
- Wires/connectors as needed  

### **Mini-Project C (Optional / Virtual)**
- Python simulation only  
- Libraries: `matplotlib`, `numpy`  
- Optional: Jupyter Notebook for interactive plotting  

---

## Recommended Workflow
**Week 1 – Mini-Project A:**  
- Split roles: one on hardware, one on plotting/tuning  
- End goal: reliably command and control a single joint  

**Week 2 – Mini-Project B or Mini-Project C:**  
- After completion, you are ready to scale to Phase 1 (multi-joint integration)  

**Notes:**  
- Mini-projects are **skill unlocks, not optional warm-ups**.  
- Biggest failure mode: skipping the warm-up; second: never stopping.  
- Stop immediately once objectives are achieved — **do not optimize endlessly**.  