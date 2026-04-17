# ⚠️ Risks and Unknowns (Rev 2.0)

**Context:** Aligned to Master Blueprint Rev 5.2 (Split-Brain Architecture)  
**Purpose:** This document captures the specific engineering gambles inherent in the Rev 5.2 architecture. These are not bugs; they are the constraints we have chosen to accept.

---

## 1. Mechanical & Thermal Risks

### 1.1 Plastic Gearbox Thermal Deformation (NEMA 23)

**Risk:**  
The NEMA 23 motors (Base/Shoulder) can reach surface temperatures of **60°C–80°C** under load.

**Context:**  
Printed **PETG/PLA gears** are used directly coupled to or near these heat sources.

**Impact:**
- Gears may soften, leading to tooth skipping or catastrophic stripping.
- Press-fit shafts may loosen as plastic expands.

**Mitigation:**
- **Active Cooling:** Heatsinks/fans on NEMA 23s are mandatory if temps exceed 50°C.
- **Material Upgrade:** Switch to ABS, ASA, or Nylon for motor-contact parts if PETG fails.
- **ME Owner:** Monitor motor temps during **Phase 3 (Tractor)** stress tests.

---

### 1.2 The “J3 Gravity Spring” Singularity

**Risk:**  
Joint 3 (Elbow) relies on a passive extension spring to counteract gravity for a **2.0 kg payload**.

**Impact:**
- **Non-Linearity:** Springs are not perfectly linear; control models may fight the spring at certain angles.
- **Fatigue:** If the spring weakens, the NEMA 17 will stall, as it is undersized for the full unassisted load.

**Mitigation:**
- **Tunable Mount:** Adjustable spring attachment point (e.g., screw tensioner).
- **Current Limits:** Strict current limits on J3 to immediately detect stalls (DS task).

---

### 1.3 Backlash in Printed Planetaries

**Risk:**  
Printed planetary gearboxes (J1, J4) introduce significantly more backlash than machined gears.

**Impact:**
- Encoder (joint) and motor (step count) disagree during direction changes.
- PID loops may oscillate while correcting this “dead zone.”

**Mitigation:**
- **Unidirectional Approach:** Motion planning may need to approach targets from a single direction.
- **DS Task:** Characterize backlash width (in degrees) during **Phase 5**.

---

## 2. Electrical & Signal Integrity Risks

### 2.1 I²C Bus Capacitance (The “Long Wire” Problem)

**Risk:**  
Rev 5.2 uses AS5600 encoders (I²C) distributed across the arm. Standard I²C is designed for PCB traces, not **6-foot cables**.

**Impact:**
- Signal reflections or capacitance can lock the bus (SDA stuck low).
- Phantom sensor readings.

**Mitigation:**
- **Differential Transceivers (Critical):** PCA9615 or LTC4311 boards are required for reliability.
- **Low Frequency:** Run I²C clock at **≤ 100 kHz** initially.

---

### 2.2 Ground Loops in the “Star” Topology

**Risk:**  
High-current devices (NEMA 23) and sensitive logic (Teensy/ESP32) share a single PSU.

**Impact:**
- Motor acceleration causes voltage dips that reset the ESP32 (brownout).
- Ground noise injects false steps into motor drivers.

**Mitigation:**
- **Strict Wiring:** Power and ground wires go from *component → PSU terminal*. Never daisy-chain.
- **Capacitor Decoupling:** Every driver requires a **100µF capacitor** at its power input.

---

## 3. “Split-Brain” Control Risks

### 3.1 Python ↔ Teensy Synchronization

**Risk:**  
The PC (Python) plans trajectories; the Teensy executes them. Windows/Python is not real-time.

**Impact:**
- **Buffer Underrun:** Python garbage collection pauses can starve the Teensy of motion segments.
- **Latency Jitter:** Python-side timestamps may not align with physical execution.

**Mitigation:**
- **Deep Buffering:** Teensy must hold **≥ 500 ms** of motion segments.
- **Keep-Alive Protocol:** Heartbeat system ensures safe halt if Python crashes.

---

### 3.2 The “Blind” Motion Planner

**Risk:**  
Phase 1 uses open-loop stepping. The Teensy assumes the motor moved as commanded.

**Impact:**
- Missed steps permanently offset internal state until re-homing.
- Robot may collide with physical stops while believing it is safe.

**Mitigation:**
- **Encoder Truth:** Monitor encoders even if not used for closed-loop control.
- **Deviation E-Stop:** If  
  \[
  |\text{Encoder Angle} - \text{Step Angle}| > \text{Threshold}
  \]  
  → **HALT immediately**.

---

## 4. Data Science & Validation Risks

### 4.1 Timestamp Drift

**Risk:**  
Telemetry from Wi-Fi (ESP32) and USB (Teensy) creates two independent timelines.

**Impact:**
- Impossible to correlate voltage spikes (Teensy) with disconnect events (ESP32).

**Mitigation:**
- **Master Clock:** `Teensy micros()` is the single source of truth.
- ESP32 packets must be timestamped by the Teensy before transmission.

---

### 4.2 “Over-Fitting” to Hardware Flaws

**Risk:**  
DS may optimize trajectories that work only on this exact robot configuration.

**Impact:**
- A fragile “golden sample” controller that fails with minor mechanical changes.

**Mitigation:**
- **Vary Parameters:** Run tests across different payloads and speeds to ensure robustness.

---

## 5. Unknown Unknowns

- **EMI vs Wi-Fi:** Will NEMA 23 coils act as antennas and jam ESP32 Wi-Fi?
- **PS5 Controller Safety:** Can a user issue commands faster than the plastic arm can physically tolerate, snapping a gearbox?

---

## 🛡️ Risk Management Strategy

**“Fail Fast, Fail Cheap”**

- **Phase 0 (Virtual):**  
  If Python logic cannot handle a simulated buffer underrun, **do not power the system**.

- **Phase 1 (Electrical):**  
  If the I²C signal looks messy on an oscilloscope, **do not mount the encoders**.

- **Phase 3 (Tractor):**  
  If a NEMA 23 melts a PETG mount, **change materials before full arm assembly**.