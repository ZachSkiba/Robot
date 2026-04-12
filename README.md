# 6-DOF Robotic Arm Platform

**Status:** Early-stage development — planning complete, simulation implementation beginning

A staged robotics project for designing, simulating, and building a 6-degree-of-freedom robotic arm. The focus is safety-first design, structured telemetry, and disciplined systems engineering — demonstrated through process and documentation now, and through running code as each phase completes.

> **Documentation rule:** Anything not yet implemented or evidenced in this repository is explicitly labeled *design intent* or *planned*. No capability is claimed without qualification until it exists.

---

## Tech Stack

| Layer | Tools |
|---|---|
| Motion planning | ROS 2 Humble · MoveIt 2 |
| Simulation | Gazebo Classic |
| Embedded control | Planned: STM32-class MCU (selection Phase 01) |
| Dev environment | Docker · VS Code Dev Containers |
| Build system | colcon · CMake |
| Language | Python · C++ (ROS 2 nodes) |

---

## Why This Project

Most hobby robot arms are built bottom-up: buy motors, wire things, hope it works. This project inverts that. Design starts with constraints, safety margins, and a validation plan — then works toward hardware.

Engineering priorities, in order:

1. **Safety** — defined at the architecture level before any motion command is written
2. **Observability** — every joint state and command logged with timestamps
3. **Staged validation** — simulation before hardware; hardware-in-the-loop before deployment
4. **Reproducibility** — fully containerized dev environment; anyone can build it

---

## Current Status

| Area | Status |
|---|---|
| Repository structure and planning docs | ✅ Present |
| ROS 2 package scaffold (`robot_control`) | ✅ Builds in container |
| Dev container environment | ✅ Operational |
| Safety architecture | 📄 Designed — not yet implemented |
| Simulation (Gazebo + URDF) | 🔲 Planned |
| Active ROS 2 control nodes | 🔲 Not yet implemented |
| Hardware integration | 🔲 Planned (Phase 01+) |

**What is not in this repository yet (explicit):**
- A checked-in URDF robot model
- Launch files for simulation
- Implemented ROS 2 control or telemetry nodes
- Hardware of any kind

---

## Phase 00 Exit Criteria

Phase 00 closes when all of the following are demonstrated — not just planned:

- [ ] ROS 2 workspace builds reproducibly in the dev container
- [ ] Gazebo launches with a URDF robot model loaded
- [ ] `robot_control` node publishes joint states to a ROS 2 topic
- [ ] Joint state output confirmed via `ros2 topic echo`
- [ ] MoveIt planning scene loads without error
- [ ] Each item above documented with terminal output or screenshot

Phase 01 does not begin until every box is checked.

---

## Safety Architecture

> **Status:** Designed and documented — not yet implemented in code.

The intended safety model is layered. No single layer is trusted alone.

**Enforcement layers (planned, in execution order):**

1. **Planning layer (MoveIt):** collision avoidance, IK validity, path feasibility
2. **Control node (`robot_control`):** joint limit enforcement, velocity/acceleration clamping, command validation before dispatch
3. **Watchdog node:** monitors command stream freshness; triggers safe stop on timeout or interruption

**Safety envelope variables:**
- Joint position limits — defined in URDF, enforced at the controller level
- Velocity and acceleration limits — clamped before any command is issued
- Workspace constraints — MoveIt planning scene boundaries
- Command timeout — stale or interrupted commands trigger halt, not continuation

**Failure behavior (design intent):**
- All faults default to **stop and hold** — not uncontrolled release
- No layer assumes a higher layer is functioning correctly
- Emergency stop is a hard cutoff, not a software request

**Phase 01+ (hardware additions):**
- Interrupt-level hardware emergency stop
- Per-joint current sensing as an independent overload signal

---

## System Architecture

> **Status:** Design intent — not yet implemented end-to-end.

