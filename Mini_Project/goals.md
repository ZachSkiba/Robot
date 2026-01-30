# 🦾 Robotic Arm Project – Mini-Projects Goals

## General Goals for All Mini-Projects
- Unlock essential skills for full 6-DOF arm development.
- Gain confidence in safely handling hardware and software.
- Verify that fundamental systems (motor, sensor, controller) behave predictably.
- Maintain strict scope: learn efficiently, stop immediately when objectives are reached.
- Avoid full-arm builds, over-optimization, or advanced ML at this stage.
- Produce reusable artifacts (plots, logs, code, reports) for Phase 1 and beyond.

---

## Mini-Project A – Single-Axis Smart Joint
**Objective:** Master control and measurement of a single joint.

**Goals:**
1. Wire **one motor + one encoder** to the microcontroller.
2. Implement **PID-based feedback control**.
3. Write a Python interface to:
   - Send motor commands
   - Log encoder data
   - Plot **position, velocity, and error vs time**
4. Quantify joint behavior:
   - Sensor noise floor
   - Steady-state error
   - Response time & overshoot
5. Implement virtual & physical safety constraints:
   - Soft limits
   - Simulated E-stop
   - Halt conditions

**Completion Criteria:**
- Motor reliably reaches commanded positions.
- Error vs time plots demonstrate expected behavior.
- Joint performance report completed.
- Phase 1 hardware validation ready.

**Timeframe:** 5–7 days

---

## Mini-Project B – Controller → Motor
**Objective:** Implement human-in-the-loop control with logging.

**Goals:**
1. Connect **PS5 controller** via Python or MCU input layer.
2. Control **joint position or velocity** with joystick input.
3. Log **joystick input and motor response** simultaneously.
4. Replay recorded trajectories reliably.
5. Explore motor limits and smooth motion under human commands.
6. Confirm that **safety overrides** (E-stop, limits) always take precedence.

**Completion Criteria:**
- Motor moves smoothly according to joystick commands.
- Trajectories replay correctly.
- Safety limits never violated.

**Timeframe:** 3–4 days

---

## Mini-Project C – 2-Link Arm in Python (Optional / Virtual)
**Objective:** Build kinematic intuition without touching hardware.

**Goals:**
1. Simulate a **2-link planar arm** in Python.
2. Implement **Forward Kinematics (FK)**.
3. Implement **Inverse Kinematics (IK)** for reachable workspace points.
4. Visualize motion with **plots or animation**.
5. Compare FK predictions with IK solutions to validate correctness.

**Completion Criteria:**
- FK/IK algorithms produce correct positions.
- Motion plots match expected trajectories.
- Data and plots reusable for 6-DOF scaling.

**Timeframe:** 2–3 days

---

## Key Notes
- Mini-projects are **skill-focused, not design-focused**.
- **Gatekeeping:** no Phase 1 hardware work until Phase 0 goals are validated.
- Deliverables: **datasets, plots, code, joint reports** — all carry forward to full arm.
- Phase 0 → Phase 1 workflow ensures **safety, governance, and reproducibility**.