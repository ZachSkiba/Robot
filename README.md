# 6-DOF Robotic Arm Platform

**Status:** Early-stage development — embedded bring-up and subsystem development in progress

A collaborative robotics project focused on designing, simulating, and eventually building a 6-degree-of-freedom robotic arm. Development follows a staged approach: establish the system architecture, validate individual subsystems, design the mechanical system, and progressively integrate hardware and software.

> **Documentation rule:** Capabilities are only described as implemented when supported by code, hardware, or test evidence in the repository. Everything else is explicitly labeled **planned** or **design intent**.

---

## Project Goals

The long-term system will combine:

* Mechanical design and actuator selection
* Embedded control
* Position sensing and feedback
* Robot kinematics and trajectory planning
* Simulation and validation
* Telemetry and data logging
* Hardware/software integration
* Safety and fault handling

The project is intentionally developed incrementally rather than attempting full-system integration immediately.

---

## Current Status

| Area                             | Status                   |
| -------------------------------- | ------------------------ |
| System architecture and planning | ✅ Established            |
| Development environment          | ✅ Operational            |
| Dev Container                    | ✅ Operational            |
| Teensy 4.1 bring-up              | 🔄 In progress           |
| PC → USB → Teensy communication  | 🔄 In progress           |
| Embedded diagnostics and testing | 🔄 In progress           |
| Robotics mini-projects           | 🔲 In progress / planned |
| Mechanical arm design            | 🔲 Not yet started       |
| Motor/driver integration         | 🔲 Not yet started       |
| Encoder integration              | 🔲 Not yet started       |
| Closed-loop joint control        | 🔲 Not yet implemented   |
| Full 6-DOF integration           | 🔲 Future                |

The physical components for the project have been acquired, but the arm has **not yet been mechanically designed, assembled, or connected into a working robotic system**.

---

## Current Development

### Embedded Platform

Current development is focused on the **Teensy 4.1** as the embedded platform.

```text
PC
 │
 │ USB
 ▼
Teensy 4.1
```

Current work includes:

* USB serial communication
* Diagnostic firmware
* Embedded performance testing
* Timing and computation benchmarks
* Hardware/software development workflow

Motor drivers, motors, encoders, and other robot hardware will be integrated in later stages.

### Mini-Projects

Small subsystem experiments are being used to validate individual capabilities before integrating the complete arm.

These exercises will cover areas such as:

* Embedded communication
* Motor and actuator control
* Sensor interfaces
* Data collection
* Control concepts
* Hardware/software interfaces

### Mechanical Design

Mechanical development has not yet begun. The next major stage will establish:

* Joint architecture
* Workspace and payload requirements
* Actuator and transmission selection
* Link geometry
* Bearings and structural interfaces
* CAD and manufacturing documentation

---

## System Architecture

**Design intent — not yet implemented end-to-end.**

```text
        Operator / Host Computer
                  │
                  ▼
       Motion / Planning Software
                  │
                  ▼
          Embedded Controller
             Teensy 4.1
                  │
                  ▼
         Motor Driver / Actuator
                  │
                  ▼
              Robot Joint
                  │
                  ▼
          Position Feedback
                  │
                  └──────► Telemetry / Logging
```

The final software architecture may incorporate ROS 2, simulation, motion planning, and additional controllers as the project progresses.

---

## Safety

Safety is being treated as a system-level requirement from the beginning.

**Planned protections include:**

* Joint position limits
* Velocity and acceleration limits
* Command validation
* Communication watchdogs
* Hardware emergency-stop functionality
* Motor/driver fault handling
* Independent overload protection where applicable

These are **design requirements**, not claims of currently implemented safety functionality.

---

## Development Phases

| Phase     | Focus                                            | Status            |
| --------- | ------------------------------------------------ | ----------------- |
| Phase 00  | Architecture, environment, and embedded bring-up | 🔄 Current        |
| Phase 01  | Subsystem mini-projects and validation           | 🔄 Current / next |
| Phase 02  | Mechanical arm design                            | 🔲 Planned        |
| Phase 03  | Single-joint hardware integration                | 🔲 Planned        |
| Phase 04  | Multi-joint integration                          | 🔲 Planned        |
| Phase 05  | Kinematics and trajectory control                | 🔲 Planned        |
| Phase 06  | Full 6-DOF integration and validation            | 🔲 Planned        |
| Phase 07+ | Advanced robotics capabilities                   | 🔲 Future         |

Later phases will be refined as earlier stages establish validated requirements and test results.

---

## Collaboration

This is a collaborative project between **Nicholas Skiba** and **Zachary Skiba**.

Current areas of contribution include:

**Nicholas Skiba**

* Embedded/Teensy development
* Hardware bring-up and testing
* Subsystem development
* Mechanical design and physical integration

**Zachary Skiba**

* Simulation development
* Data science and analysis
* Computational development

The project is maintained collaboratively, with individual contributions tracked through the repository history and project documentation.

---

## Repository Structure

```text
Robot/
├── .devcontainer/
├── Overall-Project/
├── Phase00-Plan/
├── Phase01-Arm/
├── Phase02-Trajectory/
├── Phase03-Optimize/
├── Phase04-Learning/
├── Phase05-Vision/
├── Phase06-Autonomy/
├── src/
├── docs/
├── archive/
└── README.md
```

The repository contains active development, engineering documentation, experiments, and archived work.

---

## Contact

**Nicholas Skiba**
Mechanical Engineering · Illinois Institute of Technology
[LinkedIn](https://www.linkedin.com/in/nicholas-skiba-477b6b287) · [GitHub](https://github.com/NickSki17)

**Zachary Skiba**
[LinkedIn] · [GitHub / Portfolio]

---
