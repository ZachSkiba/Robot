# 🦾 Robotic Arm Mini-Projects — Data Science Roadmap

**Role:** Data Science (DS) Lead / Software Lead  
**Philosophy:** Virtual-First, Hardware-Gated.  
**Objective:** The hardware never moves unless the software has already proven it is safe to do so.

---

## 🟢 Mini-Project 1 — Single-Joint Control + Data Contract
**Goal:** Master the feedback loop (PID), data logging, and "Truth" metrics.  
**Hardware Trigger:** Completion of Phase 0 allows the ME to power on the motor.

### 📅 Phase 0 — Virtual Execution (2–3 Weeks)
*Work to be done while waiting for Cart 1 components.*

#### **Week 1: The Foundation & Schema**
- [ ] **Define the Data Contract (Logging Schema)**
    - Create a specification for the ME. The CSV/Log must contain:
    - `timestamp_ms`: Time since boot.
    - `command_id`: Unique ID for the move command.
    - `target_position`: Where we want to be.
    - `actual_position`: Where the encoder says we are.
    - `velocity`: Computed derivative of position.
    - `pwm_effort`: The "force" applied (0-255).
    - `fault_flags`: (Binary) Over-temp, E-stop triggered, etc.
- [ ] **Set up Project Structure**
    - Create git repo with folders: `src/simulation`, `src/analysis`, `logs/`, `docs/`.
- [ ] **Implement Virtual Joint Simulation**
    - Write a Python class `MockMotor` that accepts a target and updates an `actual_position` variable.
    - Implement basic trajectories: `step()` (instant move), `ramp()` (gradual move), `hold()` (stay still).

#### **Week 2: Complexity & Metrics**
- [ ] **Enhance Simulation Fidelity**
    - Add **Noise:** Inject random Gaussian noise into the `actual_position`.
    - Add **Lag:** Make the `actual_position` take time to catch up to `target`.
    - Add **Thermal Proxy:** Create a variable that rises when `velocity` is high.
- [ ] **Develop the "Verdict" Dashboard**
    - Write a script (Jupyter/Python) that ingests the logs and plots:
        - **Error vs. Time** (Target - Actual).
        - **Velocity Profile** (Smoothness check).
- [ ] **Define Acceptance Criteria (The "Pass" Line)**
    - *Example:* "Steady-state error must be < 1.0° for 5 seconds."
    - *Example:* "Noise standard deviation must be < 0.05°."

#### **Week 3: Statistical Validation**
- [ ] **Monte Carlo Trials**
    - Run the simulation 100 times with random parameters to ensure the code doesn't crash.
- [ ] **Automated Anomaly Detection**
    - Write a script that scans logs and flags any timestamp where `error > threshold`.
- [ ] **Generate "Phase 0 Performance Report"**
    - A document showing the plots of the simulation proving the logging and analysis pipeline works.

### 🚀 Phase 1 — Hardware Execution (Post-Delivery)
*Work to be done once the motor and microcontroller are on the desk.*

- [ ] **Connectivity Test:** Verify Python can handshake with the Teensy.
- [ ] **Noise Floor Analysis:** Log the motor at rest; measure real sensor noise.
- [ ] **PID Tuning Assistant:** Use your Dashboard to advise the ME on tuning (increase P, decrease D, etc.).
- [ ] **Final Verdict:** Run the standard test trajectory and issue a **Pass/Fail** for the hardware joint.

---

## 🟡 Mini-Project 2 — Multi-Joint Coordination + Model Validation
**Goal:** Validate Kinematics (FK/IK) and ensure two joints can move without fighting each other.

### 📅 Phase 0 — Virtual Coordination (1–2 Weeks)
*Can be started alongside MP1 Phase 1.*

#### **Week 1: The Math (FK/IK)**
- [ ] **Implement Forward Kinematics (FK)**
    - Python function: `get_end_effector_xy(angle1, angle2)`.
- [ ] **Implement Inverse Kinematics (IK)**
    - Python function: `get_joint_angles(target_x, target_y)`.
- [ ] **Validation Loop**
    - Feed random angles into FK, then the result into IK. Verify you get the original angles back.

#### **Week 2: Trajectory & Synchronization**
- [ ] **Coordinated Trajectory Generation**
    - Create a path (e.g., a straight line in X/Y).
    - Convert that line into a stream of time-synced angles for Joint 1 and Joint 2.
- [ ] **Lag & Drift Analysis**
    - Simulate one joint being slightly slower than the other.
    - Plot the "Path Deviation" (how far the tip is from the straight line).
- [ ] **Phase 0 Coordination Report:** Validate that your math holds up for 1000 random points.

### 🚀 Phase 1 — Hardware Coordination
- [ ] **Ghost Replay:** Feed the "straight line" angles to the real motors.
- [ ] **Latency Test:** Measure the time delta between commanding J1 and J2.
- [ ] **Correlation Analysis:** Prove that J1 and J2 start and stop at the exact same time.

---

## 🔴 Mini-Project 3 — Integration, Replay, & Judgment
**Goal:** The final "Brain" of the system. Enforcing safety and judgment logic.

### 📅 Phase 0 — Virtual Judgment System (1–2 Weeks)

- [ ] **The "Black Box" Recorder**
    - Ensure every session automatically saves a timestamped log file.
- [ ] **Heartbeat & Timeout Logic**
    - Write logic: "If no data received for 500ms, assume hardware died and flag ERROR."
- [ ] **Automated Health Verdict**
    - Build a final script that takes a log file and outputs: `STATUS: GREEN/YELLOW/RED`.
    - **Green:** All metrics within spec.
    - **Yellow:** Minor overshoot or noise.
    - **Red:** Safety limits hit or E-stop triggered.

### 🚀 Phase 1 — Hardware Integrity
- [ ] **E-Stop Validation:** Physically hit the E-stop and verify the software flags it immediately.
- [ ] **Stress Test:** Run the arm for 10 minutes and check for thermal drift in the logs.
- [ ] **Final System Health Report:** The "Diploma" for the robot arm.

---

## 📚 Ongoing Infrastructure (Carry Forward)
*Tasks to maintain throughout the project.*

* **Metric Library:** Keep your plotting code modular (`plot_error.py`, `calc_rmse.py`) so you can reuse it.
* **Documentation:** Keep `data_schema.md` updated if you change column names.
* **Version Control:** Commit your analysis scripts to GitHub.

---

## 📝 Deliverable Summary Table

| Mini-Project | Phase 0 (Virtual) Deliverable | Phase 1 (Hardware) Deliverable |
| :--- | :--- | :--- |
| **MP1** | Simulated Logs & Error Plots | Real PID Tuning Report |
| **MP2** | FK/IK Validation Report | Multi-Joint Sync Analysis |
| **MP3** | Auto-Verdict Script | Final System Certification |