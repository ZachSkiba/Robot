# Mini-Projects — Assumptions & Constraints  
*(Aligned with Governed, Virtual → Hardware-Gated Architecture)*

---

## Assumptions

### System-Level (Applies to All Mini-Projects)

- The project is executed under a **virtual-first, hardware-gated model**:
  - No hardware motion occurs until **Phase 0 acceptance gates** are passed.
- The system is designed to **scale to a 6-DOF arm** without architectural changes.
- **ME and DS roles are non-overlapping and enforceable**:
  - **ME** provides feasibility analysis and safety mechanisms.
  - **DS** defines truth, metrics, and go / no-go decisions.
- **Python** is available as the primary orchestration, logging, and analysis environment.
- All motion—scripted or human—passes through the **same command, filtering, and safety pipeline**.
- The MCU is treated as a **behavioral contract**, not an implementation detail.
- All safety logic (limits, E-stop dominance, halts) is **modeled before hardware exists**.

---

### Mini-Project 1 — Single-Axis Control + Data Contract

- One actuator (stepper + driver) and one joint are sufficient to expose:
  - Stability limits
  - Control pathologies
  - Sensor noise
  - Safety failures
- Virtual joint dynamics are representative enough to:
  - Validate control logic
  - Define safe operating envelopes
  - Detect unstable behavior
- Sensor feedback (encoder, step count, or equivalent) is:
  - Observable
  - Timestamped
  - Loggable
- Classical control (PID / stepper profiling) is sufficient to achieve **bounded, stable behavior** at this scale.
- Any instability discovered in a single joint is assumed to **compound in a multi-joint arm**.

---

### Mini-Project 2 — Multi-Joint Coordination + Model Validation

- Forward and inverse kinematics for **2–3 joints** are sufficient to:
  - Validate mathematical models
  - Detect coordination and timing errors
- Virtual coordination errors are assumed to be **lower bounds** on hardware error.
- DS-defined error metrics meaningfully reflect **physical coordination quality**.

---

### Mini-Project 3 — Integration, Replay, and System Judgment

- Logged trajectories are sufficient to:
  - Reconstruct system behavior
  - Classify faults
  - Generate automated verdicts
- Faults can be categorized meaningfully (e.g., timing, saturation, EMI, dropout) even in early hardware.
- A system that cannot **judge its own behavior** is considered **unsafe by default**.

---

## Constraints

### Governance & Process (Hard Constraints)

- **Phase 0 must complete and pass acceptance gates before Phase 1 begins.**
- Either **ME or DS may block progression** without consensus.
- No component may bypass:
  - Safety logic
  - Rate / acceleration limits
  - Logging and metrics
- Human input (PS5 controller):
  - Is never dominant
  - Never talks directly to hardware
  - Never generates motion segments
- Mini-projects are **stopped immediately once validated**.
  - Additional optimization beyond acceptance criteria is **forbidden**.

---

### Technical & Safety Constraints

- All commanded motion must respect:
  - Declared velocity limits
  - Declared acceleration limits
  - Declared positional limits
- **E-stop dominance** must override *all* command sources, virtual or physical.
- Motor current, temperature proxies, and duty cycle must remain within:
  - Datasheet limits
  - DS-approved operating envelopes
- No hardware test may risk:
  - Thermal runaway
  - Mechanical damage
  - Loss of human control
- Sensors and MCUs must operate strictly within **voltage and timing specifications**.

---

### Scope Constraints

- **Mini-Project 1**
  - Exactly one joint
  - No payload scaling
  - No multi-axis coupling
- **Mini-Project 2**
  - Maximum 2–3 joints
  - Coordination only; no payload optimization
- **Mini-Project 3**
  - Focused on integrity and judgment, not performance gains
- No machine learning, adaptive control, or optimization layers are permitted.
- No hardware redesign is allowed during mini-project execution.

---

## Exit Conditions (Non-Negotiable)

- A mini-project is considered **complete only when**:
  - Metrics are computed
  - Acceptance criteria are evaluated
  - A written verdict exists
- Failure to meet criteria **halts progression**, not “inspires iteration.”
- Phase 1 hardware work begins **only after DS issues a pass verdict**.

---

## Bottom-Line Constraint

If a behavior cannot be:

- Logged  
- Quantified  
- Judged  
- And stopped safely  

**It is not allowed to exist in the system.**