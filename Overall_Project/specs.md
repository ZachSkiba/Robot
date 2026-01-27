# 🤖 6-DOF Robotic Arm — Final Integrated Design Blueprint

---

## 1️⃣ Robot Specifications (Final)

| Parameter | Value / Design |
|---------|----------------|
| **Degrees of Freedom (DOFs)** | 6 (Base rotation, Shoulder, Elbow, Wrist pitch, Wrist yaw/roll, Gripper open/close) |
| **Link Length** | 20 cm each (3 main structural links) |
| **Material** | PETG Pro for links, housings, and 3D-printed gearboxes |
| **Max Payload** | ~1 kg |
| **Max Reach** | ~60 cm horizontal, ~60 cm vertical (approx.) |
| **Speed** | Shoulder/Elbow: 10–20°/s<br>Wrist: 30–60°/s<br>Gripper: fast (servo) |

---

## 2️⃣ Mechanical Layout — Joint by Joint

All motors are mounted **directly at their respective joints** (direct drive). Torque is increased locally using printed gearboxes. No remote actuation or cable drives.

| Joint | Motor | Gearbox | Placement | Notes |
|------|------|---------|-----------|------|
| **Base Rotation** | NEMA 17 (59 N·cm) | 10–15:1 PETG planetary/spur | Mounted on base plate | Rotates entire arm; supports distal joint torque |
| **Shoulder** | NEMA 17 (59 N·cm) | 15:1 PETG planetary | Mounted on shoulder pivot | Lifts entire arm + payload; most torque-critical joint |
| **Elbow** | NEMA 17 (59 N·cm) | 10–15:1 PETG planetary/spur | Mounted at elbow joint | Carries forearm + payload |
| **Wrist Pitch** | NEMA 17 (59 N·cm) | 5–10:1 PETG spur | Mounted on wrist plate | Low torque, higher speed |
| **Wrist Yaw / Roll** | NEMA 17 (59 N·cm) | 5–10:1 PETG spur | Mounted on wrist plate | Rotates end-effector; low torque |
| **Gripper Open/Close** | Micro servo | N/A | Mounted directly | Lightweight, fast |

**Notes:**
- Torque is multiplied locally via gearboxes
- No motors mounted remotely at the base
- Optional upgrade: dual steppers at shoulder/elbow for higher payload (not required for 1 kg)

---

## 3️⃣ Electronics & Control Architecture

### Control Topology
- **Arduino Mega**
  - Central coordinator
  - Computes forward & inverse kinematics (FK / IK)
  - Plans trajectories
  - Sends motion commands to ESP32s

- **3 × ESP32 Boards**
  - Distributed stepper controllers
  - Each controls 1–2 motors
  - Generates precise step pulses with microstepping

### Motor Drivers
- **A4988 or DRV8825** per stepper
- Configure for **1/16 or 1/32 microstepping** for smooth motion

### Power
- **12–24 V power supply**
- **6–8 A total**
- Supports 6 steppers + 1 servo

### Wiring Notes
- Keep stepper wires twisted and short
- Shield signal lines where possible
- Separate logic and motor power grounds carefully

**Why distributed control?**
- Prevents missed steps
- Enables smooth, synchronized 6-DOF motion
- Offloads timing-critical tasks from the Mega

---

## 4️⃣ Gearbox Recommendations

| Joint Group | Gear Ratio | Gear Type |
|------------|-----------|-----------|
| Shoulder & Elbow | 10–15:1 | Planetary or spur |
| Wrist | 5–10:1 | Spur |

**Design Guidelines:**
- PETG Pro is sufficient for **≤1 kg payload**
- Gear tooth thickness: **≥5 mm**
- Gear module: **≥2 mm**
- Lubricate with **PTFE grease**
- Minimize backlash, especially at shoulder and wrist joints

---

## 5️⃣ Payload & Torque Estimates (Approx.)

| Joint | Required Torque | Output Torque (with gearbox) | Feasible? |
|------|----------------|------------------------------|-----------|
| **Base** | ~400–500 N·cm | 590–885 N·cm | ✅ |
| **Shoulder** | ~800 N·cm | 750–880 N·cm | ✅ (upper limit) |
| **Elbow** | ~530 N·cm | 750–880 N·cm | ✅ |
| **Wrist** | ~150–200 N·cm | 300–400 N·cm | ✅ |
| **Gripper** | ~10–20 N·cm | N/A | ✅ |

✔ **1 kg max payload is fully achievable with this configuration**

Safety factor at shoulder/elbow: ~1.2×

---

## 6️⃣ Expected Performance

- **Max payload:** ~1 kg  
- **Reach:** ~60 cm horizontal / vertical  
- **Speed limits:**
  - Shoulder & Elbow: 10–20°/s (gear-limited)
  - Wrist joints: 30–60°/s
  - Gripper: fast servo response
- **Motion quality:** smooth, simultaneous multi-axis movement

---

## 7️⃣ Mechanical Design Tips

- Use **bearings at all joints** to reduce torque loss and wear
- Keep center of mass as close to the base as possible
- Reinforce gearbox housings — PETG flex can cause slippage
- Plan wrist cable routing carefully to avoid twisting during roll
- Test each joint individually before full assembly

---

## 8️⃣ Software Considerations

### Kinematics
- **Forward Kinematics:** standard 6-DOF serial chain
- **Inverse Kinematics:**
  - Use numeric solver (Jacobian pseudo-inverse)
  - 6-DOF redundancy allows wrist orientation optimization

### Motion Control
- Trajectory planning: move all joints simultaneously
- Use acceleration profiles to avoid skipped steps
- Microstepping improves smoothness and precision

---

## 9️⃣ Build & Integration Strategy

1. Print links, gearboxes, and housings in PETG Pro  
2. Assemble each joint: stepper + gearbox + bearings  
3. Wire steppers to ESP32s; Mega handles coordination  
4. Test torque, backlash, and range per joint  
5. Integrate gripper and servo control  
6. Run full-arm IK and payload tests  

---

## 💡 Bottom Line

This is a **realistic, DIY-buildable 6-DOF robotic arm**:

- **6 motors total** (5 × NEMA 17 + 1 servo)
- Direct-drive joints with printed gearboxes
- **~1 kg payload**
- PETG links and housings
- Arduino Mega + 3 ESP32s for distributed control

✅ Cost-effective  
✅ Mechanically simple  
✅ Strong resume-grade project  
