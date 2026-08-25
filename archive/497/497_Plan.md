# MMAE 497 — 16-Week Robotic Arm Work Plan

## Semester Objective

Use the 16-week, 2-credit MMAE 497 course to develop the **mechanical and CAD foundation of a 6-DOF robotic arm**.

The primary objective is to create a **parametric 6-DOF Inventor assembly**, complete a **detailed engineering design of J1 (base)**, develop **preliminary CAD for J2–J6**, and perform enough mechanical and kinematic validation to establish that the architecture is feasible.

### Design Targets

- 6 degrees of freedom
- 2 kg end-effector payload
- ~400 mm working radius
- Actual purchased hardware used where practical
- Parametric CAD suitable for future iteration
- Belt-based transmission architecture

The larger robot project also includes electronics, embedded control, ROS2, controls, data analysis, and future research. Those remain part of the overall project, but **MMAE 497 focuses primarily on the mechanical/CAD work**.

---

# Semester Deliverables

By the end of the semester, the goal is to have:

### Full 6-DOF Mechanical Architecture

- J1–J6
- Joint axes
- Link lengths and offsets
- Joint limits
- Motor envelopes
- Encoder envelopes
- Bearing locations
- Transmission envelopes
- Major structural interfaces
- Parametric relationships

### Detailed J1 Assembly

- Actual motor
- Encoder
- Bearings
- Shaft
- Coupler
- Belt
- Pulleys
- Motor mount
- Structural plates
- Ribs
- Fasteners
- J2 interface
- Cable-routing provisions
- Manufacturing/3D-print considerations

### Preliminary J2–J6 CAD

- Mechanical architecture
- Motor/encoder placement
- Bearings
- Shafts
- Transmission concepts
- Structural links/housings
- Joint interfaces
- Joint limits

J2–J6 do **not** need to be fully fabrication-ready.

### Engineering Validation

- 2 kg payload at ~400 mm
- Torque requirements
- Motor capability
- Transmission ratio
- Belt forces
- Shaft loading
- Bearing loading
- Basic structural considerations
- Mass properties where useful

### Simulation

- CAD → URDF
- Primarily J1–J3
- Correct joint axes
- Correct coordinate frames
- Joint limits
- Reach/workspace
- Basic collision/interference
- Basic Gazebo motion

### Documentation

- Requirements
- Design decisions
- Design iterations
- Engineering calculations
- Final CAD
- Simulation results
- Remaining limitations
- Future work

---

# 16-Week Schedule

## Phase 1 — Requirements and Mechanical Architecture

### Week 1 — Requirements, Hardware, and Inventor Setup

**Goal:** Set up the project correctly before spending time on detailed geometry.

#### Requirements

- Review existing robot requirements.
- Confirm:
  - 6 DOF
  - 2 kg end-effector payload
  - ~400 mm working radius
  - Motor assignments
  - Encoder assignments
  - Transmission philosophy
- Identify which requirements are fixed versus adjustable.

#### Hardware

Gather actual dimensions of hardware already purchased:

- Motors
- Motor shafts
- Mounting-hole patterns
- Encoders
- Bearings
- Couplers
- Other hardware that affects mechanical interfaces

#### Inventor

- Create project/folder structure.
- Establish naming conventions.
- Establish J1–J6 naming.
- Establish coordinate-system conventions.
- Create a master parameter table.
- Set up the main assembly.

#### CAD Work

Create a rough:

`J1 → J2 → J3 → J4 → J5 → J6`

assembly.

The objective is establishing the overall design framework, not detailed geometry.

#### Output

**Initial parametric 6-DOF skeleton**

---

## Week 2 — Kinematic Architecture

**Goal:** Make sure the proposed arm geometry works before designing detailed mechanical components.

### CAD

Define:

- Joint axes
- Link lengths
- Link offsets
- Joint origins
- Approximate joint limits
- End-effector location
- Motor envelopes
- Bearing envelopes

### Engineering Checks

Check:

- ~400 mm working radius
- Basic workspace
- Reach in important configurations
- Obvious self-intersections
- Impossible joint configurations
- Hardware packaging
- General arm proportions

### Output

**Parametric 6-DOF kinematic skeleton v1**

### Gate 1

Before beginning detailed J1 work:

> Can the proposed geometry achieve the required reach while accommodating the selected motors, bearings, transmissions, and joint limits?

If not, fix the architecture now.

---

# Phase 2 — Detailed J1 Engineering Design

## Week 3 — J1 Mechanical Architecture

**Goal:** Determine exactly how J1 should work mechanically.

### Design Decisions

Determine:

- Base geometry
- Rotating structure
- Bearing arrangement
- Bearing spacing
- Shaft arrangement
- Motor position
- Pulley position
- Belt path
- J2 mounting interface
- Structural load path

### CAD

Create a rough complete J1 assembly containing:

- Base
- Rotating structure
- Bearings
- Shaft
- Motor envelope
- Encoder envelope
- Pulley envelopes
- J2 interface

Focus on mechanical function rather than cosmetic detail.

