# ⚙️ Phase 0 – Assumptions & Constraints (Rev 5.2)

---

## 1️⃣ Assumptions

### General Architecture
The "Split-Brain" Reality assumes a distributed control topology:

- **PC (Python):** The high-level "Brain" handling kinematics, trajectory planning, and safety arbitration.  
- **Teensy 4.1:** The hard real-time "Motion Core" handling step generation (1 kHz tick), acceleration ramps, and hardware safety.  
- **ESP32-C3:** A strictly non-blocking telemetry bridge (no motion authority).

**Collaborative Roles:**

- **ME (Mechanical Engineer):** Owns the physical reliability, firmware execution (Teensy), and hardware safety (E-Stop).  
- **DS (Data Scientist):** Owns the motion planning (Python), trajectory optimization, and anomaly detection algorithms.

---

### Mechanical & Physical Design
- **6-DOF Configuration:** 6 active joints (Base, Shoulder, Elbow, Wrist P, Wrist R, Gripper).  
- **Gravity Assist (J3):** J3 (Elbow) has a non-linear torque profile due to the gravity assist spring. Simulations must account for this "assisted" load.  

**Transmission Realities:**

- Gear ratios are fixed (10:1 to 25:1).  
- Backlash is present but modeled as "zero" for initial kinematics; later added as a "noise factor" for encoder data simulation.

---

### Stepper Control & Latency
- **Discrete Time:** Motion is a series of discrete hardware timer interrupts; simulations must validate Teensy can handle step rates for 6 simultaneous axes.  
- **Buffered Execution:** Python planner must account for latency window (100–500ms buffered motion).  
- **Trapezoidal First:** Phase 0 validates trapezoidal velocity profiles (Phase 1 MVP); data structure must support S-Curve parameters (Phase 2) without breaking.

---

### Kinematics & Simulation
- **3D Space:** Verification requires 3D visualization (Matplotlib 3D, RoboDK, or Python OpenGL) to check for self-collisions in 6-DOF space.  
- **Inverse Kinematics (IK):** Analytical or robust numerical solution exists for this specific link configuration (likely a spherical wrist variant).  
- **Safety Limits:** Soft limits (software) and hard limits (physical) are distinct. Teensy enforces soft limits autonomously if PC crashes.

---

## 2️⃣ Constraints

### Scope & Timebox
- **Hardware-Free Zone:** Phase 0 is strictly Calculation, Simulation, and Protocol Definition. No soldering or machining.  

**Deliverables:**

- Validated DH Parameters for the 6-DOF chain  
- Defined "Motion Packet" structure (Rev 5.2 Standard)  
- Simulated "Heartbeat" failure test

---

### Mechanical Constraints
- **Payload Envelope:** Arm constrained to 2.0 kg, dependent on the J3 spring. Trajectories exceeding torque limits flagged "Invalid" by Python planner.  
- **Motor Limits:**  
  - J1/J2 (NEMA 23): High torque, lower max RPM  
  - J5/J6 (NEMA 11): Low torque, thermal sensitivity  
- **Cable Drag:** Reduce effective torque due to drag chains/cabling (10–15% safety margin)

---

### Software & "Hardened" Safety Constraints
- **Heartbeat Rule:** Loss of comms triggers controlled deceleration. Phase 0 architecture ensures the arm cannot keep moving if Python freezes.  
- **Teensy Authority:** Teensy never executes step commands violating physical acceleration limits, regardless of Python requests.  
- **USB vs. Wi-Fi:**  
  - USB: Motion Commands (Deterministic)  
  - Wi-Fi: Telemetry Only (Non-Deterministic)

---

### Data & Protocol Schema (Rev 5.2)
- **Packet Design:** Define exact byte structure for `<SegID, Velocities, Duration>`  
- **Encoder Integration:**  
  - Phase 1: J3 feedback for stall detection  
  - Phase 2: Full 6-axis feedback  
- **Logging:** Simulation data must match hardware log format for "Sim-to-Real" validation

---

## 3️⃣ Next Steps (Phase 0 Execution)
1. Define the **DH Parameters table** for the 6 joints  
2. Write the **Python Class Structure** (e.g., `RobotController`, `TrajectoryPlanner`, `SafetyMonitor`)  
3. Simulate a `"Move J1 to 90°"` command and plot the **Trapezoidal Velocity Profile vs. Time**