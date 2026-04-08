# 🔹 6-DOF Robotic Arm — Project Overview

This project is a **research-grade, 6-DOF robotic arm** designed for safe, repeatable motion experiments, targeting high repeatability and precision. It combines modular mechanical design, robust electronics, and a split-brain control architecture, supporting both autonomous and teleoperated operation. The platform serves as a testbed for trajectory optimization, control experiments, and data-driven analysis.

## Current Maturity (Detailed)

* **Architecture & Planning:** Mature — system architecture (Rev 5.2), task split/governance, risks/constraints, and phase roadmaps fully documented.
* **Simulation:** Moderate — mini-project simulation exists (single-motor + 2-link/3D dynamics) with multiple logged datasets (e.g., March 6, 2026) showing repeatable virtual test runs.
* **Procurement:** Moderate-to-high — BOMs and component selections developed; staged purchasing plans in place.
* **Software Environment:** High — ROS2/Gazebo/devcontainer workflows documented and scaffolded; application-level robot packages mostly skeletons/TODOs.
* **Mechanical:** Early — no CAD assets checked in, and no finalized 3-DOF or 6-DOF mechanical model yet.

## Team & Task Split

* **Nick (MechE):** Mechanical design, CAD, motor mounts and structural components, wiring/build quality, embedded safety, and hardware validation.
* **Nick+Zach (DS):** Kinematics, trajectory planning, data logging, performance analysis, dashboards, and optimization experiments.
* **Shared Responsibility:** Hardware-software integration, phase-gate decisions, troubleshooting oscillations or noise, and ensuring packet/command contract compliance.
* **Governance:** Safety concerns from MechE can halt runs; bad data quality from DS can block progression.

## Mechanical & Electronics Overview

* Modular 6-DOF arm, capable of **~2 kg payload**.
* **Motors:** J1/J2 — NEMA23, J3/J4 — NEMA17, J5/J6 — NEMA11.
* **Sensors:** Encoders on all joints; Phase 1 active feedback on elbow (J3) for load/stall detection.
* **Electronics:** Teensy 4.1 handles real-time step generation and safety limits; ESP32-C3 provides Wi-Fi telemetry; Python on PC performs kinematics and trajectory planning.
* **Safety Features:** Hardware E-stop, watchdog on Teensy, motion limit enforcement, and autonomous deceleration in case of failure.

## Software & Motion Control

* **Phase 1 (MVP):** Trapezoidal motion profiles with safe, repeatable joint motion.
* **Phase 2 (Research):** S-curve profiles, full 6-DOF feedback, PID control, and calibration.
* **Phase 3+:** Data logging, trajectory optimization, learning from error, and optional teleoperation with PS5 controller.

> **Key Principle:** Python may request motion; Teensy enforces all safety and autonomy rules.

---

## Phase Summary (High-Level)

| Phase | Focus | Outcome |
| :--- | :--- | :--- |
| 0 | Plan/Simulation | Define kinematics, logging, and assumptions |
| 1 | Arm Build | 3-DOF arm, homing, limits, repeatable motion |
| 2 | Trajectory | Measure and optimize trajectory quality |
| 3 | Optimize/Learn | Reduce error, compensate backlash and bias |
| 4 | Learning/RL | Optional advanced learning experiments |
| 5 | Vision | Add camera pipeline and vision-guided manipulation |
| 6 | Autonomy | Extend to higher-level task execution |
| 7 | Research Optimization | Hybrid control + learning + robustness testing |
| 8 | Deployment | Reliability, failure handling, and long-run stability |
| 9 | Specialization | Focus track (controls, ML, perception) |
| 10 | Mastery | Freeze gold version; portfolio-ready outputs |

## Project Goals

* Build a **safe, modular robotic platform** suitable for experimental and research tasks.
* Enable **repeatable, data-driven motion experiments** with high fidelity.
* Develop a **team workflow** where mechanical and data-driven responsibilities are clearly split, supporting collaboration on both hardware and software integration.
* Establish a foundation for **future extensions:** learning-based control, vision guidance, and autonomy.