# Phase 0 — README

## Overview

Phase 0 focuses on **Architecture, Math, Simulation, and Minimal Hardware Reference** for a 3-DOF robotic arm.

**Duration:** ~2 weeks  
**Goal:** Simulate a robotic arm that can move to targets, generate plots/metrics, and document design decisions.  
**Scope:** Software-first, with optional reference hardware for verification. This phase lays a solid foundation for all subsequent work.

---

## Key Outcomes

At the end of Phase 0, you should have:

* Defined the robotic arm: 3 DOF, joint types, link lengths, joint limits
* Implemented **forward kinematics (FK)** in code
* Built a simulation that:
  * Computes joint angles for a target
  * Visualizes motion in 2D or 3D
* Optional: Small reference hardware test (single motor, driver, encoder) to validate concepts
* Defined a **data schema** for telemetry, logging, and potential ML applications
* Added plots and metrics to verify correctness and physical realism

> ✅ This is **resume-worthy** and ensures Phase 1 proceeds smoothly.

---

## Step-by-Step Plan & Roles

### Step 0.1 — Define the Arm (Day 1–2)
**Together:** DOF layout, joint types, link lengths, joint limits  
**Zach (DS):** Coordinate frames, variable names, assumptions document  
**Nicholas (MechE):** Sketches, feasibility, torque directions, motor placement  

### Step 0.2 — Coordinate Frames & Math (Day 3–4)
**Together:** Agree on base frame, axes, and rotation conventions  
**Zach:** Implement FK in Python  
**Nicholas:** Derive FK on paper and check rotations  

### Step 0.3 — First Simulation (Day 5–6)
**Zach:** 2D/3D visualization, animate motion  
**Nicholas:** Verify physical realism, suggest adjustments to link lengths  

### Step 0.4 — Define Data Schema (Day 7)
**Together:** Decide on fields for telemetry and logging  
**Zach:** Consider ML, plotting, and analysis needs  
**Nicholas:** Ensure physical measurability and sanity checks  

### Step 0.5 — Inverse Kinematics (Intro Only) (Day 8–10)
**Together:** Analytical vs numerical IK discussion  
**Zach:** Implement numerical IK  
**Nicholas:** Check joint limits, singularities, feasibility  

### Step 0.6 — Metrics & Plots (Day 11–12)
**Zach:** Generate plots and save results  
**Nicholas:** Interpret motion realism, oscillations, and anomalies  

### Step 0.7 — Phase 0 Deliverables (Day 13–14)
**Together:** Prepare README, documented design, and demo scripts  
**Deliverables:**  
* Documented arm design  
* FK/IK simulation scripts  
* Plots and metrics showing kinematics and motion  

---

## Collaboration Matrix

| Area        | Zach (DS)    | Nicholas (MechE)     |
| ----------- | ------------ | -------------------- |
| FK / IK     | Implement    | Validate physics     |
| Simulation  | Code & plot  | Sanity-check realism |
| Data schema | Design       | Ensure measurability |
| Metrics     | Analyze      | Interpret physically |
| Decisions   | Quantitative | Mechanical intuition |

---

## Reference Hardware (Optional)

Phase 0 does not require full motors or mechanical assembly. Optional hardware can help validate concepts:

| Component | Purpose | Notes |
|-----------|---------|-------|
| Single stepper + driver | Test motion, step response | NEMA 17 + TMC2209 recommended |
| Microcontroller (Teensy / Arduino) | Pulse generation, encoder reading | Optional for verification |
| Encoder (AS5600) | Absolute angle feedback | Optional, I²C interface |
| USB / Power | Connect MCU and motor driver | Optional for reference tests |
| Breadboard / Resistors / Capacitors / Ferrite beads | Noise suppression & testing | Optional, ensures driver stability |

> Focus is **software simulation**, not full mechanical build.

---

## After Phase 0

* CAD design, sensors, and logging in Phase 1 will follow validated simulation and schema  
* Optional reference hardware tests reduce risk for Phase 1 assembly  
* Provides **well-documented baseline** for Phase 1: mechanical, electrical, and control systems

---