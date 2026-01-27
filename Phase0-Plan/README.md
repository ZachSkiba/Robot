# Phase 0 — README

## Overview

Phase 0 focuses on **Architecture, Math, and Simulation** for a 3-DOF robotic arm.

**Duration:** ~2 weeks
**Goal:** Simulate a robotic arm that can move to targets with plots, metrics, and documented design decisions.

This phase sets a solid foundation for all subsequent work.

---

## Key Outcomes

At the end of Phase 0, you should have:

* Defined the robotic arm (3 DOF, joint types, link lengths, joint limits)
* Implemented forward kinematics in code
* Built a simulation that:

  * Computes joint angles for a target
  * Visualizes motion in 2D or 3D
* Defined a **data schema** for later phases
* Added plots and metrics to verify correctness and realism

This is **resume-worthy** and ensures Phase 1 proceeds smoothly.

---

## Step-by-Step Plan & Roles

### Step 0.1 — Define the Arm (Day 1–2)

**Together:** DOF layout, joint types, link lengths, joint limits
**Zach (DS):** Coordinate frames, variable names, assumptions doc
**Nicholas (MechE):** Sketches, feasibility, torque directions, motor placement

### Step 0.2 — Coordinate Frames & Math (Day 3–4)

**Together:** Agree on base frame, axes, signs
**Zach:** FK implementation in Python
**Nicholas:** FK derivation on paper, check rotations

### Step 0.3 — First Simulation (Day 5–6)

**Zach:** 2D/3D visualization, animate motion
**Nicholas:** Verify physical realism, suggest link adjustments

### Step 0.4 — Define Data Schema (Day 7)

**Together:** Decide on fields for telemetry and logging
**Zach:** Consider ML and plotting needs
**Nicholas:** Ensure measurability, ground truth vs estimates

### Step 0.5 — Inverse Kinematics (Intro Only) (Day 8–10)

**Together:** Analytical vs numerical IK
**Zach:** Implement numerical IK
**Nicholas:** Check joint limits, singularities, feasibility

### Step 0.6 — Metrics & Plots (Day 11–12)

**Zach:** Generate plots, save results
**Nicholas:** Interpret motion realism, oscillations

### Step 0.7 — Phase 0 Deliverables (Day 13–14)

**Together:** Prepare short README and demo script
**Deliverables:** Documented arm design, plots, demo script showing simulation and kinematics

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

## After Phase 0

* CAD, sensors, and logging in Phase 1 follow validated simulation and schema
* Phase 0 ensures execution is clear and risk is minimized