### Output

**J1 mechanical architecture v1**

---

## Week 4 — J1 Motor, Encoder, and Transmission

**Goal:** Turn the J1 concept into a physically plausible actuator.

### CAD

Model actual hardware where possible:

- Motor
- Motor shaft
- Encoder
- Encoder mounting/interface
- Bearings
- Shaft
- Coupler
- Motor mount
- Pulley envelopes

Establish:

- Driven pulley
- Motor pulley
- Belt path
- Belt tensioning concept
- Transmission ratio

### Engineering Calculations

Calculate:

- Required torque
- Payload torque
- Estimated arm-load contribution
- Motor torque margin
- Transmission ratio
- Pulley torque
- Approximate belt forces
- Preliminary belt sizing

For the payload alone:

\[
M = mgr
\]

\[
M=(2)(9.81)(0.4)\approx7.85\text{ N·m}
\]

This is only the payload contribution. The mass of the arm and other components must also be considered.

### Output

**J1 actuator and transmission design**

---

## Week 5 — J1 Structural CAD

**Goal:** Develop the actual structural components around the calculated loads.

### Detailed CAD

Design:

- Base
- Structural plates
- Ribs
- Bearing supports
- Motor mount
- Shaft supports
- J2 mounting structure
- Fastener interfaces

### Design Considerations

Evaluate:

- Stiffness
- Load path
- Bearing support
- Manufacturability
- 3D-printability where appropriate
- Material usage
- Assembly access
- Fastener access
- Part separation
- Cable clearance

### Output

**J1 structural CAD v1**

---

## Week 6 — Complete J1 Assembly

**Goal:** Turn the individual J1 components into a complete subsystem.

### Integrate

- Motor
- Encoder
- Bearings
- Shaft
- Coupler
- Pulleys
- Belt
- Structural components
- Fasteners
- J2 interface

### Assembly Checks

Check:

- Interference
- Clearance
- Assembly sequence
- Fastener accessibility
- Bearing installation
- Belt clearance
- Motor clearance
- Encoder clearance
- Cable exit
- Cable routing
- Serviceability

### Electronics Boundary

Electronics are included **only as mechanical interfaces** where required, such as:

- Motor cable routing
- Encoder cable routing
- Connector clearance
- Electronics envelopes
- Strain relief

Electronics themselves are outside the primary MMAE 497 scope.

### Output

**Complete J1 assembly v1**

---

## Week 7 — J1 Engineering Validation and Revision

**Goal:** Verify that J1 is mechanically credible.

### Inventor Mass Properties

Estimate:

- Part masses
- Subassembly mass
- Center of mass
- Preliminary total arm mass

### Engineering Analysis

Evaluate:

- Payload torque
- J1 torque
- Arm mass contribution
- Shaft loading
- Bearing loading
- Belt tension
- Motor capability
- Transmission ratio
- Basic structural safety

A full-arm FEA study is not required.

### Design Iteration

Use the calculations to revise the CAD where necessary.

Examples:

- Increase shaft diameter
- Increase bearing spacing
- Increase plate thickness
- Add ribs
- Move the motor
- Change pulley ratio
- Modify mounting geometry

### Output

**J1 design v2 + engineering calculations**

### Gate 2

At the end of Week 7:

> J1 should be a mechanically credible design that could reasonably be prototyped.

---

# Phase 3 — J2 and J3 Development

## Week 8 — J2 Preliminary Design

**Goal:** Develop the shoulder architecture.

### CAD

Model:

- Motor
- Encoder
- Bearings
- Shaft
- Transmission envelope
- Structural link/housing
- J1 interface
- J3 interface
- Joint limits

### Engineering

Perform enough analysis to determine whether the J2 actuator and structure are plausible.

Focus on:

- Torque
- Motor capability
- Packaging
- Basic structural requirements

Do not try to make J2 as detailed as J1.

### Output

**J2 preliminary assembly**

---

## Week 9 — J3 Preliminary Design

**Goal:** Develop the elbow architecture.

### CAD

Model:

- Motor
- Encoder
- Bearings
- Shaft
- Transmission
- Structural components
- J2 interface
- J4 interface
- Joint limits

### Engineering

Check:

- Torque
- Motor capability
- Packaging
- Approximate structural loading

### Output

**J3 preliminary assembly**

---

## Week 10 — J1–J3 Integration

**Goal:** Create the first mechanically coherent 3-DOF section of the robot.

### Assembly

Integrate:

`J1 → J2 → J3`

### Check

- Reach
- Workspace
- Joint limits
- Interference
- Self-collision
- Motor packaging
- Encoder packaging
- Cable routing
- Mass distribution
- Structural interfaces

### Revise

Fix problems discovered during integration.

### Output

**Integrated J1–J3 mechanical assembly**

### Gate 3

You should be able to show:

> "This is the mechanically developed first three joints of the robot."

---

# Phase 4 — Complete the 6-DOF Architecture

## Week 11 — J4 Preliminary Design

**Goal:** Extend the arm into the wrist section.

