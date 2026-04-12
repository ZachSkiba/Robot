# Phase 0–5 Scope Definition (Robotic Arm Only)

This document defines **what belongs and does not belong** in Phases 0–5 of the robotic arm project, with a focus on technical depth, realism, and resume value.

---

## ✅ PID Control — YES (Core)

**Phase:** 2–3  
**Status:** Mandatory

### What You Do
- Joint-level PID control for position
- Compare different gain settings
- Measure:
  - Rise time
  - Overshoot
  - Steady-state error

### Why It’s Good
- Demonstrates control fundamentals
- Establishes baseline system performance

**Resume signal:**  
> Designed and tuned closed-loop controllers for a multi-DOF robotic arm

---

## ✅ System Identification — YES (Core)

**Phase:** 4–5  
**Status:** Mandatory, project-defining

### What You Do
Estimate from experimental data:
- Motor constants
- Friction
- Gear ratios
- System delay

Fit simple models and validate against real behavior.

### Why It’s Good
- Bridges hardware, math, and data
- Enables all advanced control and learning later

**Resume signal:**  
> Performed system identification on real robotic hardware using experimental data

---

## ✅ Optimal Control (Lightweight) — YES (Selective)

**Phase:** Late Phase 5  
**Status:** Allowed (keep scope reasonable)

⚠️ Not full LQR yet.

### What You Do
- Optimize simple trajectories:
  - Smooth point-to-point motion
  - Minimize time or energy
- Compare optimized motion vs PID baseline

### Why It’s Good
- Shows optimization skill without overreaching

**Resume signal:**  
> Implemented trajectory optimization under physical constraints

---

## ⚠️ Digital Twin — PARTIAL ONLY

**Phase:** 5 (minimal scope)

You do **not** build a full digital twin yet.

### Allowed
- Simple kinematic simulator
- Parameterized using measured values
- Used for:
  - Visualization
  - Sanity checks

### Not Allowed Yet
- RL training
- Claims of “high-fidelity simulation”

**Resume wording:**  
> Developed a kinematics-based simulator informed by experimental measurements

---

## ❌ Reinforcement Learning — NO (Not Yet)

**Phase:** 8+

### Why Not
- Requires a stable simulator
- Needs large datasets
- Risky without constraints

Allowed mention only:
> Future work includes reinforcement learning

---

## ❌ Predictive Maintenance — NO

**Phase:** 10+

### Why Not
- Requires long-term degradation data
- No meaningful failure signals early on

---

# Phase ≤5 Add-Ons (Strong Alternatives)

These add depth **without** overreaching.

---

## ⭐ Add-On 1: Calibration Pipeline (Highly Underrated)

**Phase:** 3–4

### What You Do
- Automatic homing
- Zero-offset estimation
- Repeatability testing

### Why It’s Strong
- Very realistic robotics work
- Strong industry signal

**Resume:**  
> Designed automated calibration and repeatability testing for a robotic manipulator

---

## ⭐ Add-On 2: Constraint-Aware Motion Planning

**Phase:** 4–5

### What You Do
Enforce:
- Joint limits
- Velocity limits
- Collision-free zones
- Abort unsafe motions

### Why It’s Strong
- Safety-focused
- Shows engineering maturity

---

## ⭐ Add-On 3: Data Infrastructure (Big DS Signal)

**Phase:** 3–5

### What You Do
Automatic logging of:
- Joint states
- Commands
- Errors

Produce:
- Structured datasets
- Clean plots
- Quantitative metrics

**Resume:**  
> Built a data collection and analysis pipeline for robotic experiments

---

## ⭐ Add-On 4: Performance Benchmarking Suite

**Phase:** 5

### What You Do
Define metrics:
- Accuracy
- Repeatability
- Energy usage

Compare controllers quantitatively.

---

## ⭐ Add-On 5: Model Validation Experiments

**Phase:** 5

### What You Do
- Predict motion using the identified model
- Compare predicted vs real behavior
- Quantify mismatch

**Resume:**  
> Validated physics-based models against real-world experimental data

---

## Phase ≤5 Checklist

### INCLUDED
- 3-DOF robotic arm
- Sensors and automatic logging
- PID control
- System identification
- Simple optimization
- Kinematics-based simulator
- Calibration and benchmarking

### EXCLUDED (For Now)
- Reinforcement learning
- High-fidelity digital twin
- Predictive maintenance
- Vision

---

## Final Verdict

If you stop at **Phase 5**, the project is:

- ✅ Intern-ready  
- ✅ Technically deep  
- ✅ Fun to build  
- ✅ Expandable later  
- ❌ Not overambitious  

This is exactly where strong students stop — and smart ones leave room to grow.

---

# Optional Extension: PS5 Controller Integration (Phase ≤5 Safe)

Connecting a PS5 controller is **not a gimmick** if framed correctly.

---

## Best Phase to Add
**Phase:** 3–4  
After stable PID control, before optimization.

---

## What It Is vs What It Is Not

### ❌ Not
- Gaming the robot
- Replacing autonomy

### ✅ Is
- Teleoperation interface
- Data collection tool
- Baseline benchmark

---

## Concrete Uses (Ranked by Value)

### ⭐ 1. Teleoperation for Data Collection
Map controller inputs to joint velocities and log:
- Joint angles
- Velocities
- Timestamps

Creates:
- Demonstration trajectories
- Realistic motion profiles
- Future training/validation data

**Resume:**  
> Designed a human-in-the-loop teleoperation interface for robotic data collection

---

### ⭐ 2. Baseline Controller Comparison
Compare:
- Human teleoperation
- PID control
- Optimized trajectories

Metrics:
- Smoothness
- Time to target
- Repeatability

---

### ⭐ 3. Safety and Limits Testing
Enforce:
- Joint limits
- Velocity caps
- Emergency stop (PS button)

---

### ⭐ 4. Mode Switching
Controller buttons:
- Manual mode
- Autonomous mode
- Replay recorded trajectory

---

## Tech Stack

### Software
- Python
- pygame or inputs
- Serial / USB / WiFi communication

### Hardware
- PS5 controller (Bluetooth or USB)
- ESP32 or Arduino

No additional cost.

---

## Resume Impact Summary

- Teleop alone: 🟢  
- Teleop + logging: 🟢🟢  
- Teleop vs optimization: 🟢🟢🟢  
- Teleop → imitation learning (future): 🟢🟢🟢🟢  

---

## Bottom Line

PS5 controller integration is:
- Fun
- Resume-safe
- Technically meaningful
- A clean bridge to ML later
