# ⚖️ Task Split & Governance

## Purpose
Division of Labor and Separation of Concerns between the two primary engineers:

- **Mechanical Engineer (ME):** Your Brother  
- **Data Scientist (DS):** You  

Under the Split-Brain Architecture, tasks are not just assigned based on skill, but on **System Authority**:

- **ME owns the Hardware & Reflex (Teensy)**  
- **DS owns the Strategy & Judgment (Python)**

---

## 1. The Core Philosophy: "Tension Model"
We do not just "help each other." We act as **checks and balances**.

| Domain | Owner | Core Responsibility | Authority |
|--------|-------|-------------------|----------|
| Feasibility | ME | Making it move safely | **Veto Power:** Can refuse to run code that looks physically unsafe |
| Truth | DS | Measuring how well it moved | **Blocking Power:** Can refuse to proceed to the next phase if data shows instability |

---

## 2. Mechanical Engineering (ME) — "The Body & Reflex"
The ME builds the physical machine and the hard real-time firmware that protects it.

### A. Hardware & Electronics
- **CAD Design:** Fusion 360 models, printable parts, and gear design  
- **Electrical Build:** Soldering, crimping, wire management (Star Topology)  
- **Noise Suppression:** Installing ferrites, capacitors, and shielding  
- **Safety Rig:** Building the E-Stop loop and PSU mount

### B. Embedded Firmware (Teensy 4.1)
- **Motion Core:** Writing the C++ timer interrupts for step generation  
- **Safety Invariants:** Coding the hard limits, thermal checks, and watchdog  
- **Buffer Logic:** Managing the ring buffer that receives commands  
- **Sensor Drivers:** Writing the low-level I²C/SPI code to read encoders  

**Primary Deliverable:** A machine that holds position, accepts commands, and triggers E-Stop if disconnected.

---

## 3. Data Science (DS) — "The Brain & Conscience"
The DS acts as the pilot (sending commands) and the auditor (grading performance).

### A. Control Strategy (Python)
- **Trajectory Planner:** Writing the IK solvers and path generation logic  
- **Dashboard:** Building the real-time visualization tool (PyQt/Matplotlib)  
- **Teleop Mapping:** Converting PS5 controller inputs into safe velocity vectors

### B. Data & Analysis
- **Telemetry Pipeline:** Parsing binary packets from the ESP32  
- **Signal Processing:** Analyzing encoder noise (FFT), jitter, and steady-state error  
- **System ID:** Calculating real-world friction, gravity, and backlash from logs  
- **Acceptance Testing:** Defining metrics (e.g., "Max Error < 0.5°") required to pass a Mini-Project  

**Primary Deliverable:** Verified plots proving the robot is ready for the next phase.

---

## 4. The "Demilitarized Zone" (Shared Tasks)
These are the boundaries where the two domains meet and require **Synchronous Collaboration**.

### A. The API Contract
- Define the packet structure (Bytes, Headers, Checksums)  
- **Why:** ME needs to parse it (C++); DS needs to pack it (Python). If this drifts, the robot crashes.

### B. Hardware-in-the-Loop (HIL) Integration
- The physical day where Python is first connected to the Teensy  
- **ME manages:** E-Stop button  
- **DS manages:** Run button

### C. Troubleshooting
- **When the arm oscillates:**  
  - ME checks belt tension and driver current  
  - DS checks PID gains and latency logs

---

## 5. Execution by Phase

### Mini-Project 1: Single Axis
- **ME:** Wires the NEMA 17, Driver, and Encoder; writes basic "Step + Read" firmware  
- **DS:** Writes the script to step 100 times and plot the encoder error  
- **Decision:** DS reviews the plot. If noise > threshold, ME rewires with ferrites

### Mini-Project 2: Coordination
- **ME:** Wires 3 motors; updates firmware to handle multi-axis buffering  
- **DS:** Writes a "Circle" trajectory generator  
- **Decision:** DS compares the "Circle" in Python vs. the "Circle" in Encoder logs

### Phase 4: Full Build
- **ME:** Prints and assembles the plastic arm  
- **DS:** Calibrates the gravity compensation constants in the Python model

---

## 6. Conflict Resolution Rules
- **Safety Wins:** If ME says "The motor is getting too hot," we stop. No debate.  
- **Data Wins:** If DS says "The encoder variance is too high," we do not add load. We fix the noise.  
- **Code Wins:** The Architecture.md is the law. We do not hack "quick fixes" that violate the Split-Brain design

---

## Guiding Principle
> "ME builds the vehicle. DS provides the map and the black box recorder."

This ensures clear authority boundaries while maintaining safe, data-driven development.
