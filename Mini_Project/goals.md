# Mini-Projects – Goals

## **General Goals for All Mini-Projects**
- Unlock core skills needed for full robotic arm development.  
- Build confidence in handling hardware and software without panic.  
- Verify that fundamental systems (motor, sensor, controller) work as expected.  
- Keep scope limited: learn quickly, stop immediately when objectives are achieved.  
- Avoid over-optimization, ML, full-arm builds, or complex simulations at this stage.  

---

## **Mini-Project A – Single-Axis Smart Joint**
**Objective:** Command a single joint reliably and understand its behavior.  

**Specific Goals:**  
1. Wire one motor and one sensor to the microcontroller.  
2. Implement a feedback loop using PID control.  
3. Write a Python script to:  
   - Send commands to the motor  
   - Log sensor data  
   - Plot error vs time  
4. Understand real motor behavior:  
   - Response to commands  
   - Noise in sensor data  
   - Importance of PID tuning  
5. Build debugging skills for hardware calmly.  

**Completion Criteria:**  
- Motor reaches commanded positions reliably.  
- Error can be plotted vs time.  
- No further optimization needed; ready to scale to multi-joint arm.  

**Timeframe:** 5–7 days  

---

## **Mini-Project B – Controller → Motor**
**Objective:** Learn human-in-the-loop control and trajectory logging.  

**Specific Goals:**  
1. Connect a PS5 controller to the microcontroller or Python interface.  
2. Control motor velocity or position using joystick input.  
3. Log both joystick input and motor response.  
4. Replay recorded trajectories on the motor.  
5. Understand motor limits, saturation, and smooth vs jerky motion.  

**Completion Criteria:**  
- Smoothly move the motor using joystick.  
- Can replay recorded motion accurately.  

**Timeframe:** 3–4 days  

---

## **Mini-Project C (Optional) – 2-Link Arm in Python**
**Objective:** Build kinematic intuition without hardware.  

**Specific Goals:**  
1. Simulate a 2-link arm in Python.  
2. Implement forward kinematics (FK).  
3. Implement inverse kinematics (IK) for reachable points.  
4. Visualize motion using Matplotlib or similar.  

**Completion Criteria:**  
- FK and IK work correctly.  
- Plots match expected motion of the 2-link arm.  

**Timeframe:** 2–3 days  

---

**Notes:**  
- Mini-project goals are strictly scoped to **skill unlocks**, not full design.  
- Stop immediately once goals are achieved.  
- These goals provide the foundation for **Phase 1: full arm assembly and control**.
