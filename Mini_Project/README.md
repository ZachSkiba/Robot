# Robotic Arm Project – Mini-Projects Phase 0

## Overview
Phase 0 consists of **mini-projects** designed to unlock core skills and build confidence before building the full robotic arm. These are **training wheels**, not resume projects. The goal is to answer the question:

> “Can we do this without panic?”

Mini-projects are short, focused, and **stop immediately once objectives are met**.

---

## Mini-Projects

### **Mini-Project A (Mandatory) – Single-Axis Smart Joint**
- **Objective:** Command a single joint reliably, log data, and visualize performance.
- **Components:** 1 motor, 1 microcontroller (Arduino/ESP32), 1 sensor (encoder/step count), Python script.
- **Learning Outcomes:** Motor behavior, PID tuning, sensor noise handling, calm hardware debugging.
- **Stop Condition:** Motor reaches commanded positions, error plotted vs time.
- **Timeframe:** 5–7 days

### **Mini-Project B (Strongly Recommended) – Controller → Motor**
- **Objective:** Human-in-the-loop control and trajectory logging.
- **Components:** PS5 controller, motor + driver, logging system.
- **Learning Outcomes:** Smooth motion, motor limits, trajectory replay, saturation effects.
- **Stop Condition:** Smooth joystick-controlled motion; recorded trajectory can be replayed.
- **Timeframe:** 3–4 days

### **Mini-Project C (Optional) – 2-Link Arm in Python**
- **Objective:** Build kinematic intuition without hardware.
- **Components:** Python-only simulation, 2 joints, FK + IK, visualization.
- **Learning Outcomes:** Forward/inverse kinematics, plotting.
- **Stop Condition:** FK and IK work, reachable points correctly plotted.
- **Timeframe:** 2–3 days

---

## Goals
- Unlock critical skills for full arm development.
- Verify hardware and software systems function as expected.
- Build confidence in wiring, motor control, PID tuning, and plotting.
- Limit scope strictly to mini-project objectives.
- Stop immediately once objectives are achieved.

---

## Assumptions
- Microcontroller and Python environment are set up and functional.
- Motor and sensor behave predictably for single-joint tests.
- PID control is sufficient for single-joint stabilization.
- Mini-projects are completed within 1–2 weeks.
- Data logging and plotting are feasible in real-time or post-processing.
- Mini-projects are skill unlocks, not optimized or production-ready systems.

---

## Constraints
- Stop mini-projects **once learning objectives are met**.
- Use **only one joint** for Mini-Project A; simulate **2 joints** for Mini-Project C.
- Avoid over-optimization, ML, full-arm builds, or complex simulations.
- Motor current and sensor signals must remain within datasheet limits.
- Hardware and software must be safe to handle.
- Mini-projects should not exceed 1–2 weeks total.

---

## Materials

### General
- Arduino Mega or ESP32 (1)  
- USB cable (1)  
- Breadboard (1)  
- Jumper wires (20–30)  
- Computer with Python and libraries: `matplotlib`, `numpy`, `pyserial`  
- Power supply (5–12V, 2–5A)  
- Basic tools: screwdriver, pliers, wire strippers  
- Multimeter (1)

### Mini-Project A
- Servo or stepper motor (1)  
- Motor driver (if stepper) (1)  
- Encoder or step-count sensor (1)  
- Screws, nuts, washers (few)  
- Small platform or bracket (1)  
- Heat shrink tubing / insulation  
- Optional 3D-printed mount

### Mini-Project B
- PS5 controller (1)  
- USB dongle / Bluetooth adapter (1)  
- Reuse motor & driver from Mini-Project A  
- Wires/connectors as needed  

### Mini-Project C (Optional)
- Python simulation only  
- Libraries: `matplotlib`, `numpy`  
- Optional: Jupyter Notebook for interactive plotting  

---

## Recommended Workflow
**Week 1:** Mini-Project A  
- Split roles: one on hardware, one on plotting/tuning  
- End goal: can command and control a single joint

**Week 2:** Mini-Project B **or** start Phase 1 (mechanical + electronics)  
- After this, you are officially “doing robotics”

**Notes:**  
- Mini-projects are **not optional for skill development**; skip only if you already mastered core skills.  
- The biggest failure mode is skipping the warm-up; second biggest is never stopping.  
- Stop immediately once objectives are achieved — do **not** optimize endlessly.  
