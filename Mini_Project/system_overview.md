# 🦾 Robotic Arm Project

## Mini-Projects — Production-Grade Foundations

**ME + DS Parity · 6-DOF-Ready · Virtual → Hardware-Gated**

---

## Design Philosophy (Non-Negotiable)

These mini-projects exist to answer one question:

> **Can this team design, validate, and govern a safety-critical electromechanical system using quantitative evidence before physical risk is introduced?**

Every task must:

* Scale directly to a **6-DOF arm**
* Produce **reusable artifacts** (code, data, plots, reports)
* Give **ME and DS real decision authority**
* Be **stoppable the moment it is validated**

Anything that violates these rules is excluded.

---

## Global Collaboration Model

*(Applies to All Mini-Projects)*

* ME and DS work **in parallel every week**
* Shared interfaces are defined **before motion**

### Authority (Explicit)

* **ME** owns *actuation feasibility* and *safety enforcement*
* **DS** owns *metrics*, *acceptance criteria*, and *go / no-go decisions*
* **Either side can block progression*

This is intentional tension.

---

## 🎮 Human-in-the-Loop Control (PS5 Controller)

**Present throughout all mini-projects, never dominant**

### Purpose

The controller is **not** for driving the robot.
It exists to test whether unpredictable human input can be:

* Filtered
* Rate-limited
* Logged
* Governed
* Rejected when unsafe

If human input can bypass safety or metrics, the system is invalid.

### Global Rules

* Controller is just **another command source**
* Same limits, filters, and logging as scripted motion
* Never talks directly to hardware
* Never generates motion segments directly

Always overridden by:

* E-stop
* Safety logic
* DS verdicts

---

## Fixed Architecture

*(Mini-Projects → 6-DOF)*

```
PS5 Controller
      ↓
Python Input Layer (DS-owned)
      ↓
Command Mapping + Filtering
      ↓
Rate / Accel / Limit Enforcement
      ↓
Unified Motion Command API
      ↓
MCU Behavioral Contract
      ↓
Motor Drivers
```

> **Phase 0:** MCU Behavioral Contract is simulated
> **Phase 1+:** MCU Behavioral Contract is enforced on real hardware

This architecture **never changes**.

---

## 🧩 Mini-Project 1

## Single-Axis Control + Data Contract

*(Foundation of the Entire Robot)*

### Why This Exists

Every failure mode of a 6-DOF arm exists in one joint:

* Overshoot
* Oscillation
* Thermal runaway
* Encoder noise
* Missed steps
* Unsafe limits

If one joint is not **provably stable**, the arm is fiction.

---

### Phase 0 — Virtual Execution

#### ME Responsibilities — Control & Safety Authority *(Virtual)*

* Define theoretical actuator envelope:

  * Max velocity
  * Max acceleration
  * Thermal proxy limits
* Implement virtual stepper / joint model
* Implement:

  * Soft limits
  * Velocity & acceleration limits
  * Safety invariants and halt conditions
  * Simulated E-stop dominance

**Execute virtual trajectories**

* Step
* Ramp
* Hold

**Deliverables**

* Declared operating envelope
* Virtual joint model
* Safety invariant definitions

---

#### DS Responsibilities — Truth & Acceptance Authority *(Virtual)*

* Define logging schema before motion
* Build plots:

  * Error vs time
  * Velocity vs command
  * Constraint violations
* Quantify:

  * Noise floor
  * Steady-state error
  * Overshoot
* Implement anomaly flags

**Deliverables**

* Clean dataset
* Statistical characterization
* Explicit pass / fail criteria

---

### Phase 1 — Hardware Execution *(Unlocked Only After Phase 0 Gate)*

#### ME Responsibilities — Physical Control & Safety

* Wire motor, driver, encoder
* Implement control logic (PID / stepper profiles)
* Enforce:

  * Hardware E-stop dominance
  * Velocity & acceleration limits
  * Soft limits
* Execute repeatable trajectories under load

**Deliverables**

* Control gains
* Electrical diagram
* Declared physical operating envelope

---

#### DS Responsibilities — Physical Validation

* Log real sensor data:

  * Position
  * Velocity
  * Current
  * Fault flags
* Quantify:

  * Tracking error
  * Thermal trends
  * Current spikes

**Deliverables**

* Hardware performance report
* Updated acceptance verdict

---

### 🔒 Mandatory Gate

📦 **Single-Joint Performance Report (Shared)**

* ME: control strategy, limits, failure handling
* DS: error distributions, noise stats, stability verdict

Failure blocks all progression.

---

## 🧩 Mini-Project 2

## Multi-Joint Coordination + Model Validation

*(Math ↔ Physics Contract)*

### Phase 0 — Virtual Coordination

* ME implements FK / IK for 2–3 joints
* DS validates predicted vs simulated behavior
* Error bounds defined by DS

### Phase 1 — Hardware Coordination

* ME executes coordinated trajectories
* DS validates lag, drift, correlation error

---

## 🧩 Mini-Project 3

## Integration, Replay, and System Judgment

*(What Makes This Serious)*

### Phase 0 — Judgment System

* Simulated motion buffering
* Heartbeat timeout logic
* Trajectory replay validation

### Phase 1 — Hardware Integrity

* EMI robustness
* E-stop dominance
* Hardware fault classification

---

## 🧠 Final Deliverable

## Automated Health Verdict System

**Input**

* Trajectory log (scripted or human)

**Output**

* OK / Warning / Fault

ME may not increase speed, payload, or complexity unless DS verdict allows it.

---

## 📊 Final Summary

| Mini-Project | Phase 0 Focus           | Phase 1 Focus             | 6-DOF Carry-Forward |
| ------------ | ----------------------- | ------------------------- | ------------------- |
| 1            | Virtual joint stability | Hardware joint validation | Joint template      |
| 2            | Model correctness       | Coordinated execution     | FK/IK + metrics     |
| 3            | Judgment logic          | System integrity          | Full-arm governance |

---

**Time:** 3–4 weeks @ 10 h/week/person
**Waste:** None
**Carry-forward:** ~90%

---

## Final Verdict

This is not *"a robotics project with data."*

This is a **governed cyber-physical system with enforced gates**.