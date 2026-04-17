# Phase 6 - Mobile Manipulation and Full Autonomy

**Duration:** ~8–12 weeks (can be stretched)  
**Goal:** Turn the arm into a complete autonomous robot system by adding mobility and high-level decision making.  

## Outcomes
- Mobile base + robotic arm integration  
- Global + local planning  
- Perception-driven task execution  
- Full autonomy loop (sense → decide → act)  
- End-to-end autonomous demo  

---

## Plan

#### STEP 6.1 — Mobile Base Design (Weeks 1–2)

**Together**
- Decide platform:  
  - Differential drive (recommended)  
  - Table-top scale (apartment-safe)  

**Nicholas (MechE)**
- Design base chassis  
- Wheel selection + motor mounting  
- Stability analysis (arm motion + base)  

**Zach (DS)**
- Define software architecture  
- Plan state representation  
- Set up simulation for base motion  

**Coordination**
- Trade off:  
  - stability vs agility  
  - size vs reach  

---

#### STEP 6.2 — Base Control & Odometry (Weeks 3–4)

**Together**
- Define:  
  - coordinate frames  
  - control interface  

**Nicholas**
- Integrate motors + encoders  
- Tune low-level motion control  
- Validate straight-line + rotation accuracy  

**Zach**
- Implement odometry estimation  
- Fuse sensor data  
- Log drift + error  

**Coordination**
- Validate odometry estimates against measured motion.

---

#### STEP 6.3 — Navigation & Planning (Weeks 5–6)

**Together**
- Define environment:  
  - apartment-scale map  
  - static obstacles  

**Zach**
- Implement global planner (A*, RRT, etc.)  
- Local collision avoidance  
- Task-level planning logic  

**Nicholas**
- Validate physical feasibility  
- Tune acceleration limits  
- Ensure arm stability while moving  

**Coordination**
- Confirm that navigation, dynamics, and arm constraints remain consistent.

---

#### STEP 6.4 — Arm + Base Coordination (Weeks 7–8)

**Together**
- Define behaviors:  
  - drive → stop → manipulate  
  - manipulate → move → repeat  

**Zach**
- High-level state machine  
- Task sequencing  
- Failure recovery logic  

**Nicholas**
- Safe arm poses while moving  
- Mechanical stress analysis  
- Collision envelope definition  

**Coordination**

---

#### STEP 6.5 — Autonomous Task Demo (Weeks 9–10)

**Together**
- Pick one clean demo:  
  - find object → drive to it → pick → place  
  - object sorting in different locations  
  - “trash” to bin (simplified)  

**Zach**
- Measure success rate  
- Optimize planning efficiency  
- Log autonomy metrics  

**Nicholas**
- Improve mechanical reliability  
- Reduce vibration + slip  
- Increase repeatability  

**Coordination**
- Iterate until the behavior is repeatable and not dependent on manual intervention.

---

#### STEP 6.6 — Final System Polish (Weeks 11–12)

**Together**
- Deliver:  
  - full demo video  
  - architecture diagram  
  - failure analysis  
  - roadmap for future work  

## Role Split

| Area                 | Zach (DS) | Nicholas (MechE) |
|----------------------|-----------|----------------|
| Planning & autonomy   | ✅        | ➖             |
| Control & odometry    | ✅        | ➖             |
| Mechanical design     | ➖        | ✅             |
| Stability & dynamics  | ➖        | ✅             |
| System integration    | ✅        | ✅             |
| Evaluation & demos    | ✅        | ✅             |
