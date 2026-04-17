# 🤖 6-DOF Robotic Arm Platform

## Overview
This project is a high-fidelity engineering initiative to design, build, and govern a safety-critical robotic arm platform.

Unlike typical hobbyist builds, this system treats hardware as an industrial platform. It uses a **"Split-Brain" Architecture** where real-time safety guarantees (Teensy 4.1) are decoupled from high-level trajectory planning (Python/PC), linked by a strict data contract.

The intent is not just to make motors move, but to create a scalable engineering system that enforces **ME/DS parity**—where mechanical limits and data science verification hold equal authority.

---

## High-Level Objectives
- **Provable Safety:** The robot must intuitively halt if trajectory limits, thermal thresholds, or heartbeat signals are violated.
- **Split-Brain Control:** Decouple the "Brain" (Python Strategy) from the "Reflex" (Teensy Real-Time Execution).
- **Hardware-in-the-Loop (HIL):** Validate the "Vertical Stack" via gated Mini-Projects before full assembly.
- **Data-Driven Governance:** Log all motion data to specific schemas; ME cannot increase speed/load unless DS verifies the data proves it is safe.
- **Resume-Grade Artifacts:** Produce reusable libraries, distinct engineering gates, and quantitative performance reports.

---

## Guiding Principles
- **Safety Dominance:** Hardware E-Stops and firmware watchdogs override all software logic.
- **Data Before Motion:** We do not move until we can measure. Every motion is an experiment.
- **ME/DS Parity:** Mechanical feasibility and Data Science truth are equal partners.
- **Fail Fast, Fail Cheap:** Validate critical risks (I²C noise, jitter, heat) in Mini-Projects first.
- **Modularity:** Hardware and software are designed to scale from 1 axis to 6 axes without rewriting core logic.

---

## Project Scope (High Level)

### In Scope
- **6-DOF Mechanics:** NEMA 23 Base, NEMA 17 Arm, printed planetary gearboxes.
- **Split-Brain Firmware:** PlatformIO project with distinct environments for Motion Core (Teensy) and Comms Bridge (ESP32).
- **Telemetry Pipeline:** Real-time logging of position, velocity, and error metrics via Wi-Fi/USB.
- **Teleoperation:** Human-in-the-loop control via PS5 controller for data collection.
- **Safety Architecture:** Power-dominant E-Stop, Watchdogs, and Heartbeat enforcement.

### Out of Scope (for now)
- Full humanoid manipulation
- Real-time mobile autonomy
- Computer Vision (until Phase 5+)

---

## Project Phases
Each phase represents a gated milestone:

- **Phase 0 (Virtual):** Architecture, Python simulation, and data schemas.
- **Mini-Project 1:** Single-Axis control, noise validation (Ferrites/Caps), and steady-state error analysis.
- **Mini-Project 2:** Multi-axis coordination and virtual model validation.
- **Mini-Project 3:** Governance system, safety logic, and "Judgment" implementation.
- **Phase 4 (Heavy Metal):** Physical assembly of the full 6-DOF arm (unlocked only after MP1-3 pass).
- **Phase 5 (Research):** Advanced PID, S-Curve profiling, and closed-loop optimization.

---

## Roles & Collaboration Philosophy
This project uses a **"Tension Model"** for collaboration:

- **Mechanical Engineering (ME):** Owns Feasibility. Responsible for wiring, CAD, firmware, and physical safety. Can stop the project if hardware is at risk.
- **Data Science (DS):** Owns Truth. Responsible for logging, signal analysis, and acceptance testing. Has blocking power if data shows instability.

The goal is shared system ownership through explicit contracts, not task silos.

---

## What Makes This Project Valuable
- Demonstrates Systems Engineering and Cyber-Physical design.
- Shows progression from Theory → HIL Validation → Production Hardware.
- Produces artifacts interviewers can reason about:
  - Architecture Diagrams (Split-Brain)
  - Quantitative Performance Reports
  - Safety Analysis Documents

---

## Current Status
- **Architecture:** Locked  
- **Procurement:** Cart 1 (Mini-Project Kit) defined  
- **Phase:** Mini-Project 1 (Setup)  

Detailed implementation, experiments, and iteration live inside the Mini-Project and Phase folders.

---

## Critical Rules
- **Capacitor Rule:** 100µF per driver  
- **Heartbeat Rule:** 100ms timeout  

These are non-negotiable architectural constraints.
