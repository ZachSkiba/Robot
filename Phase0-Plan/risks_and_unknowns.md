# Phase 0 – Risks & Unknowns

## **General Risks**
- **Overcomplexity:** Spending too much time refining simulation or kinematics can delay Phase 1.  
- **Misalignment of roles:** Lack of coordination between mechanical and data science tasks could cause inconsistencies.  
- **Incorrect assumptions:** Unrealistic torque, link lengths, or joint limits could invalidate simulation results.  
- **Software bugs:** Errors in FK, IK, or trajectory code could produce misleading visualizations.  
- **Data schema mismatch:** Poorly defined logging fields may cause refactors in Phase 1.  

---

## **Mechanical Design Risks**
- Link lengths or joint limits may be physically infeasible when hardware is built.  
- Torque calculations may underestimate worst-case payload or gravity effects.  
- Misaligned coordinate frames could lead to FK/IK errors.  

---

## **Stepper Motor & Control Risks**
- Microstepping assumptions may not match real hardware behavior.  
- Stepper torque/speed limits may restrict achievable trajectories.  
- Step-to-angle conversions may introduce cumulative errors in simulation.  

---

## **Kinematics & Simulation Risks**
- FK/IK solutions may produce singularities or unreachable positions.  
- Discrete step simulations may not accurately capture continuous motion dynamics.  
- Trajectory planning may exceed safe simulated joint limits.  
- Errors in simulation visualization could lead to false confidence.  

---

## **Unknowns**
- Exact motor response and stepper behavior in real hardware.  
- Realistic step limits and maximum speed without skipped steps.  
- Latency or timing constraints when later integrating Python → Arduino.  
- Numerical stability of IK solver for edge-of-reach positions.  
- Potential conflicts between data logging needs and physical feasibility.  

---

## **Mitigation Strategies**
- Keep Phase 0 **time-boxed**: stop when objectives are met.  
- Validate FK and IK via **cross-checks** (Python vs paper vs optional MATLAB).  
- Document all assumptions, constraints, and results carefully.  
- Keep all link lengths, torque calculations, and coordinate frames **physically reasonable**.  
- Ensure data schema is flexible enough to accommodate future hardware logs.  
