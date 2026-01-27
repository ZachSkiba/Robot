# Mini-Projects – Assumptions & Constraints

## **Assumptions**

### General
- You have access to one motor (servo or stepper) and one microcontroller (Arduino Mega / ESP32).  
- Python environment is installed and can interface with the microcontroller.  
- Sensors (encoder, step count) provide accurate readings within nominal tolerances.  
- Mini-projects will be completed within 1–2 weeks; time is limited.  
- Hardware behaves similarly in single-joint tests as it will in multi-joint configuration.  
- PID control is sufficient for stabilizing a single joint.  
- Early tests may have noise or minor wiring issues, but nothing catastrophic.  
- Mini-projects are **skill unlocks**, not fully optimized systems or final design.  

### Mini-Project A – Single-Axis Smart Joint
- The motor can reach commanded positions reliably.  
- The sensor feedback loop can be read in real-time.  
- Data logging and plotting in Python are feasible.  
- You can debug hardware calmly without redesigning the motor or electronics.  

### Mini-Project B – Controller → Motor
- PS5 controller input can be read via microcontroller or Python.  
- Motor speed/position can respond smoothly to joystick commands.  
- Logging joystick and motor response is feasible.  
- Recorded trajectories can be replayed on the same motor.  

### Mini-Project C (Optional) – 2-Link Python Simulation
- Python can simulate 2 joints with forward and inverse kinematics.  
- Visualization using Matplotlib or similar is possible.  
- Kinematics calculations are accurate enough to guide future hardware design.  

---

## **Constraints**

### General / Mini-Project Scope
- Stop each mini-project **once learning objectives are achieved**:
  - **Mini-Project A:** Command position → joint reaches target → plot error vs time.  
  - **Mini-Project B:** Smooth joystick-controlled motion → can replay trajectory.  
  - **Mini-Project C:** FK + IK works → plots match expected motion.  
- Do **not** over-optimize, add ML, or redesign hardware.  
- Only use one joint for Mini-Project A; only simulate 2 links for Mini-Project C.  
- Hardware and software must be safe to handle (avoid overheating motors, short circuits, or mechanical damage).  
- Mini-projects are short — target 1–2 weeks combined, not longer.  

### Technical
- Motor current ≤ datasheet limits to prevent damage.  
- Sensors and microcontroller operate within voltage/current specs.  
- Data logging and plotting must be completed in real-time or post-processing.  
- Python scripts and microcontroller firmware must remain simple; avoid unnecessary complexity.  

---

**Notes:**  
- These assumptions and constraints are strictly scoped for **Phase 0 mini-projects**.  
- Purpose: quickly unlock skills, gain confidence, and de-risk full arm design.  
- The moment objectives are achieved, **stop and move to Phase 1**.
