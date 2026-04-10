# 🔹 6-DOF Robotic Arm — 2-Credit Project Summary (One Pager)

### Project Title
**Incremental CAD Design and Simulation of a 6-DOF Robotic Arm**

### Objective
Develop a **parametric CAD model of a 6-DOF robotic arm**, complete detailed design of **J1 (base)** as the critical subsystem, and **validate** kinematic feasibility in URDF/Gazebo. Optional **3D printing** will be used for structural and transmission prototypes. Design target: **2 kg payload, ~400 mm working radius.**

### Background
* Software environment is fully prepared (ROS2, MoveIt, Gazebo, devcontainers, scripts).
* Hardware, motors, and transmission ideas are defined; procurement and BOM planning mostly complete.
* No CAD assets exist yet; 3-DOF skeleton is not modeled.
* **Goal:** produce a structured CAD model first, focusing on one link/joint at a time to reduce workload while keeping parametric flexibility.
* Workload scoped for 2 credits, CAD-first, belt-only transmission, no springs.

### Proposed Work

#### 1. Parametric CAD Skeleton
* Build full 6-DOF skeleton, starting with **J1–J3 (base/shoulder/elbow)**.
* Define joint axes, link envelopes, motor mounts, and bearing placeholders.
* Keep all link lengths, offsets, and joint limits parametric for future iteration.
* Non-priority joints (J2–J6) initially modeled to conceptual/preliminary detail.

#### 2. Detailed Subsystem Design
* **J1 (Base):** fully detailed for fabrication and assembly.
* Motor placement, belt sizing, wide-spaced bearings, thick ribbed plates for torsional stiffness.
* Other joints: envelopes/parametric placeholders; focus detailed design on one critical subsystem first.

#### 3. 3D Printing & Prototyping
* Print structural frames, pulley mounts, and belt components for validation.
* Ensure fit, assembly, and basic motion clearance; prototype loads lighter than 2 kg.

#### 4. Simulation
* Export CAD to URDF/Gazebo, starting with J1–J3.
* **Validate:**
    * Joint motion and workspace (~400 mm reach)
    * Axis directions, joint limits, self-collision detection
    * Placeholder J4–J6 for eventual full 6-DOF simulation.

### Expected Deliverables
* Parametric CAD model of full 6-DOF arm.
* Detailed CAD of J1 (base) subsystem.
* Conceptual/preliminary CAD for non-priority joints (J2–J6).
* URDF/Gazebo model demonstrating J1–J3 motion.
* Short report documenting design rationale, iteration decisions, and simulation results.

### Key Design Considerations
* Belt-only transmission, no springs.
* 3D-printed components for structure, mounts, and pulleys.
* Modular, parametric design for incremental build and iteration.
* Maintain 2 kg payload and ~400 mm reach for kinematic feasibility.
* Prioritize mechanical clarity over full system assembly.