# Task Split

## Purpose of This Document

This document defines how work is logically decomposed across the project and clarifies responsibilities between contributors.

Unlike the system-level decomposition, this version explicitly maps tasks to the primary team members: you (data science) and your brother (mechanical engineering).

---

## 1. Mechanical System Tasks (Handled by MechE)

* Arm kinematic structure design
* Joint and link geometry
* Material selection and structural integrity
* Assembly, alignment, and repeatability
* Validate mechanical tolerances
* Document assembly procedures

**Deliverables:** CAD models, mechanical drawings, payload and range-of-motion specs

---

## 2. Electrical & Embedded Systems Tasks (Shared / Primarily MechE)

* Motor drivers and power distribution
* Sensor integration
* Embedded control firmware
* Safety mechanisms

**Deliverables:** Schematics, wiring diagrams, firmware code, bring-up procedures

---

## 3. Control & Modeling Tasks (Shared / Primarily MechE)

* Kinematic and dynamic modeling
* Low-level and mid-level control
* Simulation models

**Deliverables:** Mathematical derivations, control code, performance plots

---

## 4. Planning & Optimization Tasks (Shared / You Lead on Data & Analysis)

* Trajectory generation and optimization
* Constraint handling
* Performance evaluation

**Deliverables:** Planning algorithms, evaluation metrics, optimization results

---

## 5. Data, Analysis & Learning Tasks (Handled by Data Science - You)

* Data logging infrastructure
* Experiment management
* Analysis, optimization, and learning

**Deliverables:** Datasets, analysis scripts, learning models, reports

---

## 6. Systems Integration Tasks (Shared)

* Interface definition between subsystems
* End-to-end testing
* Regression prevention

**Deliverables:** Interface documentation, integration tests, system validation reports

---

## 7. Documentation & Project Management Tasks (Shared)

* Maintain clarity and continuity
* Capture decisions and tradeoffs
* Track risks and assumptions
* Keep documentation synchronized with reality

**Deliverables:** Updated documentation, design decision records, phase summaries

---

## Collaboration Model

* Tasks overlap intentionally; all major decisions are discussed jointly
* MechE focuses on hardware and low-level control
* Data Science focuses on logging, analysis, learning, and evaluation
* Integration and documentation remain collaborative

---

## Guiding Principle

> **If a task touches more than one layer, it must be discussed jointly. Mechanical and Data Science responsibilities are clearly delineated, but collaboration is continuous.**
