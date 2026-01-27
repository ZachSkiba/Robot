# Phase 0 — System Overview

## Purpose

This document provides a **system-level view of Phase 0**, focusing on architecture, math, and simulation for the 3-DOF robotic arm.

Phase 0 is entirely **virtual**; no hardware is used. The goal is to validate design decisions, coordinate frames, and control algorithms in simulation, and prepare a foundation for data-driven experimentation.

---

## System Layers in Phase 0

1. **Virtual Physical Layer**

   * Represents links and joints in simulation
   * Includes approximate joint limits and link lengths
   * No real actuators yet

2. **Mathematical Layer**

   * Forward kinematics (FK) implementation in Python
   * Optional DH parameters or homogeneous transforms
   * Preliminary inverse kinematics (numerical) for motion planning

3. **Simulation Layer**

   * 2D/3D visualization of the robotic arm
   * Animate motion between target poses
   * Track joint positions and end-effector trajectories

4. **Data & Metrics Layer**

   * Define schema for logging joint commands, states, and end-effector pose
   * Generate plots of joint angles, errors, and trajectory performance
   * All outputs saved for future reference

---

## Workflow

```
Target Pose --> IK Solver --> Joint Angles --> FK Verification --> Visualization
                         |                           |
                     Error Metrics               Plot & Save
```

* IK solver computes joint angles for given target
* FK verifies correctness of computed angles
* Visualization layer animates motion
* Data & metrics layer logs and plots results

---

## Phase 0 Responsibilities

| Layer            | Zach (DS)                                              | Nicholas (MechE)                                  |
| ---------------- | ------------------------------------------------------ | ------------------------------------------------- |
| Virtual Physical | Define link lengths & joint limits (check feasibility) | Sketch and verify physical plausibility           |
| Math (FK / IK)   | Implement FK, numerical IK, compute errors             | Validate calculations, check signs, singularities |
| Simulation       | Build visualization, animate motion, save outputs      | Validate realism of motion, suggest adjustments   |
| Data & Metrics   | Define data schema, generate plots                     | Interpret plots, verify realism                   |

---

## Success Criteria

* Arm simulation matches agreed-upon 3-DOF design
* FK implementation verified against paper derivation
* Visualization shows smooth, physically plausible motion
* Data schema defined for all future phases
* Plots and metrics provide confidence in arm behavior

---

## Guiding Principle

> **Phase 0 proves the concept virtually. All hardware decisions and data collection strategies follow from this validated simulation.**
