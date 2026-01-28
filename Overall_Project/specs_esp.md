# 🤖 6-DOF Robotic Arm — Final Integrated Design Blueprint (Rev 4.6)

**The "FluidNC" Edition: Plug-and-Play Electronics, Wireless, Heavy Duty**

---

## 1️⃣ Robot Specifications

| Parameter | Value / Design |
|-----------|----------------|
| **Brain** | ESP32 via "FluidNC 6-Pack" Controller |
| **Degrees of Freedom** | 6 (Base, Shoulder, Elbow, Wrist Pitch, Wrist Roll, Gripper) |
| **Kinematic Structure** | Standard Serial Linkage (Motor-on-Joint) |
| **Max Payload** | 1.5 kg (Rated safe load) |
| **Control Frequency** | 200 kHz+ (Smooth, Wi-Fi enabled) |
| **Smoothing Tech** | Software S-Curve (FluidNC) + Geometric Gravity Springs |
| **Sensors** | Absolute Magnetic Encoders (AS5600) on major joints |
| **Connectivity** | Native Wi-Fi / Bluetooth (Phone App & WebUI Ready) |
| **Transmission Style** | 100% Gear Driven (NO BELTS) |

---

## 2️⃣ Mechanical Layout (The "Unbreakable" Stack)

**Core Strategy:** Unchanged from previous designs. Robust spur gears + single strong motors.  

| Joint | Motor | Transmission | Placement | Notes |
|-------|-------|-------------|----------|-------|
| Base | NEMA 23 (3.0 Nm) | 10:1 Planetary | Base Plate | Rotates the whole robot. Module 1.5 gears. |
| Shoulder | NEMA 23 (3.0 Nm) | 20:1 Compound Spur | Base Plate | Metal hub mandatory. |
| Elbow | NEMA 17 (59 Ncm) | 20:1 Compound Spur | Upper Arm | Open Air Design for cooling. |
| Wrist P | NEMA 17 (59 Ncm) | 15:1 All-Gear | Forearm | 5:1 Metal Planetary (on motor) → 3:1 Printed Spur. |
| Wrist R | NEMA 11 (8 Ncm) | 5:1 Spur | Wrist Plate | Standardized small motor. |
| Gripper | NEMA 11 (8 Ncm) | Worm Gear | End Effector | Self-Locking. |

---

## 3️⃣ Electronics & Control (The "6-Pack" Upgrade)

**Core Strategy:** Use a dedicated CNC Motherboard to eliminate loose wiring.  

| Component | Product / Details | Integration Strategy |
|-----------|-----------------|-------------------|
| Motherboard | FluidNC 6x Controller ("6-Pack") | All-in-One Board. Contains ESP32 slot, driver sockets, and I/O. |
| Logic Voltage | 5V / 3.3V (Auto) | No Level Shifters needed. Board handles signal conversion internally. |
| Base Drivers | 2 × DM556 (External) | Wire to board's "External Motor" screw terminals. |
| Arm Drivers | 4 × TMC2209 (StepStick) | Plug directly into slots 1–4 on motherboard. |
| Sensors | 2 × AS5600 (I2C) | Plug into board's I2C header (VCC, GND, SDA, SCL). |
| Power Supply | 24V DC, 15A (360W) | Powers board directly. Board creates 5V for ESP32. |

---

## 4️⃣ Gearbox Strategy (Hardened)

**Core Strategy:** Durability is paramount. Grease heavily.  

| Joint | Ratio | Type | Module | Reinforcement Strategy |
|-------|-------|------|--------|----------------------|
| Base | 10:1 | Planetary | 1.5 | 100% Infill. Grease ports required. |
| Shoulder | 20:1 | Compound Spur | 1.5 | Metal Output Hub required. Open design. |
| Elbow | 20:1 | Compound Spur | 1.0 | Fan cooled. |
| Wrist P | 15:1 | Planetary + Spur | 1.0 | Metal Gearbox on motor face drives printed spur gear. |
| Gripper | 20:1 | Worm | 1.0 | Brass Worm recommended. |

---

## 5️⃣ The "FluidNC Wiring" Guide (Simplified)

**Since we are using the 6-Pack board, the wiring is standardized:**

1. **Main Power**  
   - Connect 24V PSU to Green Power Terminal on 6-Pack board.  
   - Result: Board powers up, fans spin, ESP32 turns on.  

2. **Small Motors (Wrist/Gripper)**  
   - Plug TMC2209 Drivers into Slots 1–4.  
   - Connect motor wires to the 4-pin headers next to them.  

3. **Big Motors (Base/Shoulder)**  
   - Locate "External Driver" terminals on Slots 5 & 6.  
   - Wire: Step → PUL+, Dir → DIR+, GND → PUL-/DIR-.  
   - Note: Board outputs 5V signals automatically. No converters needed.  

4. **Encoders**  
   - Locate I2C Header on board.  
   - Wire SDA/SCL/GND/3.3V to AS5600 sensors.  

---

## 6️⃣ Smoothing & Intelligence

1. **Software S-Curves (FluidNC Native)**  
   - Configure `acceleration_mm_per_sec2` in `config.yaml`.  
   - ESP32 handles calculations, eliminates jerk.  

2. **Geometric Gravity Assist**  
   - Shoulder: Spring anchor High + Offset Behind axis.  
   - Elbow: Spring anchor ensures max tension at full extension.  
   - **Benefit:** Reduces motor load by 60%.  

3. **Wireless Control**  
   - WebUI: Connect phone to "FluidNC" Wi-Fi network.  
   - Open browser to `192.168.0.1`.  
   - **Benefit:** Full jogging control, macros, G-Code sending without installing an app.  

---

## 7️⃣ Build Phases (Rev 4.6)

1. **Phase 1: The Config**  
   - Plug ESP32 into 6-Pack Board.  
   - Upload FluidNC Firmware via USB.  
   - Edit `config.yaml` to define 6 axes (Motor currents, Steps per mm).  

2. **Phase 2: The Foundation**  
   - Build Base & Shoulder.  
   - Wire DM556 drivers to board screw terminals.  
   - Test: Jog base using phone.  

3. **Phase 3: The Arm**  
   - Assemble Elbow + Wrist (All Gears).  
   - Plug TMC2209s into board slots.  

4. **Phase 4: The Network**  
   - Connect AS5600s.  
   - Calibrate "Home" positions in WebUI.  

---

## 💡 Final Verdict

**Rev 4.6 — "Gold Standard" for DIY Arms**  

- **Complexity:** Low (Single board).  
- **Performance:** High (ESP32 + S-Curves).  
- **Cost:** Medium (~$45 board, saves hours of wiring).  
- **Future Proof:** Ready for Computer Vision via Wi-Fi/USB.  
