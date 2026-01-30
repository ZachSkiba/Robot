# Phase 0 — System Overview (Updated)

## Purpose

Phase 0 provides a **system-level simulation and architectural validation** for the 3-DOF prototype of the planned 6-DOF robotic arm. It is entirely **virtual**, with no hardware involvement. The goals are:

- Verify kinematics, motion feasibility, and coordinate frames.
- Define data structures, logging, and metrics for future hardware integration.
- Lay the foundation for trajectory planning, motion limits, and eventual control software.

> **Key principle:** This phase de-risks all critical design decisions before any hardware is connected.

---

## System Layers in Phase 0

| Layer                  | Functionality                                | Notes / Phase 0 Scope |
|------------------------|----------------------------------------------|----------------------|
| **Virtual Physical Layer** | Models links, joints, and physical constraints | Use simplified mass/inertia; joint limits approximate; no motors yet |
| **Mathematical Layer** | FK and preliminary IK (numerical & symbolic) | Verify DH parameters, check singularities, compute Jacobians for 3-DOF |
| **Simulation Layer**   | 2D/3D visualization and animation            | Animate motion between targets; optionally add collision boundaries; motion smoothing |
| **Data & Metrics Layer** | Logging and analysis                        | Define JSON or CSV schema for joint commands, angles, end-effector positions, error metrics; generate plots of trajectory tracking and feasibility |

---

## Workflow
Target Pose --> IK Solver --> Joint Angles --> FK Verification --> Visualization
| |
Error Metrics Plot & Save

**Step-by-step:**

1. Target pose specified in Cartesian space.  
2. IK solver computes feasible joint angles.  
3. FK verifies computed angles against expected end-effector pose.  
4. Visualization animates motion and checks plausibility.  
5. Data & metrics layer logs and plots results for review.

---

## Phase 0 Responsibilities

| Layer              | Zach (DS)                                             | Nicholas (MechE)                                 |
|-------------------|------------------------------------------------------|-------------------------------------------------|
| **Virtual Physical** | Define link lengths & joint limits, check feasibility | Sketch and validate physical plausibility; review kinematic chain |
| **Math (FK / IK)**  | Implement FK, numerical IK, compute errors          | Validate equations, signs, and singularities; verify joint limits |
| **Simulation**      | Build visualization, animate motion, save outputs   | Validate realism, suggest adjustments, check collisions |
| **Data & Metrics**  | Define logging schema, generate plots               | Interpret plots, verify realism, confirm trajectory smoothness |

---

## Success Criteria

- Simulated 3-DOF arm matches planned physical dimensions.  
- FK and IK implementations verified against analytical derivations.  
- Smooth and physically plausible motion demonstrated in 2D/3D visualization.  
- Data schema established for logging joint angles, velocities, and end-effector pose.  
- Metrics clearly indicate motion feasibility, error tracking, and singularity handling.

---

## Risks & Unknowns

| Risk / Unknown                  | Impact | Mitigation in Phase 0 |
|---------------------------------|--------|----------------------|
| IK solver fails near singularities | High   | Implement numerical fallback; test multiple configurations |
| Joint limits incorrect           | Medium | Cross-check with CAD dimensions; plot reachable workspace |
| Trajectory infeasibility         | Medium | Use trapezoidal approximation for Phase 0; check velocity/acceleration proxies |
| Collision / link interference    | Medium | Simple bounding boxes in visualization |
| Data schema gaps                 | Low    | Review and standardize logging structure for Phase 1 |

---

## Guiding Principle

> Phase 0 proves the concept virtually. Hardware decisions, trajectory planning, safety constraints, and data collection strategies must flow directly from this validated simulation.

# Phase 0 — Timeline (Adjusted for Availability)

## Combined Availability

- **Hours per day:** 4 hours  
- **Days per week:** 5 days  
- **Total weekly availability:** 20 hours/week

---

## Original Estimate

- ~8–10 full person-days (~8 hours/day)  
- Total: 64–80 hours

---

## Adjusted Timeline

| Task                          | Hours Needed |     Days      | Notes |
|-------------------------------|-------------|----------------|-------|
| Define virtual physical model | 8           | 2              | Includes joint limits and CAD sketches |
| Implement FK                  | 8           | 2              | Python scripts with verification |
| Implement numerical IK        | 16          | 4              | Iterative solver, singularity fallback |
| Build basic 2D/3D simulation  | 16          | 4              | Visualization using Matplotlib3D, VPython, or lightweight PyBullet |
| Logging & data schema         | 4           | 1              | JSON/CSV format, test logging |
| Plotting & metrics            | 8           | 2              | Trajectory plots, error checks |
| Testing & validation          | 8           | 2              | Verify FK ↔ IK consistency, workspace coverage |

---

## Total Hours and Duration

- **Sum of hours:** 8 + 8 + 16 + 16 + 4 + 8 + 8 = 68 hours  
- **Weekly availability:** 20 hours/week  
- **Total duration:** 68 ÷ 20 ≈ 3.4 weeks  

✅ Realistic estimate: **~3.5–4 weeks** at your combined pace.

---

## Recommended Weekly Plan

| Week | Deliverables |
|------|-------------|
| **Week 1** | Virtual physical model + FK implementation |
| **Week 2** | Numerical IK implementation (basic) + start visualization |
| **Week 3** | Complete visualization + logging/data schema + plotting framework |
| **Week 4** | Testing, validation, error analysis, finalize plots, verify workspace coverage |

> Note: Includes small buffer for unexpected issues such as IK convergence near singularities or visualization adjustments.