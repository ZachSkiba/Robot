# 🤖 6-DOF Robotic Arm — Final Master Blueprint (Rev 5.0)

**The "Research" Edition**  
*Split-Brain, Hard Real-Time, Safety-Critical*

---

## 1️⃣ Robot Specifications (Comprehensive)

| Parameter | Value / Design |
|---------|----------------|
| **Hardware** | Teensy 4.1 (Motion) + ESP32-C3 (Wi-Fi Bridge) + Discrete Drivers |
| **Firmware Architecture** | PlatformIO Split Env: `env:motion_core` (Teensy) + `env:comms_bridge` (ESP32) |
| **Brain (Logic)** | Python (PC) running Kinematics, Trajectory Planning & Safety Monitor |
| **Update Rate** | 1 kHz internal loop / 100–500 Hz adaptive telemetry stream |
| **Latency Model** | USB: Host-scheduled (Low Latency) · Wi-Fi: Nondeterministic (Telemetry Only) |
| **Safety System** | Hard Watchdog (Teensy) + Physical E-Stop (Hardware) |
| **Sensors** | 6 × AS5600 encoders installed · 1 active (Elbow) for Phase 1 |
| **Motion Profile** | Trapezoidal (Phase 1 MVP) → S-Curve (Phase 2 Upgrade) |
| **Payload Capacity** | 2.0 kg (requires gravity assist spring on J3) |

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

## 4️⃣ The “Strategic” Software Pipeline

This defines the path from **“Moving” → “Research Grade.”**

---

### 🧠 1. Motion Strategy (Teensy 4.1)

#### Phase 1 (MVP): Trapezoidal Ramps
- **Library:** TeensyStep or AccelStepper  
- **Why:** Simple, mathematically cheap, robust  
- **Guarantee:** Works on Day 1  
- **Behavior:** Linear acceleration, slight jerk at start/stop

#### Phase 2 (Research): S-Curve Profiles
- **Library:** Custom 3rd-order polynomial generator  
- **Why:** Eliminates vibration for data science precision  
- **Behavior:** Ultra-smooth starts/stops  
- **Requirement:** Buffered motion segments from Python

---

### 👁️ 2. Sensor Strategy (Encoders)

**Hardware:** All 6 AS5600 encoders wired using shielded CAT5e/6

#### Phase 1 (MVP): Single-Joint Feedback
- **Active:** Elbow (J3) only  
- **Bus:** I²C enabled for one device  
- **Goal:** Detect stall on heaviest joint without I²C instability

#### Phase 2 (Research): Full-State Feedback
- **Active:** All 6 encoders  
- **Goal:** Real-time PID closure + backlash compensation

---

### 🐍 3. Python Strategy (The Planner)

- **Protocol:** Streams time-parameterized motion segments
- **Packet Format:**
- <SegID=102, J1_Vel=50, J2_Vel=20, Duration=50ms>

- **Safety Heartbeat:**  
Python must send a *Keep Alive* packet every **100 ms**

---

## 5️⃣ Wiring Guide (The “Noise-Proof” Standard)

**Failure to follow this results in phantom steps and jitter.**

---

### A. Power & Grounding (Star Topology)

**Star Point:**  
Negative terminal (–) of the 24 V PSU

**Rules:**
- Motor ground and logic ground meet **only** at the PSU
- Never daisy-chain grounds between drivers

---

### B. Signal Wiring

**Encoders (I²C):**
- Shielded twisted pair required
- Add **2.2 kΩ pull-up resistors** to SDA/SCL near Teensy

**DM556T (Base / Shoulder):**
- Teensy pin → Level shifter input
- Level shifter 5 V output → DM556 `PUL+ / DIR+`

**Cable Management:**
- All moving cables inside **drag chains**
- Strain relief at **both ends**

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

- Flash Teensy with motion watchdog code
- Send motion commands from Python
- Kill Python abruptly

✅ **Success:** Signal ramps down and stops  
🚫 **Do not connect motors until this works**

---

### Phase 3: The “Tractor” (Base Assembly)

- Connect J1/J2 (DM556T)
- Jog heavy loads using trapezoidal profiles
- **Check:** EMI resets (Teensy crashing on motor stop)

---

### Phase 4: Full Integration (HIL)

- Connect arm, elbow encoder, and Wi-Fi bridge
- Run sweep test logging encoder vs step position
- **Verify:** Gravity assist spring supports full 2 kg payload

---

## 💡 Final Verdict

### **Rev 5.0 — “The Hardened Master Plan”**

- **Mechanical:** 2 kg payload ready (spring-assisted elbow)
- **Electrical:** Star-grounded, level-shifted, E-Stop protected
- **Software:** Buffered trajectories, watchdog enforced

