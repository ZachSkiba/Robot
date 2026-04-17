# Phase 2 - Trajectory Execution and Optimization

**Duration:** ~4–6 weeks  
**Goal:** The arm executes repeatable trajectories and quantitatively improves motion quality through optimization (no ML yet).  

## Outcomes
- Deterministic joint-space & Cartesian trajectories  
- Defined cost functions  
- Automated experiments  
- Quantitative comparison of:  
  - naïve control vs optimized control  
- Plots + metrics that clearly show improvement  

## Plan

#### STEP 2.1 — Define Motion Goals & Metrics (Days 1–3)

**Together**
- Decide:  
  - What motions matter?  
    - point-to-point  
    - pick-and-place (no object yet)  
  - What “good” means:  
    - accuracy  
    - smoothness  
    - speed  
    - repeatability  

**Zach (DS)**
- Formalize metrics:  
  - endpoint error  
  - velocity/acceleration smoothness  
  - execution time  
- Define cost function structure  

**Nicholas (MechE)**
- Validate metrics physically:  
  - “Does this actually represent good motion?”  
- Identify constraints:  
  - max speed  
  - torque limits  
  - vibration concerns  

**Coordination**  
- Refine metrics until:  
  - mathematically clean  
  - physically meaningful  

---

#### STEP 2.2 — Trajectory Parameterization (Days 4–7)

**Together**
- Choose trajectory form:  
  - joint-space polynomials  
  - splines  
  - time-scaled profiles  

**Zach**
- Implement trajectory generator in Python  
- Parameters = decision variables  
- Generate trajectories offline  

**Nicholas**
- Check:  
  - feasibility  
  - joint limit compliance  
  - mechanical stress intuition  

**Coordination**  
- Bad trajectories get rejected early  
- Simulation ↔ hardware consistency checked  

---

#### STEP 2.3 — Execute & Log Trajectories on Hardware (Days 8–12)

**Zach**
- Send parameterized trajectories to arm  
- Automate:  
  - run N trials  
  - log all telemetry  
- Plot:  
  - joint angles  
  - end-effector paths  
  - error vs time  

**Nicholas**
- Observe:  
  - missed steps  
  - vibration  
  - backlash effects  
- Suggest:  
  - speed caps  
  - mechanical damping  
  - trajectory constraints  

**Coordination**  
- Data explains why motion looks bad  
- Mechanics explain why data looks bad  
- Use logging and mechanical observations together to diagnose poor motion quality.

---

#### STEP 2.4 — Optimization Loop (Days 13–20)

**Together**
- Decide:  
  - Which parameters are optimized  
  - Which constraints are hard vs soft  

**Zach**
- Implement optimization:  
  - grid search  
  - random search  
  - gradient-free methods  
- Run batch experiments  
- Rank trajectories by cost  

**Nicholas**
- Review optimized motions:  
  - Are they physically sensible?  
  - Are they abusing the system?  
- Add constraints if needed  

**Coordination**  
- Optimization → physical review → constraint update → repeat  
- Review optimized trajectories jointly and update constraints as needed.

---

#### STEP 2.5 — Validation & Comparison (Days 21–26)

**Zach**
- Compare:  
  - naïve trajectory  
  - hand-tuned trajectory  
  - optimized trajectory  
- Generate summary plots  

**Nicholas**
- Validate repeatability:  
  - run same trajectory multiple times  
- Identify sources of residual error  

**Coordination**  
- Jointly identify where optimized motion improves performance and where residual error remains.
- Record unresolved issues for Phase 3.

---

#### STEP 2.6 — Phase 2 Deliverables (Days 27–30)

**Together**
- Prepare:  
  - README:  
    - trajectory formulation  
    - cost functions  
    - optimization method  
  - Figures:  
    - before vs after plots  
  - Short demo video  

## Role Split

| Area                | Zach (DS) | Nicholas (MechE) |
|--------------------|-----------|----------------|
| Metrics & cost      | ✅        | ✅             |
| Trajectory math     | ✅        | ➖             |
| Physical feasibility| ➖        | ✅             |
| Optimization        | ✅        | ➖             |
| Hardware tuning     | ➖        | ✅             |
| Validation          | ✅        | ✅             |
