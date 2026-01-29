# 🤖 6-DOF Robotic Arm — Final “Hardened” Design Blueprint (Rev 5.0)

**The "Research" Edition**  
*Split-Brain, Hard Real-Time, Safety-Critical*

---

## 1️⃣ Robot Specifications (Corrected)

| Parameter | Value / Design |
|---------|----------------|
| **Hardware** | Teensy 4.1 (Motion) + ESP32-C3 (Wi-Fi Bridge) + Discrete Drivers |
| **Firmware Architecture** | PlatformIO Split Environment: `env:motion_core` (Teensy) + `env:comms_bridge` (ESP32) |
| **Brain (Logic)** | Python (PC) running Kinematics, Trajectory Planning & Safety Monitor |
| **Update Rate** | 1 kHz internal loop / 100–500 Hz adaptive telemetry stream |
| **Latency Model** | USB: Host-scheduled (Low Latency) · Wi-Fi: Nondeterministic (Telemetry Only) |
| **Safety System** | Hard Watchdog (Teensy) + Physical E-Stop (Hardware) |
| **Sensors** | Absolute Magnetic Encoders (AS5600) + Driver Fault Flags |

---

## 2️⃣ Mechanical Layout (Verified Stack)

**Note:** The Elbow (Joint 3) is the critical load point.

| Joint | Motor | Transmission | Placement | Notes |
|-----|------|--------------|-----------|------|
| **Base (J1)** | NEMA 23 (3.0 Nm) | 10:1 Planetary | Base Plate | Module 1.5 gears |
| **Shoulder (J2)** | NEMA 23 (3.0 Nm) | 20:1 Compound | Base Plate | Metal hub mandatory |
| **Elbow (J3)** | NEMA 17 | 20:1 + Spring | Upper Arm | Gravity assist spring mandatory for 2 kg payload |
| **Wrist P (J4)** | NEMA 17 | 15:1 Planetary | Forearm | Metal 5:1 planetary on motor |
| **Wrist R (J5)** | NEMA 11 | 5:1 Spur | Wrist Plate | Standardized small motor |
| **Gripper (J6)** | NEMA 11 | Worm Gear | End Effector | Self-locking |

---

## 3️⃣ Electronics & Control (The “Hardened” Stack)

**Changes:** Added level shifters, isolation, and E-Stop.

| Component | Product / Details | Critical Integration Note |
|---------|------------------|---------------------------|
| **Master** | Teensy 4.1 | DIN rail mount. USB power only (isolated from 24 V) |
| **Safety** | Physical E-Stop Button | Wired to NC relay (cuts 24 V) **and** Teensy input |
| **Base Drivers** | 2 × DM556T | Requires high-speed 5 V level shifter (3.3 V too weak) |
| **Arm Drivers** | 4 × TMC2209 | StepStick adapters with capacitor decoupling |
| **Power** | 24 V 15 A PSU | Star grounding point is mandatory |
| **Signal Integrity** | Ferrite Beads | On USB cable and long encoder cables |

---

## 4️⃣ The “Data Science” Pipeline (Corrected Architecture)

This defines **exactly** how the robot moves without jitter.

---

### 🧠 1. Python (The Planner)

**Role:** Trajectory generation & system identification  
**Protocol:** Does **NOT** send “Go to X”

- Streams **time-parameterized motion segments**
- Packet format:
- <SegID=102, J1_Vel=50, J2_Vel=20, Duration=50ms>

- **Safety:** Must send a *Heartbeat* packet every **100 ms**

---

### ⚙️ 2. Teensy 4.1 (The Real-Time Executive)

- **Motion Buffer:** ~10 segments stored in a ring buffer
- **Interpolator:** Generates exact step pulses at **20 kHz+** inside a hardware timer ISR
- **Watchdog (Critical):**
- If buffer empty **OR**
- Heartbeat lost (>200 ms)  
→ **SOFT STOP** (velocity ramps to zero)

---

### 📊 3. Analysis (Telemetry)

- Teensy pushes state:
- [Timestamp, Pos_Enc, Pos_Step, Error]
- ESP32 reads buffer via UART
- UDP broadcast to Python for logging & visualization

---

## 5️⃣ Wiring Guide (The “Noise-Proof” Standard)

**Failure to follow this results in phantom steps and jitter.**

---

### A. Power & Grounding (Star Topology)

**The Star Point:**  
Negative terminal (–) of the 24 V PSU

**Rules:**
- Motor ground and logic ground **meet only at the PSU**
- Never daisy-chain grounds between drivers

---

### B. Signal Wiring

**Encoders (I²C):**
- Shielded twisted pair required (CAT5e/6 works well)
- Add **2.2 kΩ pull-ups** to SDA/SCL near Teensy

**DM556T (Base / Shoulder):**
- Teensy pin → Level shifter input
- Level shifter 5 V output → DM556 `PUL+ / DIR+`

**Cable Management:**
- All moving cables must run in **drag chains**
- Strain relief required at **both ends**

---

## 6️⃣ Build Phases (Rev 5.0)

---

### Phase 1: The “Dry Run” (Electrical Validation)

**Goal:** Prove electronics don’t smoke.

- Wire Teensy, level shifters, and **one** driver
- **Test:** Verify clean 0 V / 5 V square wave from level shifter using oscilloscope or multimeter

---

### Phase 2: The “Heartbeat” (Software Safety)

**Goal:** Verify watchdog behavior.

- Flash Teensy watchdog firmware
- Send motion commands from Python
- Kill Python abruptly

✅ **Success:** Motor signal ramps down and stops  
🚫 **Do not connect motors until this works**

---

### Phase 3: The “Tractor” (Base Assembly)

- Connect J1/J2 (DM556T)
- Jog heavy loads
- Watch for **EMI resets** (Teensy crashes on motor stop)

**Fix if needed:**
- Add ferrite beads
- Re-check star grounding

---

### Phase 4: Full Integration (HIL)

- Connect arm, encoders, and Wi-Fi bridge
- Run **Sweep Test**
- Log encoder vs step position

---

## 💡 Final Verdict

### **Rev 5.0 — “The Hardened Standard”**

- **Safety:** Redundant (Watchdog + Physical E-Stop)
- **Signal:** Level-shifted & shielded
- **Power:** Isolated & star-grounded
- **Software:** Buffered trajectory (no jitter)


