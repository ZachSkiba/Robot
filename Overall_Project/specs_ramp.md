# 🤖 6-DOF Robotic Arm — Final Integrated Design Blueprint (Rev 4.2)

**The "Tractor" Edition: Heavy Duty, High Durability, Spring-Assisted**

---

## 1️⃣ Robot Specifications

| Parameter | Value / Design |
|-----------|----------------|
| **Degrees of Freedom** | 6 (Base, Shoulder, Elbow, Wrist Pitch, Wrist Roll, Gripper) |
| **Kinematic Structure** | Standard Serial Linkage (Motor-on-Joint) |
| **Link Length** | 20–25 cm each (Upper Arm & Forearm) |
| **Materials** | PETG Pro (Gearboxes) + Aluminum Extrusion (Structure) |
| **Max Payload** | 1.5 kg (Rated safe load) |
| **Max Reach** | ~70 cm Vertical / ~60 cm Horizontal |
| **Speed Target** | 15–25°/s (Slow & Controlled) |
| **Smoothing Tech** | Geometric Gravity Compensation + Grease Damping |
| **Sensors** | Absolute Magnetic Encoders (AS5600) on major joints |

---

## 2️⃣ Mechanical Layout (The "Unbreakable" Stack)

**Core Strategy:** Replaced risky planetary gears with robust spur gears. Single strong motors only.  

| Joint | Motor | Transmission | Placement | Notes |
|-------|-------|-------------|----------|-------|
| Base | NEMA 23 (3.0 Nm) | 10:1 Planetary | Base Plate | Rotates the whole robot. Module 1.5 gears. |
| Shoulder | NEMA 23 (3.0 Nm) | 20:1 Compound Spur | Base Plate | CHANGED: Switched to Spur Gears for max durability. |
| Elbow | NEMA 17 (59 Ncm) | 20:1 Compound Spur | Upper Arm | Open Air Design for cooling. |
| Wrist P | NEMA 17 (59 Ncm) | 15:1 All-Gear | Forearm | UPDATED: 5:1 Box (on motor) → 3:1 Spur. |
| Wrist R | NEMA 11 (8 Ncm) | 5:1 Spur | Wrist Plate | Standardized motor size. |
| Gripper | NEMA 11 (8 Ncm) | Worm Gear | End Effector | Self-Locking. High grip force. |

---

## 3️⃣ Electronics & Control Architecture

**Core Strategy:** Hybrid Power with "Safety Patch" for RAMPS.  

| Component | Details | The Fix / Tuning |
|-----------|--------|----------------|
| Microcontroller | Arduino Mega 2560 | Use AccelStepper library. |
| Interface | RAMPS 1.4 (Modified) | CRITICAL: Desolder green power terminals. Solder XT60 wires directly. |
| Base Drivers | 2 × DM556 (External) | Set to 1600 steps/rev (1/8 microstepping). |
| Arm Drivers | 4 × TMC2209 (On Board) | Set to SpreadCycle Mode (not StealthChop). |
| Sensors | 2 × AS5600 (I2C) | Mount on Shoulder & Elbow shafts for absolute position. |
| Power Supply | 24V DC, 15A (360W) | Mandatory for NEMA 23 torque. |

---

## 4️⃣ Gearbox Strategy (Hardened)

**Critical Update:** Switched Shoulder **AND** Elbow to Spur Gears.  

| Joint | Ratio | Type | Module | Reinforcement Strategy |
|-------|-------|------|--------|----------------------|
| Base | 10:1 | Planetary | 1.5 | 100% Infill. Grease ports required. |
| Shoulder | 20:1 | Compound Spur | 1.5 | Metal Output Hub required. Open design. |
| Elbow | 20:1 | Compound Spur | 1.0 | Fan cooled. Open design. |
| Wrist P | 15:1 | Planetary+Spur | 0.8 | Attached to NEMA 17 face. |
| Gripper | 20:1 | Worm | 1.0 | Use Brass Worm if possible, or print & polish. |

---

## 5️⃣ Payload & Torque Verification

**Calculated with "Heavy Hand" (2.0kg tip mass) + Spring Assist.**  

| Joint | Load Torque (Raw) | Motor Output | Spring Assist | Safety Factor |
|-------|-----------------|-------------|---------------|---------------|
| Base | 7.0 Nm | 21.0 Nm | N/A | 3.0x ✅ |
| Shoulder | 12.8 Nm | 42.0 Nm | Optional | 3.3x ✅ |
| Elbow | 5.1 Nm | 8.4 Nm | +3.0 Nm Lift | ~5.0x ✅ (With springs) |
| Wrist P | 1.96 Nm | 6.1 Nm | N/A | 3.1x ✅ |

---

## 6️⃣ "Smoothing" Features to Design in CAD

1. **Geometric Gravity Assist (The Anti-Jerk System)**  
   - Shoulder Design: Place spring anchor high on the tower and offset behind arm axis.  
   - Elbow Design: Place hook so spring stretches max when arm extends.  
   - **Benefit:** Mechanically neutralizes gravity, preventing gear "clunk."

2. **Encoder Mounts**  
   - Design: Add flat spot or screw holes near Shoulder & Elbow axles to mount AS5600 PCB.  
   - **Benefit:** Allows the robot to "wake up" knowing where it is.

3. **Grease Injection Ports**  
   - Design: Add a 2mm hole on the side of Base & Wrist gearboxes.  
   - **Benefit:** Allows grease injection to create hydraulic damping.  

---

## 7️⃣ Build Phases

1. **Phase 1: The Foundation**  
   - Build Base (Planetary) & Shoulder (Spur).  
   - Solder XT60s to RAMPS.  

2. **Phase 2: The Arm**  
   - Build Elbow (Spur).  
   - Install AS5600 magnets with superglue (must be centered).  

3. **Phase 3: The Hand**  
   - Assemble Wrist/Gripper.  
   - Solder silicone wires.  

4. **Phase 4: The Suspension**  
   - Install arm. Attach springs.  
   - Tune tension until arm floats.  

---

## 💡 Final Verdict

Rev 4.2 is the **"Finished" Design for Builders**  

- Removes last weak link (Plastic Shoulder Planetary).  
- Adds last missing feature (Encoders).  
- Fixes fire hazard (RAMPS connectors).  

- PCB way has 6 axis control boards as well