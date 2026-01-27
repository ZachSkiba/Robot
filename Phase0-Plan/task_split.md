# Phase 0 — Task Split

## Purpose

This document defines **task responsibilities for Phase 0** of the robotic arm project (Architecture, Math, & Simulation).

It clarifies what each contributor focuses on while ensuring collaboration at key interaction points.

---

## 1. Arm Definition (Step 0.1)

**Together:** Decide DOF layout, joint types, link lengths, joint limits

| Task                                       | Zach (DS) | Nicholas (MechE) |
| ------------------------------------------ | --------- | ---------------- |
| Document coordinate frames and assumptions | ✅         | -                |
| Define variable names                      | ✅         | -                |
| Sketch arm concepts                        | -         | ✅                |
| Assess feasibility and torque directions   | -         | ✅                |
| Discuss DOF layout and motions             | ✅         | ✅                |

---

## 2. Coordinate Frames & Math (Step 0.2)

| Task                                               | Zach (DS) | Nicholas (MechE) |
| -------------------------------------------------- | --------- | ---------------- |
| Implement FK in Python                             | ✅         | -                |
| Derive FK on paper                                 | -         | ✅                |
| Compare Python vs paper FK                         | ✅         | ✅                |
| Check axes, rotations, and physical interpretation | -         | ✅                |

---

## 3. Simulation (Step 0.3)

| Task                                     | Zach (DS) | Nicholas (MechE) |
| ---------------------------------------- | --------- | ---------------- |
| Build 2D/3D visualization                | ✅         | -                |
| Animate motion between poses             | ✅         | -                |
| Validate link lengths and motion realism | -         | ✅                |
| Suggest mechanical adjustments           | -         | ✅                |
| Iterate math ↔ visualization ↔ realism   | ✅         | ✅                |

---

## 4. Data Schema (Step 0.4)

| Task                                                | Zach (DS) | Nicholas (MechE) |
| --------------------------------------------------- | --------- | ---------------- |
| Define telemetry fields for logging                 | ✅         | ✅                |
| Identify ML and plotting requirements               | ✅         | -                |
| Verify what is physically measurable                | -         | ✅                |
| Decide compromise between nice-to-have and feasible | ✅         | ✅                |

---

## 5. Inverse Kinematics (Step 0.5)

| Task                                                    | Zach (DS) | Nicholas (MechE) |
| ------------------------------------------------------- | --------- | ---------------- |
| Implement numerical IK in Python                        | ✅         | -                |
| Check joint limits, singularities, and pose feasibility | -         | ✅                |
| Tune step sizes, constraints, and failure handling      | ✅         | ✅                |

---

## 6. Metrics & Plots (Step 0.6)

| Task                                         | Zach (DS) | Nicholas (MechE) |
| -------------------------------------------- | --------- | ---------------- |
| Generate plots (joint angles, errors, etc.)  | ✅         | -                |
| Automatically save results                   | ✅         | -                |
| Interpret plots for realism and oscillations | -         | ✅                |
| Discuss and refine plots                     | ✅         | ✅                |

---

## 7. Phase 0 Deliverables (Step 0.7)

| Task                                                             | Zach (DS) | Nicholas (MechE) |
| ---------------------------------------------------------------- | --------- | ---------------- |
| Prepare short README documenting problem, arm design, plots      | ✅         | ✅                |
| Prepare demo script: target → motion → visualization             | ✅         | ✅                |
| Ensure deliverables show validated design, FK/IK, and simulation | ✅         | ✅                |

---

## Guiding Principle

> **Phase 0 tasks are split by expertise but always involve collaboration at interaction points. Zach leads data, plots, and code; Nicholas leads mechanical feasibility; al
