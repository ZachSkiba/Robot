# PHASE 0 — Architecture, Math, & Simulation

**Duration:** ~2 weeks  
**Goal:** A simulated robotic arm that can move to targets with plots, metrics, and design decisions justified

If Phase 0 is strong, everything after it becomes easier and more impressive.

---

## Phase 0 Outcomes

At the end of Phase 0, you will have:

- A clearly defined **3-DOF robotic arm design**
- Forward kinematics implemented (Python, MATLAB optional)
- A simulation that:
  - takes a target
  - computes joint angles
  - visualizes motion
- An agreed-upon **data schema** for later phases

This alone is **resume-worthy**.

---

## STEP-BY-STEP PLAN (WITH ROLES)

---

## STEP 0.1 — Define the Arm Together (Day 1–2)

### What You Decide Together
- Number of DOFs: **3**
- Joint 1: Base rotation  
- Joint 2: Shoulder  
- Joint 3: Elbow  
- Rough (realistic) link lengths  
- Joint limits (important for safety later)

### Zach (Data Science Focus)
- Write down:
  - coordinate frame assumptions
  - variable names
- Start a shared Google Doc or README:
  - **"Robotic Arm Assumptions"**

### Nicholas (Mechanical Engineering Focus)
- Sketch arm concepts (paper is fine)
- Think about:
  - physical feasibility
  - torque directions
  - motor mounting

### Interaction Point
You *constructively argue* about:
- Is this DOF layout overkill?
- What motions do we actually want?

This is **real engineering collaboration**.

---

## STEP 0.2 — Coordinate Frames & Math (Day 3–4)

### Together
Agree on:
- base frame
- joint axes
- sign conventions

**Do not skip this step.**

### Zach
- Implement **Forward Kinematics** in Python
- Use:
  - NumPy
  - homogeneous transforms or DH parameters
- Write functions like:
  - `fk(joint_angles) -> end_effector_pose`

### Nicholas
- Independently derive FK on paper
- Check:
  - axes
  - rotations
  - physical interpretation

### Interaction Point
- Compare Python vs paper
- If they don’t match, someone is wrong — **this is good**
- This is exactly how robotics teams work

---

## STEP 0.3 — First Simulation (Day 5–6)

### Zach
- Build a simple 2D or 3D visualization:
  - joint positions
  - links
  - end effector
- Animate motion between two poses

### Nicholas
- Validate:
  - link lengths look reasonable
  - motion matches physics intuition
- Suggest mechanical changes:
  - joint orientation
  - link length adjustments

### Interaction Point
Iterate:
- math ↔ visualization ↔ physical realism  
No one is “done” until both agree.

---

## STEP 0.4 — Define What Data Will Exist Later (Day 7)

This step is **huge** and often skipped.

### Together — Define the Data Schema

Example fields:
- timestamp
- joint_1_cmd
- joint_2_cmd
- joint_3_cmd
- joint_1_est
- joint_2_est
- joint_3_est
- ee_x
- ee_y
- ee_z

### Zach
Think like a data scientist:
- What will we plot later?
- What would ML models need?

### Nicholas
Think like a control engineer:
- What is physically measurable?
- What is an estimate vs ground truth?

### Interaction Point
Compromise between:
- “nice to have”
- “physically realistic”

This prevents painful refactors later.

---

## STEP 0.5 — Inverse Kinematics (Intro Only) (Day 8–10)

### Together
Decide between:
- analytical IK (if feasible)
- numerical IK (gradient or search)

### Zach
- Implement numerical IK in Python
- Focus on:
  - convergence
  - error metrics

### Nicholas
- Evaluate:
  - joint limit violations
  - strange poses
  - singularities (intuitive level)

### Interaction Point
Tune:
- step sizes
- constraints
- failure handling

This is where **optimization thinking** begins.

---

## STEP 0.6 — Metrics & Plots (Day 11–12)

### Zach
Add plots:
- joint angles vs time
- end-effector error
- automatically saved results

### Nicholas
Interpret plots:
- Why does a joint oscillate?
- Is this motion realistic?

### Interaction Point
Learn to:
- trust data
- question it when physics disagrees

This skill is gold in interviews.

---

## STEP 0.7 — Phase 0 Deliverables (Day 13–14)

### Together
Prepare:
- Short README including:
  - problem statement
  - arm design
  - plots
- Demo script:
  - target → motion → visualization

You should be able to say:

> "Before building hardware, we validated our robotic arm design through simulation, kinematics, and data analysis."

That’s a serious sentence.

---

## Why Both of You Are Always Useful

| Area | Zach (DS) | Nicholas (MechE) |
|-----|-----------|------------------|
| FK / IK | Implement | Validate physics |
| Simulation | Code & plot | Sanity-check realism |
| Data schema | Design | Ensure measurability |
| Metrics | Analyze | Interpret physically |
| Decisions | Quantitative | Mechanical intuition |

No one is ever waiting.

---

## After Phase 0

Phase 1 becomes **execution**, not confusion:
- CAD follows simulation
- sensors follow schema
- logging follows design
