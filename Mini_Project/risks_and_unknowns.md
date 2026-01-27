# Mini-Projects – Risks & Unknowns (Phase 0)

## **General Risks**
- **Hardware damage:** Motors, sensors, or microcontroller could be damaged by overcurrent, incorrect wiring, or mechanical stress.  
- **Electrical shorts:** Loose wires, exposed connections, or misconnected power could cause shorts.  
- **Time overruns:** Spending too long optimizing or debugging can delay progression to Phase 1.  
- **Overcomplication:** Adding ML, full-arm testing, or complex algorithms distracts from skill-building objectives.  
- **Skill imbalance:** Focusing only on hardware or software may leave gaps in troubleshooting or understanding.

---

## **Mini-Project A – Single-Axis Smart Joint**
**Risks:**  
- PID tuning may initially cause oscillations or overshoot, potentially stressing the motor.  
- Sensor readings may be noisy, leading to confusing plots.  
- Incorrect wiring could damage the motor or microcontroller.  
- 3D printed mounts or brackets may break under torque if not secured properly.

**Unknowns / Uncertainties:**  
- Exact motor response characteristics (speed, torque curve, delay).  
- Sensor latency or measurement noise.  
- How the motor behaves under different load conditions.  
- Real-time performance of Python logging scripts.

---

## **Mini-Project B – Controller → Motor**
**Risks:**  
- Joystick commands may saturate motor response, causing jerky movement.  
- Communication latency between controller and microcontroller may affect smoothness.  
- Over-rotation or rapid motion could stress mechanical setup.  
- Logging failures may result in incomplete trajectory data.

**Unknowns / Uncertainties:**  
- Maximum achievable smoothness for human-in-the-loop control.  
- How the motor responds to rapid or non-linear joystick inputs.  
- Bluetooth/USB controller latency or compatibility issues.

---

## **Mini-Project C (Optional) – 2-Link Python Simulation**
**Risks:**  
- Poorly implemented FK/IK algorithms could give incorrect visualizations.  
- Over-reliance on simulation may give misleading intuition about hardware performance.  

**Unknowns / Uncertainties:**  
- Exact mapping from Python simulation to real hardware (timing, torque, backlash).  
- Potential numerical instabilities in IK solutions at edge-of-reach positions.  

---

## **Mitigation Strategies**
- Keep **currents and voltages within datasheet limits**.  
- Test one component at a time; never connect full system before verifying subsystems.  
- Stop mini-projects immediately once objectives are achieved.  
- Use logging and plotting to verify behavior instead of guessing.  
- Keep spare wires, sensors, and motor components for safe replacement.  
- Document all observations to reduce unknowns for Phase 1.  

---

**Notes:**  
- These risks and unknowns are strictly scoped to **Phase 0 / mini-projects**.  
- Purpose: make hardware/software interactions predictable, safe, and understandable.  
- Mini-projects are designed to reveal these unknowns early and safely, reducing risk in full arm assembly.  
