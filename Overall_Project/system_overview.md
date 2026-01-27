# System Overview

## Purpose of This Document

This document provides a **technical, system-level view** of the robotic arm platform: what the system is made of, how the major components interact, and how capability evolves over time.

Unlike the project `README.md`, which explains *why the project exists* and *how it is organized*, this document explains:

* What the **system actually is**
* How data, control, and hardware flow together
* Where phase boundaries sit in the architecture
* Which parts are stable vs. intentionally evolving

This document should remain valid across phases, with updates only when the **architecture itself** changes.

---

## System at a Glance

At its core, the project is a **robotic manipulation platform** consisting of:

* A multi‑DOF robotic arm
* A layered control and planning stack
* A unified data and experiment pipeline
* A phase‑driven capability expansion model

The arm is treated not as a one‑off machine, but as an **instrumented experimental system** where every motion produces data that can be analyzed, optimized, and improved over time.

---

## High‑Level Architecture

The system is organized into four primary layers:

1. **Physical Layer** – Mechanics, actuators, sensors, electronics
2. **Control Layer** – Kinematics, dynamics, low‑level control
3. **Planning & Optimization Layer** – Trajectories, constraints, performance objectives
4. **Data & Learning Layer** – Logging, analysis, optimization, learning

Each layer exposes clear interfaces to the layers above and below it.

```
User / Experiments
        ↓
Planning & Optimization
        ↓
Control & Execution
        ↓
Hardware Abstraction
        ↓
Physical Robotic Arm
        ↑
   Telemetry & Logs
```

---

## Physical Layer

### Responsibilities

* Provide repeatable, safe, and measurable motion
* Expose joint‑level state (position, velocity, effort)
* Support incremental mechanical upgrades

### Key Characteristics

* Initial configuration targets **3 DOF**, expandable later
* Modular joints and link design where possible
* Clear electrical and communication standards
* Safety mechanisms (limits, emergency stop, current limits)

This layer is intentionally conservative: reliability and observability are prioritized over performance.

---

## Control Layer

### Responsibilities

* Hardware abstraction (decouple software from specific motors/sensors)
* Forward and inverse kinematics
* Low‑level joint control (e.g., position / velocity / torque loops)
* Enforcing safety constraints during execution

### Design Intent

* Classical control methods come first
* Models and assumptions are explicit and documented
* Control performance is measurable and logged

This layer forms the **contract** between hardware and higher‑level intelligence.

---

## Planning & Optimization Layer

### Responsibilities

* Generate feasible joint‑space or task‑space trajectories
* Respect kinematic, dynamic, and safety constraints
* Evaluate execution quality using defined metrics

### Evolution Across Phases

* Early phases: deterministic trajectories and open‑loop execution
* Mid phases: closed‑loop correction and optimization
* Later phases: adaptive and learning‑augmented planning

This layer is where performance improvements are most visible and quantifiable.

---

## Data & Learning Layer

### Responsibilities

* Automatic logging of all executions
* Experiment metadata capture
* Offline analysis and visualization
* Optimization and learning pipelines

### Core Principle

> Every motion is an experiment.

No learning or optimization component is allowed to exist without:

* A baseline comparison
* Clear metrics
* Reproducible evaluation

Learning augments the system only after classical baselines are established.

---

## Phase Integration Model

Each phase activates or expands parts of the same underlying system rather than introducing disconnected subsystems.

* **Phase 0**: Architecture, math, simulation, interfaces
* **Phase 1**: Physical arm + safe control + full telemetry
* **Phase 2**: Trajectory execution and optimization
* **Phase 3**: Data‑driven correction and learning

Earlier layers are considered **stable contracts** as phases progress.

---

## Stability vs. Flexibility

### Expected to Remain Stable

* Layered architecture
* Data‑first philosophy
* Phase‑driven development model

### Expected to Evolve

* Mechanical design details
* Control strategies
* Optimization and learning methods

Architectural changes are deliberate and documented when they occur.

---

## Success Criteria for the System

At any point in the project, the system should:

* Execute commanded motion safely
* Log complete, structured data automatically
* Allow performance comparison between approaches
* Support extension without rewriting core components

---

## Relationship to Other Documents

* `README.md` – Vision, motivation, and repository orientation
* `goals.md` – Long‑term success criteria
* `assumptions_and_constraints.md` – Design boundaries
* `risks_and_unknowns.md` – Known technical risks
* Phase `system_overview.md` files – Phase‑specific instantiations of this architecture

---

## Guiding Statement

> **The system is not defined by what it can do today, but by how cleanly it can grow tomorrow.**