```
┌─────────────────────────────────────────────────┐
│                  Operator Input                  │
└───────────────────────┬─────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────┐
│             MoveIt 2 (Planning Layer)            │
│  · Collision avoidance                          │
│  · IK solving                                   │
│  · Path feasibility check                       │
└───────────────────────┬─────────────────────────┘
                        │ validated trajectory
                        ▼
┌─────────────────────────────────────────────────┐
│         robot_control Node (Control Layer)       │
│  · Joint limit enforcement                      │
│  · Velocity / acceleration clamping             │
│  · Command validation before dispatch           │
└──────────┬────────────────────────┬─────────────┘
           │                        │
           ▼                        ▼
┌──────────────────┐     ┌──────────────────────┐
│  Watchdog Node   │     │  Simulated Joints     │
│  · Command       │     │  (Gazebo · Phase 00)  │
│    freshness     │     │                       │
│  · Safe stop     │     │  Physical Joints      │
│    on timeout    │     │  (Phase 01+)          │
└──────────────────┘     └──────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────┐
│              Telemetry / Logging             │
│  · Joint states (position, velocity, effort) │
│  · Command stream with timestamps            │
│  · Fault and watchdog events                 │
└──────────────────────────────────────────────┘
```

*Hardware path (Phase 01+) replaces simulated joints. Architecture otherwise unchanged.*

---

## Design Constraints

| Constraint | Value |
|---|---|
| Degrees of freedom | 6 (serial manipulator) |
| Target payload | TBD — primary driver for joint and actuator selection |
| Control loop target | ≥ 50 Hz |
| Safety posture | Fail-stop (halt on any unresolved fault) |
| Gate rule | No phase advances before prior phase exit criteria are met |

---

## Project Phases

| Phase | Focus | Status |
|---|---|---|
| Phase 00 | Simulation and architecture | 🟡 In progress |
| Phase 01 | Physical arm build and basic control | 🔲 Planned |
| Phase 02 | Trajectory planning | 🔲 Planned |
| Phase 03 | Telemetry and logging | 🔲 Planned |
| Phase 04+ | Advanced capabilities | 🔲 Scoped as prior phases close |

Phases beyond 03 are not fully defined yet. That is intentional — scope is defined when it is earned, not pre-planned into imaginary detail.

---

## Repository Structure

```
Robot/
├── .devcontainer/          # VS Code + Docker dev environment
├── src/
│   └── robot_control/      # ROS 2 package: nodes, launch files, configs
├── docs/
│   ├── overall_project/    # System vision, constraints, risk log
│   ├── phase_00/           # Simulation planning and architecture docs
│   ├── phase_01/           # Physical build planning
│   └── phase_02+/          # Later phase roadmap docs
└── README.md
```

---

## Getting Started

### Option 1: VS Code Dev Container (Recommended)

Requirements: Docker, VS Code, Dev Containers extension.

```bash
git clone <repo-url>
cd Robot
# Open in VS Code → "Reopen in Container"
# Container installs all ROS 2 Humble dependencies automatically
```

Inside the container:

```bash
colcon build
source install/setup.bash
```

### Option 2: Existing ROS 2 Humble Environment

```bash
source /opt/ros/humble/setup.bash
cd Robot
colcon build
source install/setup.bash
```

---

## Recommended Reading Order

1. [`docs/overall_project/README.md`](docs/overall_project/README.md) — scope, constraints, safety philosophy
2. [`docs/overall_project/system_overview.md`](docs/overall_project/system_overview.md) — architecture and component relationships
3. [`docs/phase_00/README.md`](docs/phase_00/README.md) — current simulation work and validation plan
4. [`docs/phase_01/overview.md`](docs/phase_01/overview.md) — physical build planning

---

## Professional Context

This repository is developed with the discipline expected in a production robotics environment:

- Requirements and risk documentation written before implementation begins
- Containerized, reproducible development workflow
- Explicit exit criteria per phase — no phase advances without demonstrated evidence
- Commit history reflecting deliberate, traceable progress
- Honest separation of what is designed, what is planned, and what is running

The goal is not to show a robot that moves. It is to demonstrate the ability to operate inside a real engineering process — and to close that gap into working code phase by phase.

---

## Contact

*[Your name · email · LinkedIn · portfolio]*