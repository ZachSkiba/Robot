# Mini-Projects – Risks & Unknowns (Phase 0)

## **General Risks**
- **Hardware damage:** Motors, drivers, sensors, or microcontrollers may fail due to overcurrent, mechanical stress, or miswiring.
- **Electrical hazards:** Shorts or incorrect power supply connections can damage components or create fire risk.
- **Time overruns:** Excessive debugging or optimization could delay Phase 1 hardware work.
- **Scope creep:** Introducing ML, full-arm testing, or complex algorithms distracts from skill-focused objectives.
- **Skill gaps:** Over-focusing on either hardware or software may leave blind spots in troubleshooting or integration.
- **Data integrity risk:** Logging failures or misconfigured plots may produce misleading conclusions.

---

## **Mini-Project A – Single-Axis Smart Joint**
**Risks:**  
- PID tuning can cause oscillation, overshoot, or motor stress.  
- Sensor noise may complicate data interpretation.  
- Miswiring could damage microcontroller, driver, or motor.  
- Brackets or mounts may fail under torque if not secured.  
- Stepper motors may skip steps if acceleration limits are exceeded.

**Unknowns / Uncertainties:**  
- Motor-specific response (torque curve, lag, thermal behavior).  
- Encoder latency, noise floor, or quantization effects.  
- Real-time performance of Python logging for high-frequency joint motion.  
- How software safety limits interact with physical system in unexpected scenarios.

---

## **Mini-Project B – Controller → Motor**
**Risks:**  
- Joystick commands may generate sudden jerks, saturating motor or driver.  
- Communication latency could degrade smoothness of human-in-the-loop motion.  
- Over-rotation or rapid inputs could damage mounts or connectors.  
- Logging failures may result in incomplete trajectories or misdiagnosed errors.  

**Unknowns / Uncertainties:**  
- Max achievable smoothness given controller, microcontroller, and motor hardware.  
- Motor response to rapid, non-linear, or repeated joystick inputs.  
- Latency and compatibility variability of PS5 controller via USB/Bluetooth.  
- Safety system interaction under continuous or conflicting commands.

---

## **Mini-Project C (Optional) – 2-Link Python Simulation**
**Risks:**  
- Incorrect FK/IK implementation may produce misleading motion visualization.  
- Over-reliance on simulation could give false confidence for hardware behavior.  

**Unknowns / Uncertainties:**  
- Translation of Python simulation to real hardware: torque, backlash, timing, and limits.  
- Numerical instabilities at edge-of-reach positions or singularities in IK.  
- Real-world limits (motor torque, thermal effects, joint friction) not captured in simulation.

---

## **Mitigation Strategies**
- Enforce **datasheet limits** for current, voltage, and torque.  
- Test each subsystem independently before full system execution.  
- Stop mini-projects immediately once objectives are met; avoid endless optimization.  
- Use logging, plots, and repeatable scripts to verify behavior quantitatively.  
- Maintain spare wires, sensors, and motor components.  
- Document all findings to reduce unknowns and support Phase 1.  
- Include software safety checks: soft stops, acceleration/velocity limits, simulated or real E-stop override.  

---

**Notes:**  
- Risks and unknowns are scoped **strictly to Phase 0 / mini-projects**.  
- Purpose: reveal unknowns early, minimize hardware/software surprises, and build predictable, safe systems.  
- Early identification of these factors ensures Phase 1 full-arm integration is **low-risk and reproducible**.