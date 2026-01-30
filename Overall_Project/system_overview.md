# 🏗 System Overview (Rev 5.2)

## Purpose of This Document
This document provides a technical, system-level view of the 6-DOF Robotic Arm Platform (Rev 5.2).

Unlike the README.md, which explains the project's organization and vision, this document explains:

- **The "Split-Brain" Architecture:** How non-real-time logic (Python) safely controls real-time hardware (Teensy).  
- **The Data Lifecycle:** How motion commands flow down and telemetry flows up.  
- **The Safety Layers:** Where authority resides when things go wrong.  

This document defines the invariant architecture that remains stable across all build phases.

---

## System at a Glance
The system is a hybrid cyber-physical platform designed to separate high-level intelligence from low-level safety.

- **The Brain (PC):** Infinite compute, non-real-time, runs complex Python/ML.  
- **The Reflex (Embedded):** Limited compute, hard real-time, guarantees safety.  
- **The Contract:** A strict communication protocol ensures the "Brain" cannot force the "Reflex" to violate physical laws.  

The arm is treated not as a peripheral, but as a semi-autonomous agent that accepts trajectory requests but retains the right to refuse them based on self-preservation logic.

---

## High-Level Architecture: "The Split-Brain"
The architecture is divided into four distinct domains of authority:

### 1. Strategy Layer (The "Brain")
- **Hardware:** PC / Laptop  
- **Software:** Python (Custom Planner + Dashboard)  
- **Role:**  
  - Generates trajectories (Inverse Kinematics, Path Planning)  
  - Visualizes telemetry in real-time  
  - **Data Science Authority:** Decides if a motion is valid based on historical data

### 2. Bridge Layer (The "Nerve")
- **Hardware:** ESP32-C3  
- **Software:** PlatformIO (env: comms_bridge)  
- **Role:**  
  - Acts as a transparent telemetry bridge  
  - Decouples logging traffic (Wi-Fi) from control traffic (USB)  
  - Ensures data logging never blocks the motion loop

### 3. Reflex Layer (The "Muscle")
- **Hardware:** Teensy 4.1 (600 MHz)  
- **Software:** PlatformIO (env: motion_core)  
- **Role:**  
  - Hard Real-Time Execution: Generates step pulses via hardware timers  
  - Safety Enforcement: Checks limits, thermals, and "Keep Alive" heartbeats 1,000 times per second  
  - Autonomy: Once a motion segment is buffered, the Teensy executes it independently of the PC

### 4. Power Layer (The "Limit")
- **Hardware:** 24V PSU, E-Stop, Drivers (DM556T/TMC2209), Capacitor Bank  
- **Role:**  
  - The physical baseline of truth  
  - **Power-Dominant Safety:** The E-Stop cuts power physically, overriding all software layers

---

## Data Flow Pipeline
The system uses a **Dual-Path data model** to minimize latency while maximizing observability.

### Path A: Control (Downlink)
- **Route:** Python → USB → Teensy Ring Buffer  
- **Protocol:** Custom binary packet `<CommandID, Payload, Checksum>`  
- **Constraint:** Must be deterministic. No heavy data payloads

### Path B: Telemetry (Uplink)
- **Route:** Teensy → UART → ESP32 → Wi-Fi → Python Dashboard  
- **Content:** High-frequency state data (Position, Velocity, Error, Current)  
- **Constraint:** Best-effort delivery. Dropped packets are acceptable; blocking motion is not

---

## Safety Hierarchy (The "Veto" System)
Safety is enforced hierarchically. A lower layer always overrides a higher layer:

1. **Physical Layer (Highest Authority)**  
   - **Trigger:** E-Stop Button pressed  
   - **Action:** 24V Power cut to drivers; motor torque vanishes instantly  
   - **Software Override:** Impossible

2. **Reflex Layer (Firmware)**  
   - **Trigger:** Watchdog timer expiry (Python crash), Joint Limit breach, or Tracking Error > Threshold  
   - **Action:** Ramps down velocity to 0, disables driver EN pins

3. **Strategy Layer (Software)**  
   - **Trigger:** Inverse Kinematics solver fails, or collision predicted  
   - **Action:** Refuses to send the command packet

---

## Component Details (Rev 5.2 Specifics)

### 1. Motion Core (Teensy 4.1)
- **Step Generation:** Uses hardware timer interrupts, not delay()  
- **Buffering:** Maintains a circular buffer of ~500ms of motion to absorb Windows/Python scheduler jitter  
- **Sensors:** Reads 6x AS5600 Encoders via I²C (Polled via DMA or non-blocking ISR)

### 2. Comms Bridge (ESP32-C3)
- **Isolation:** Physically separate chip to ensure Wi-Fi stack crashes do not freeze the robot  
- **Power:** Powered by independent LDO to prevent RF noise from injecting into the Teensy's ADC rails

### 3. Drivers & Actuators
- **Base (J1-J2):** NEMA 23 + DM556T (Industrial, external)  
- **Arm (J3-J6):** NEMA 17/11 + TMC2209 (Silent, UART-configurable)  
- **Protection:** Every driver input has a 100µF Capacitor to absorb regenerative braking voltage spikes

---

## Evolution Model: The "Mini-Project" Pipeline
The system architecture is validated incrementally through Hardware-in-the-Loop (HIL) stages:

- **Mini-Project 1: Single Axis**  
  Validates the Control Path (USB → Teensy → Driver)

- **Mini-Project 2: Multi-Axis**  
  Validates the Synchronization (Kinematics match Reality)

- **Mini-Project 3: Teleop**  
  Validates the Safety Hierarchy (Human input vs. Limits)

- **Full Build:**  
  Validates the Mechanical Structure (Torque/Gravity)

---

## Guiding Principle
> "The PC requests. The Teensy decides. The Hardware enforces."

This separation ensures that a bug in the Python script or a Windows update restart cannot cause physical damage to the robot or the operator.