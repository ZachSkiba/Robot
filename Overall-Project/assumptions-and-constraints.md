# 📜 Assumptions & Constraints

---

## 1. Assumptions (System Modeling)

These are the simplifications we accept to make the math solvable.  
**If these assumptions are false, the control theory fails.**

---

### ⚙️ Mechanical

- **Finite Stiffness**  
  We assume links are rigid, but we acknowledge **Joint 3 (Elbow)** will exhibit elastic deflection under the **2.0 kg max load**.  
  This deflection is assumed to be repeatable (consistent hysteresis).

- **Gravity Compensation**  
  We assume the passive spring on **J3** reduces the holding torque required by the **NEMA 17** motor to  
  \[
  < 60\% \text{ of its holding torque rating}
  \]  
  The spring does not need to be perfect—only sufficient to prevent thermal overload.

- **Planar Base**  
  The mounting surface is assumed to be perfectly rigid and level.  
  Any vibration is attributed to the arm itself, not the supporting structure.

---

### ⚡ Electrical & Signal

- **Noisy Environment**  
  The chassis is assumed to be an EMI-hostile environment.  
  Stepper cables will broadcast noise. Standard single-ended signals (e.g., I²C) are assumed to fail over cable runs longer than **20 cm**.

- **Logic Isolation**  
  USB power is assumed to be noisy and electrically separate from the clean **3.3V logic rail** required by sensors.

- **Star Grounding**  
  All high-current return paths must go directly to the PSU.  
  This prevents ground bounce on the driver side from shifting logic thresholds on the **Teensy**.

---

### 🧠 Control & Software

- **Host is Non-Deterministic**  
  The Python host (PC) is not real-time.  
  Packet arrival times may jitter by **±20 ms**.  
  The Teensy must buffer sufficient motion data to survive these gaps.

- **Kinematic Decoupling**  
  The Wrist assembly (**J4/J5/J6**) is assumed to have sufficiently low mass such that its dynamics do not significantly perturb the **Base/Shoulder (J1/J2)** control loops.

---

## 2. Constraints (Hard Requirements)

These are **binary pass/fail limits**.  
Violating any constraint risks hardware damage or safety failure.

---

### 🛑 Safety & Hardware Protection

- **Logic Voltage Cap**  
  Strictly **3.3V logic only**.  
  Any sensor or driver interface exceeding 3.3V is forbidden.  
  Level shifting is mandatory for 5V components (e.g., **DM556T** inputs).

- **E-Stop Authority**  
  The physical **Emergency Stop** must directly cut **24V High Power** to the motor drivers.  
  Software-based stops (Teensy-controlled) are not acceptable.

- **Thermal Ceiling**  
  Stepper motors must not exceed **80 °C case temperature** during a **10-minute hold cycle** at maximum payload.

---

### 🔌 Electrical & Communication

- **Power Budget**  
  - 24V DC Rail  
  - 15A maximum (360W total)

- **Sensor Interface**  
  Any encoder located more than **10 cm** from the Teensy must use:
  - Differential I²C (**PCA9615 / LTC4311**), or  
  - **RS-485**

  Standard ribbon cables for I²C are explicitly banned.

- **Heartbeat Timeout**  
  If the Teensy does not receive a valid **Keep Alive** packet from Python within **250 ms**,  
  it must autonomously decelerate all joints to a halt.

---

### 💻 Real-Time Performance

- **Tick Rate**  
  Motion Planner on the Teensy must run at **≥ 1 kHz (1000 Hz)**.

- **Step Generation**  
  Step pulses must be generated using **hardware timers** (interrupt-driven), not the main loop.  
  Allowed jitter:  
  \[
  < 1\ \mu s
  \]

- **Latency Budget**
  - USB round-trip: **< 5 ms (average)**
  - Wi-Fi telemetry: **< 50 ms**  
    *(Acceptable for data only — forbidden for control loops)*

---

### 📐 Motion & Physics

- **Payload Envelope**  
  - 2.0 kg dynamic payload  
  - Within a **400 mm radius**

- **Velocity & Acceleration Limits**
  - Max joint velocity: **60°/sec** (hard safety cap)
  - Max acceleration:  
    Determined by *slip threshold*  
    \[
    \text{Required torque} < 80\% \text{ of motor pull-out torque}
    \]

- **Motion Profile**
  - **Phase 1:** Trapezoidal (infinite jerk acceptable)
  - **Phase 2:** S-curve (finite jerk required for data validity)

---

## 3. Operational Boundaries

Explicit behaviors the system **does not** support.

- **No Collision Detection (Phase 1)**  
  The robot assumes the workspace is empty.  
  It will not stop upon impact unless encoder deviation triggers a **Stall Fault**.

- **No Hot-Plugging**  
  Motors must **not** be connected or disconnected while the **24V rail is live**.  
  Doing so risks immediate driver destruction.

- **No Waterproofing**  
  The system is rated **IP20** — indoor / laboratory use only.

---
