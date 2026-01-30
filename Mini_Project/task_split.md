# Mini-Projects – Task Split (Phase 0)

## **Guiding Principles**
- Each mini-project is a **skill unlock**, not a full design or production build.  
- Roles are split to maximize hands-on experience in both hardware and software.  
- Swap roles periodically to ensure both participants gain **full system familiarity**.  
- Stop each mini-project immediately once objectives are achieved.  
- Document all observations, plots, and configurations for Phase 1 integration.  

---

## **Week 1 – Mini-Project A (Single-Axis Smart Joint)**

| Role | Tasks | Notes |
|------|-------|------|
| **Participant 1 – Hardware Lead** | - Mount motor and sensor securely on bracket/platform<br>- Wire motor to microcontroller and driver<br>- Verify basic motor response and safety limits | Focus on wiring, mechanical stability, and safe handling |
| **Participant 2 – Software Lead** | - Develop Python interface to send motor commands<br>- Implement real-time logging of sensor data<br>- Plot position, velocity, and error vs time<br>- Implement PID feedback control | Focus on data visualization, tuning, and anomaly detection |
| **Both** | - Execute test trajectories: step, ramp, hold<br>- Observe plots and adjust PID parameters<br>- Swap roles halfway to gain cross-domain experience | Goal: joint reaches commanded positions; error plots match expected behavior |

**Completion Criteria:**  
- Joint moves reliably to commanded positions.  
- Plots confirm PID stability and expected behavior.  
- All safety limits (soft stops, E-stop) verified.  

---

## **Week 2 – Mini-Project B (Controller → Motor)**

| Role | Tasks | Notes |
|------|-------|------|
| **Participant 1 – Hardware Lead** | - Connect PS5 controller via USB/Bluetooth<br>- Wire motor and driver (reuse Mini-Project A hardware)<br>- Verify signal integrity and power safety | Focus on safe integration of human-in-the-loop control |
| **Participant 2 – Software Lead** | - Map joystick input to motor velocity/position commands<br>- Log controller input and motor response simultaneously<br>- Implement trajectory replay for recorded sessions | Focus on smooth motion, input filtering, and logging integrity |
| **Both** | - Test smooth joystick-driven motion<br>- Replay recorded trajectories and compare against logs<br>- Observe system response and validate safety overrides | Goal: smooth human-in-the-loop control; trajectories replay accurately without violating limits |

**Completion Criteria:**  
- Motor responds predictably and smoothly to controller input.  
- Logged trajectories can be replayed reliably.  
- Safety mechanisms (soft stops, velocity/acceleration limits, E-stop) override all motion commands.  

---

## **Mini-Project C (Optional) – 2-Link Python Simulation**

| Role | Tasks | Notes |
|------|-------|------|
| **Participant 1** | - Implement forward kinematics (FK) for 2-link planar arm<br>- Validate FK calculations | Focus on math correctness and plotting |
| **Participant 2** | - Implement inverse kinematics (IK) for reachable workspace points<br>- Validate IK solutions against FK | Focus on joint angle calculation and visualization |
| **Both** | - Generate plots/animations to visualize arm motion<br>- Compare FK predictions to IK results<br>- Adjust calculations as necessary | Goal: FK + IK algorithms validated; motion plots match expected behavior |

**Completion Criteria:**  
- FK and IK calculations produce correct positions.  
- Visualization confirms reachable workspace and motion accuracy.  
- Data and plots reusable for multi-joint (6-DOF) scaling.  

---

## **Key Notes**
- Swap roles whenever possible to ensure **equal exposure to hardware and software**.  
- Mini-projects are **short, focused, and stop when objectives are met**.  
- Document all plots, PID values, and trajectory logs for Phase 1.  
- Mini-projects ensure a **safe, reproducible foundation** for scaling to multi-joint hardware.  
- Always enforce **hardware/software safety limits**: voltage/current, joint motion, and E-stop overrides.