# Phase 0 – Assumptions & Constraints

## **Assumptions**

### General
- You have access to a laptop/desktop with Python 3.10+ installed.  
- Python libraries for numerical computation and visualization are installed (`numpy`, `matplotlib`, `scipy`).  
- A basic Arduino/stepper setup is available for reference testing if needed.  
- Sketches, notes, and derivations can be performed on paper or digital tools.  
- Both participants (mechanical engineer & data scientist) collaborate on decisions.  
- Phase 0 is limited to simulation, kinematics, and planning — no full hardware assembly yet.  

### Mechanical Design
- Arm will have 3 degrees of freedom (base rotation, shoulder, elbow).  
- Link lengths are realistic and feasible for the motors selected.  
- Torque required per joint is estimated including worst-case payload + gravity.  
- Joint limits are known or can be reasonably assumed for safety and motion feasibility.  

### Stepper Motor / Control
- Stepper motors are capable of required torque and microstepping resolution.  
- Step-to-angle conversion is linear and accurate within microstepping limits.  
- Max speed can be determined analytically or via Python simulation without skipped steps.  
- Microstep effects on motion smoothness can be approximated in simulation.  

### Kinematics & Simulation
- Forward kinematics (FK) equations are derivable for all 3 joints.  
- Inverse kinematics (IK) is solvable numerically or analytically within reachable workspace.  
- 2D simulation is sufficient for validating motion before 3D extension.  
- Step-based motion can be modeled as discrete increments for visualization.  

### Data & Logging
- Future Phase 1 logging schema can be defined in Phase 0.  
- Data for joint angles, steps, and end-effector positions is measurable or estimable in simulation.  

---

## **Constraints**

### General
- Phase 0 is limited to **simulation, calculation, and planning** — no full hardware assembly.  
- Timebox: ~2 weeks for completion.  
- Deliverables: verified FK/IK, stepper step mapping, trajectory plots, data schema, documentation.  
- Stop conditions: once simulations are validated and design decisions justified.  

### Mechanical
- Joint angles must respect safety limits to prevent collision or unrealistic designs.  
- Link lengths and motor selection must be mechanically feasible.  
- Arm should remain within defined workspace; no extreme configurations allowed.  

### Stepper Motors
- Steps per revolution, microstepping, and torque limits must be documented and respected.  
- Max step rates cannot exceed driver or motor limits.  
- Skipped steps, thermal limits, and current limits must be considered.  

### Simulation & Kinematics
- FK and IK solutions must be consistent with physical feasibility.  
- Step-based motion is modeled in discrete increments — continuous motion assumptions are not used.  
- Any approximations must not violate mechanical constraints or torque feasibility.  

### Data & Logging
- Data structures defined in Phase 0 must be compatible with future Phase 1 hardware implementation.  
- Logging schema must include: joint angles, steps, timestamps, and end-effector positions.  

---

**Notes:**  
- These assumptions and constraints are **strictly scoped to Phase 0**, separate from Mini-Projects.  
- Purpose: ensure Phase 0 outputs a fully validated arm design, stepper motion model, and simulation framework for Phase 1.  
