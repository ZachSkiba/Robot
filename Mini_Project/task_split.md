# Mini-Projects – Task Split (Phase 0)

## **Guiding Principles**
- Each mini-project is a **skill unlock**, not a full build.  
- Split tasks to maximize hands-on experience and learning.  
- Swap roles periodically to ensure both participants gain hardware and software familiarity.  
- Stop each mini-project immediately once objectives are met.  

---

## **Week 1 – Mini-Project A (Single-Axis Smart Joint)**

| Role | Tasks | Notes |
|------|-------|------|
| **Participant 1 – Hardware Lead** | - Mount motor and sensor on bracket/platform<br>- Wire motor to microcontroller and motor driver<br>- Verify motor responds to basic commands | Focus on wiring, assembly, and safe handling |
| **Participant 2 – Software Lead** | - Develop Python script to send motor commands<br>- Implement logging and plotting of sensor data<br>- Implement PID feedback loop | Focus on data visualization, debugging, tuning |
| **Both** | - Test joint motion<br>- Observe plots and adjust PID parameters<br>- Switch roles halfway to experience both hardware and software | Goal: joint reaches commanded positions; error plotted vs time |

**Completion Criteria:** Joint reaches commanded positions reliably; logging/plots confirm PID performance.  

---

## **Week 2 – Mini-Project B (Controller → Motor)**

| Role | Tasks | Notes |
|------|-------|------|
| **Participant 1 – Hardware Lead** | - Connect PS5 controller to microcontroller or Python interface<br>- Wire motor (reuse from Mini-Project A)<br>- Ensure power and signal integrity | Focus on safe connections and controller integration |
| **Participant 2 – Software Lead** | - Map joystick input to motor velocity/position<br>- Log joystick input and motor response<br>- Implement trajectory replay | Focus on human-in-the-loop control, data logging, and playback |
| **Both** | - Test smooth motion with joystick<br>- Replay recorded trajectories<br>- Analyze motor response to inputs | Goal: smooth joystick-controlled motion; trajectories replayable |

**Completion Criteria:** Motor responds smoothly; recorded motion can be replayed accurately.  

---

## **Mini-Project C (Optional) – 2-Link Python Simulation**

| Role | Tasks | Notes |
|------|-------|------|
| **Participant 1** | - Implement forward kinematics (FK) for 2-link arm<br>- Validate FK calculations | Focus on math and plotting correctness |
| **Participant 2** | - Implement inverse kinematics (IK)<br>- Validate IK solutions for reachable points | Focus on joint angle calculations and visualization |
| **Both** | - Create plots to visualize arm motion<br>- Compare FK vs IK results<br>- Adjust calculations as needed | Goal: FK + IK work correctly; plots match expected arm motion |

**Completion Criteria:** FK and IK calculations validated; visualization confirms correctness.  

---

## **Key Notes**
- Swap roles whenever possible to ensure both participants gain **hardware and software skills**.  
- Keep mini-projects **short and focused**: stop immediately after objectives are achieved.  
- Document all observations, plots, and tuning values to inform Phase 1 full-arm assembly.  
- Mini-projects prepare you for safe and confident transition to multi-joint hardware.  
