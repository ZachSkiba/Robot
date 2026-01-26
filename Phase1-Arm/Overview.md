# Phase 1 — Physical Arm Build + Telemetry

**Duration:** ~3–4 weeks  
**Goal:** Build a real 3-DOF robotic arm that moves repeatably, homes safely, and logs data automatically.

**Phase 1 success =** hardware behaves predictably and produces clean, reliable data.

---

## Phase 1 Outcomes

- Fully assembled 3-DOF robotic arm  
- Safe homing and enforced joint limits  
- Deterministic motion execution  
- Automatic data logging (no manual timing)  
- Closed hardware ↔ software loop established  

---

## Step-by-Step Plan (With Roles)

---

### STEP 1.1 — Translate Simulation → Physical Design (Days 1–3)

**Together**
- Lock:
  - Link lengths (from Phase 0)
  - Joint axes
  - Mounting strategy
- Decide transmission:
  - Belts **or** gears (do not mix yet)

**Zach (DS)**
- Export Phase-0 parameters:
  - Link lengths
  - Joint limits
- Define expected joint angle ranges
- Create configuration file (JSON / YAML)

**Nicholas (MechE)**
- CAD arm links and joints
- Design motor mounts
- Design base (rigidity > aesthetics)

**Interaction**
- CAD reviewed against simulation
- Simulation updated if CAD forces changes

---

### STEP 1.2 — Mechanical Assembly (Days 4–7)

**Nicholas (Lead)**
- 3D print / fabricate links
- Assemble joints
- Install bearings / bushings
- Ensure minimal wobble

**Zach (Support)**
- Measure assembled parts (calipers)
- Verify real dimensions match model
- Update kinematics parameters if needed

**Interaction**
- Physical measurements → software updates
- Both verify joint motion feels correct

---

### STEP 1.3 — Electronics & Wiring (Days 8–10)

**Together**
- Decide:
  - Arduino vs ESP32
  - Pin assignments
  - Power routing

**Nicholas**
- Wire:
  - Stepper motors
  - Drivers
  - Power supply
- Physically mount electronics
- Add strain relief (important)

**Zach**
- Create wiring diagram (draw.io or paper)
- Define firmware interface:
  - Command format
  - Data format

**Interaction**
- Firmware expectations match wiring reality
- No “mystery pins”

---

### STEP 1.4 — Homing & Safety (Days 11–13)

**Together**
- Decide homing direction per joint
- Define what “zero” means

**Nicholas**
- Mount limit switches
- Test mechanical stops
- Verify no self-collisions

**Zach**
- Implement homing logic in firmware
- Add joint limit enforcement
- Log homing data

**Interaction**
- Mechanical limits ↔ software limits aligned
- Repeat homing multiple times to verify repeatability

---

### STEP 1.5 — Motion Execution (Days 14–17)

**Zach**
- Send joint-space commands from Python
- Implement:
  - Velocity limits
  - Simple trajectories
- Plot commanded motion

**Nicholas**
- Observe physical motion:
  - Vibrations
  - Backlash
  - Missed steps
- Suggest mechanical or speed changes

**Interaction**
- Tune motion until it is:
  - Smooth
  - Repeatable
  - Safe

---

### STEP 1.6 — Telemetry & Logging (Days 18–21)

**Together**
- Finalize data schema (from Phase 0)

**Zach**
- Implement Python logger:
  - Timestamps
  - Commanded joint angles
  - Estimated joint angles
- Auto-save data every run

**Nicholas**
- Validate:
  - Data matches physical behavior
  - Repeatability between runs

**Interaction**
- Compare plots vs real motion
- Fix mismatches early

---

### STEP 1.7 — Phase 1 Deliverables (Days 22–24)

**Together**
- README:
  - Hardware overview
  - Wiring diagram
  - Homing process
- Demo:
  - Power on
  - Home arm
  - Move to target
  - Show plots

**Result**
> “We built a robotic arm with safe control, telemetry, and repeatable motion.”

That is a strong statement.

---

## Role Balance (Phase 1)

| Area                | Zach (DS) | Nicholas (MechE) |
|---------------------|-----------|------------------|
| CAD                 | ➖        | ✅               |
| Kinematics updates  | ✅        | ✅               |
| Wiring logic        | ✅        | ✅               |
| Firmware            | ✅        | ➖               |
| Mechanical tuning   | ➖        | ✅               |
| Data logging        | ✅        | ➖               |
| Validation          | ✅        | ✅               |
