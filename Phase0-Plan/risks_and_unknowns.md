# Phase 0 — Risks & Unknowns

## **General Risks**
- **Overcomplexity:** Spending too much time refining simulation, FK/IK, or trajectory planning can delay Phase 1.  
- **Role misalignment:** Lack of coordination between mechanical (Nicholas) and data science (Zach) tasks could produce inconsistent results.  
- **Incorrect assumptions:** Unrealistic torque, link lengths, joint limits, or coordinate frames could invalidate simulation outcomes.  
- **Software bugs:** Errors in FK, IK, or trajectory code may produce misleading visualizations.  
- **Data schema mismatch:** Poorly defined logging fields may require refactoring during Phase 1 integration.  

---

## **Mechanical Design Risks**
- Link lengths or joint limits may be physically infeasible when hardware is built.  
- Torque calculations may underestimate worst-case payload or gravity effects.  
- Misaligned coordinate frames can propagate FK/IK errors into trajectory simulations.  
- Minor adjustments in the 3D model may be required to match optional reference hardware.  

---

## **Stepper Motor & Control Risks**
- Microstepping assumptions may not match real-world stepper behavior.  
- Stepper torque and speed limits may restrict achievable trajectories.  
- Step-to-angle conversions may introduce cumulative errors in simulation, especially for multi-joint coordinated motion.  
- Optional reference hardware may not perfectly reflect full-scale performance.  

---

## **Kinematics & Simulation Risks**
- FK/IK solutions may produce singularities, unreachable positions, or non-physical joint angles.  
- Discrete step simulations may not fully capture continuous motion dynamics.  
- Trajectory planning may exceed safe simulated joint limits if assumptions are off.  
- Visualization errors could produce false confidence in results.  

---

## **Unknowns**
- Exact motor response, step accuracy, and torque behavior in real hardware.  
- Realistic step limits, acceleration/deceleration, and maximum speed without skipped steps.  
- Latency or timing constraints when integrating Python simulations with microcontroller control.  
- Numerical stability of IK solver near workspace boundaries.  
- Conflicts between data logging requirements and mechanical/physical feasibility.  

---

## **Mitigation Strategies**
- Time-box Phase 0: stop once simulation objectives are met.  
- Validate FK and IK via **cross-checks** (Python vs paper derivation vs optional MATLAB/Simulink).  
- Document all assumptions, constraints, and decisions carefully.  
- Keep link lengths, torque calculations, and coordinate frames **physically reasonable**.  
- Ensure data schema is **flexible**, ready to accommodate Phase 1 hardware logs.  
- Optional: test with single-motor reference hardware to confirm assumptions before full build.