### CAD

Develop preliminary:

- Motor
- Encoder
- Bearing arrangement
- Shaft
- Transmission
- Structural housing
- J3 interface
- J5 interface
- Joint limits

Focus on architecture rather than detail.

### Output

**J4 preliminary assembly**

---

## Week 12 — J5 + J6 Preliminary Design

**Goal:** Complete the mechanical architecture of the final two joints.

### J5

Model:

- Motor
- Encoder
- Axis
- Bearings
- Housing
- Transmission envelope
- Interfaces

### J6

Model:

- Motor
- Encoder
- Bearings
- Housing
- Wrist/end-effector interface
- Transmission envelope
- Joint limits

### Output

**Complete preliminary J1–J6 assembly**

At this point, the entire arm should exist in CAD.

---

# Phase 5 — Full-Arm Parametric Integration

## Week 13 — Parametric CAD Refinement

**Goal:** Turn the individual joint designs into a coherent parametric robotic-arm assembly.

### Clean Up

- Parameters
- Constraints
- Origins
- Coordinate systems
- Naming
- Interfaces
- Joint limits
- Assembly structure

### Parameter Testing

Change important parameters and verify that the model updates correctly.

Examples:

- Link length
- Motor position
- Pulley diameter
- Bearing spacing
- Joint offset

### Integration Checks

Look for:

- Interferences
- Impossible assemblies
- Broken constraints
- Packaging conflicts
- Missing interfaces

### Output

**Parametric 6-DOF CAD v1**

---

# Week 14 — CAD → URDF / Initial Simulation

**Goal:** Verify that the mechanical CAD architecture translates correctly into the robot's kinematic model.

### Start with J1–J3

Create:

- Links
- Joints
- Joint axes
- Origins
- Coordinate frames
- Joint limits
- Visual geometry
- Collision geometry

### Verify

- Axis directions
- Joint orientation
- Link dimensions
- Coordinate frames
- Joint ranges

### If Time Permits

Begin adding J4–J6.

### Output

**Functional J1–J3 URDF**

---

# Weeks 15–16 — Documentation and Wrap-Up

The final two weeks are intentionally protected from major new engineering work.

---

## Week 15 — Documentation and Final CAD Cleanup

### CAD

- Finalize J1
- Finalize the 6-DOF assembly
- Clean up file structure
- Ensure important parameters are understandable
- Fix naming
- Remove unnecessary construction geometry
- Create final screenshots/renders
- Verify the assembly opens correctly

### Documentation

Document:

- Original requirements
- Design goals
- Kinematic architecture
- J1 design process
- Transmission design
- Structural decisions
- Engineering calculations
- Major design iterations
- Problems encountered
- Solutions implemented
- Simulation status
- What remains unfinished

### GitHub / Project Documentation

Update:

- CAD references
- Project overview
- Relevant images
- Final project status
- Known limitations

### Output

**Final CAD revision + draft project documentation**

---

## Week 16 — Final Review and Course Wrap-Up

### Technical Review

Verify:

- 6-DOF assembly opens correctly
- Major parameters are correct
- J1 is complete
- J2–J6 are sufficiently represented
- Calculations are organized
- URDF works
- Documentation is clear
- Assumptions are stated
- Unfinished work is identified

### Final Report

Summarize:

1. Requirements
2. Initial architecture
3. Design methodology
4. J1 development
5. J2–J6 development
6. Engineering calculations
7. CAD iterations
8. URDF/Gazebo validation
9. Results
10. Limitations
11. Future work

### Final Progress Update

Prepare a final update for Professor Das covering:

- What was completed
- What changed from the original plan
- Major engineering decisions
- What remains for the larger robot project

### Output

**Final MMAE 497 project package**

---

# Time Allocation

The course represents approximately **4 hours/week**, or **~64 hours total**.

| Activity | Approx. Hours |
|---|---:|
| 6-DOF architecture and skeleton | 7 |
| Detailed J1 CAD | 15 |
| J1 engineering calculations/iteration | 7 |
| J2–J3 CAD | 8 |
| J4–J6 CAD | 7 |
| Full-arm integration/parametric cleanup | 5 |
| URDF/Gazebo | 4 |
| Documentation/wrap-up | 7 |
| Contingency | 4 |
| **Total** | **64** |

---

# Priority if the Schedule Slips

## Must Complete

1. 6-DOF parametric skeleton
2. Detailed J1
3. J1 calculations and design iteration
4. Preliminary J2/J3
5. Preliminary J4–J6

## Secondary

6. Full-arm refinement
7. J1–J3 URDF
8. Basic Gazebo validation

## Optional

9. Full 6-DOF URDF
10. Physical 3D-printed prototype
11. More advanced simulation

### Rule

> **If the schedule becomes constrained, prioritize mechanical CAD and J1 engineering over simulation and physical prototyping.**

The core academic workflow is:

**Requirements → Parametric CAD → Mechanical Design → Engineering Analysis → Design Iteration → Final CAD → Kinematic Validation**