# 🎯 Overall Project Goals — Rev 5.2 (Research Edition)

---

## 1. Project Vision

Design, build, and validate a **high-fidelity, safety-critical 6-DOF robotic manipulator** that bridges the gap between hobbyist hardware and research-grade control.

The project prioritizes **data integrity**, **hard real-time safety**, and **systems engineering**, ensuring the final platform is capable of capturing precise kinematic data for advanced analysis and machine learning training.

### Long-Term Vision

The manipulator will:

- **Exhibit Industrial Safety**  
  Fail safely under all conditions (power loss, logic crash, user error).

- **Generate Research-Grade Data**  
  Provide clean, synchronized telemetry for system identification and digital twin validation.

- **Demonstrate a “Split-Brain” Architecture**  
  Prove the viability of decoupling high-level Python logic from low-level silicon safety.

- **Serve as a Portfolio Masterpiece**  
  Act as verifiable proof of full-stack mechatronic engineering capability.

---

## 2. Core Objectives

### 2.1 Enforce *Safety by Design*

- Implement a **power-dominant E-Stop** system that does *not* rely on software state.
- Embed autonomous safety invariants (velocity limits, workspace bounds) directly into firmware.
- Ensure the system is **fail-secure**, not merely fail-safe.

---

### 2.2 Phase-Driven Validation (The V-Model)

- Break development into explicit, verifiable phases:  
  **Dry Run → Heartbeat → Tractor → HIL**
- Require **binary exit criteria** for every phase  
  (e.g., *“Does the watchdog stop the motor within 50 ms?”*).
- Prevent **hardware debt** by refusing to advance phases until the current phase is robust.

---

### 2.3 The “ME / DS Contract”

- **Mechanical Engineering (ME)**  
  Deliver a predictable, rigid physical plant with zero-latency safety.

- **Data Science (DS)**  
  Deliver optimized trajectories and adaptive control without risking physical hardware.

- **The Interface**  
  A strict, versioned packet protocol separating these two domains.

---

### 2.4 Real-World Robustness

- Prioritize **EMI immunity** (differential signaling, star grounding) over convenience.
- Design for **thermal stability** under continuous load (2.0 kg payload).
- Treat **noise** as a bug to be eliminated, not blindly filtered away.

---

## 3. Technical Goals

### 3.1 Software Architecture (Split-Brain)

- **Host (Python)**  
  Non-deterministic planner responsible for *what* the robot does.

- **Firmware (Teensy)**  
  Hard real-time executor responsible for *how* it happens safely.

- **Telemetry**  
  100% of motion data (Target vs. Actual) logged for post-mortem analysis.

---

### 3.2 Hardware Architecture

- **Star Topology**  
  Centralized power and ground distribution to eliminate ground loops.

- **Sensor Fusion**  
  Transition from single-ended feedback (Phase 1) to differential signaling (Phase 2).

- **Payload Definition**  
  Mechanical structure explicitly sized for a **2.0 kg payload** with a **1.5× safety factor**.

---

### 3.3 Data & Intelligence

- Treat the robot as a **Physical Data Generator**.
- Enable **Sim-to-Real** workflows:  
  Physical robot must match Python simulation within **< 5% error**.
- Support future **Black-Box Controllers** (RL / AI) by sandboxing them behind firmware safety layers.

---

## 4. Documentation & Knowledge Capture

- **Resume-Driven Documentation**  
  Every major subsystem (Safety, Kinematics, Electrical) has a standalone technical write-up.

- **Incident Logs**  
  Document every *crash*, *burn*, or *magic smoke* event to trace root causes.

- **Architecture Decision Records (ADRs)**  
  Explicitly justify key choices (e.g., Teensy vs. ESP32, Differential I²C).

---

## 5. Validation & Testing Goals

- **Unit Tests**  
  Verify packet parsing and buffer logic without motors attached.

- **Integration Tests**  
  *The Shake Test* — validate connectors and EMI shielding under maximum vibration.

- **System Identification**  
  Measure and record real friction, gravity, and inertia to update the software model.

---

## 6. Scalability Goals

- **Toolhead-Agnostic Design**  
  J6 must support swappable end-effectors (Gripper, Pen, Camera, Laser) without rewiring.

- **Bus Expandability**  
  Communication bus must allow additional sensors (IMUs, load cells) without controller redesign.

---

## 7. Learning & Iteration Philosophy

- **Physics Wins**  
  If the math says the motor is too weak, buy a bigger motor.  
  Do not code around physics.

- **Data over Intuition**  
  PID tuning is validated with step-response plots, not gut feelings.

- **Refactoring Is Progress**  
  Rewriting the planner (Trapezoidal → S-Curve) is a success, not a failure.

---

## 8. Long-Term Outcomes

Upon completion, the system should:

- Execute autonomous pick-and-place tasks with **< 1 mm repeatability**.
- Safely detect and react to **human intrusion or collision events**.
- Serve as a proven testbed for advanced control algorithms  
  (MPC, Impedance Control).

---

## 9. Non-Goals (Explicitly Out of Scope)

- **Toy Servos**  
  No PWM hobby servos — only steppers with defined steps.

- **Blind Motion**  
  No motion without enforced safety limits.

- **Wireless Control Loops**  
  No real-time PID over Wi-Fi (telemetry only).

- **“Magic” Code**  
  No libraries that have not been read and understood.

---

## 10. Guiding Principle

> **“The robot protects itself; the human protects the mission.”**  
>  
> Firmware ensures the hardware never dies.  
> Software ensures the task gets done.

---