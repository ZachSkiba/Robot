# 🤖 6-DOF Robotic Arm — Rev 5.2 Risk & Critical Issue Analysis

**The "Research" Edition**  
*Split-Brain, Hard Real-Time, Safety-Critical*

---

## 🔴 Killer Issues — Immediate Action Required

### Critical Issue 1: I²C Death Trap (Sensor Strategy)

- **Problem:** Standard I²C (AS5600) cannot reliably run alongside stepper motor cables. Stepper cables broadcast high EMI.  
- **Impact:** Teensy sees SDA low → constant timeouts → motion halts. Single-ended I²C is unusable for J1/J2/shoulder.  
- **Fix:** Use **Differential I²C** with PCA9615 or LTC4311 at both ends to convert SDA/SCL to differential signals immune to noise.  
- **Consequence if unaddressed:** Phase 1 single-encoder strategy fails immediately under load. ✅

---

### Critical Issue 2: Wrist Weakness (J5 NEMA 11)

- **Problem:** NEMA 11 with 5:1 spur is too weak (~0.5 Nm max) for a 2.0 kg payload.  
- **Physics Check:**  
  \[
  T = F \cdot r = 2\,\text{kg} \cdot 9.8\,\text{m/s²} \cdot 0.025\,\text{m} \approx 0.49\,\text{Nm}
  \]  
  Dynamic motion or inefficiency will exceed this, causing step loss or stall.  
- **Fix:** Upgrade to **NEMA 14** or increase gearing to 15:1–20:1. Aim for **safety factor ≥2×** (~1.0 Nm peak torque). ✅

---

### Critical Issue 3: Teensy 4.1 Voltage Tolerance

- **Problem:** Teensy 4.1 is strictly 3.3V I/O; many StepStick/TMC2209 boards default to 5V logic.  
- **Impact:** Feeding 5V into the Teensy (UART, TX/RX, fault pins) will destroy the MCU instantly.  
- **Fix:** Ensure all TMC2209 breakouts allow **V_IO = 3.3V** and connect exclusively to Teensy 3.3V rail. ✅

---

## 🔍 Minor Optimizations & Gotchas

- **Gravity Assist Spring (J3):** Linear spring cannot perfectly cancel sinusoidal gravity torque. Tune to shift peak load off motor at arm’s most extended position (~90°).  
- **Python Heartbeat Timing:** 100 ms is too aggressive on non-RTOS OS. Use 250–500 ms to prevent false E-Stops; Teensy handles immediate safety.  
- **Mechanical E-Stop Wiring:** Cut **24V power to drivers**, not just EN lines, to prevent “glitch” failure and ensure true safety compliance.

---

## 1️⃣ Mechanical

**Strengths:**

- Gravity-assist spring monitored → avoids catastrophic overload.  
- J3 flagged as critical load → encoder feedback on Phase 1 is good.

**Potential Issues:**

- Spring fatigue → sag and payload drift; no periodic calibration plan.  
- J3 torque margin → NEMA 17 + 25:1 + spring + backlash may reduce Phase 2 accuracy.  
- Cable drag/strain → drag chains defined, but no bend radius, tension, or expected cycle lifetime.

---

## 2️⃣ Electronics & Safety

**Strengths:**

- Power-dominant E-Stop, star grounding, autonomous motion disable.  
- Fault-driven driver disable with debouncing/filering.

**Potential Issues:**

- DM556T step-dir speed limits → skipped steps possible at high frequencies.  
- Fault-line filtering lacks defined thresholds → false/missed triggers possible.  
- Wi-Fi crosstalk → I²C single-ended encoders remain vulnerable.  
- Single active encoder in Phase 1 → J1/J2 slips undetected.

---

## 3️⃣ Motion & Software

**Strengths:**

- ISR-isolated, buffered motion pulses.  
- Teensy autonomous completion → safe if Python dies.

**Potential Issues:**

- Buffer length ≥500 ms may be insufficient for multi-joint, high-speed moves.  
- I²C reliability → bus lock or noise may trigger unplanned halts.  
- Heartbeat timeout 100 ms → too aggressive, risk of false inhibition.  
- Phase 2 S-Curve → no jerk limit, motor torque could saturate.

---

## 4️⃣ Sensors

- AS5600 I²C bus fine for single encoder, but multi-joint Phase 2 requires SPI/differential.  
- No explicit encoder error logging for research-grade data collection.

---

## 5️⃣ Build / HIL

- No automated verification for encoder vs step position; human inspection only → subtle misalignment risk.  
- E-Stop relay testing schedule not defined → mechanical contacts can degrade.

---

## ✅ Summary Table

| Category        | Risk / Issue                                                                                  |
|-----------------|------------------------------------------------------------------------------------------------|
| Mechanical      | Spring fatigue; J3 torque margin; cable drag/strain over time                                   |
| Electronics     | DM556T step speed limit; fault line noise; Wi-Fi crosstalk; single encoder Phase 1 slip         |
| Motion/Software | Buffer length too short; I²C blocking; heartbeat too sensitive; jerk not constrained            |
| Sensors         | AS5600 I²C multi-joint unreliable; no error logging                                            |
| Build/HIL       | No automated verification; E-Stop relay aging not tracked                                      |

---

## ⚠️ Verdict

- Architecture (Split-Brain, Teensy autonomous motion) is **excellent**.  
- Without addressing **I²C bus integrity, J5 torque, and Teensy voltage**, hardware failure is likely.  

**Immediate Actions Before Purchasing:**

1. Add PCA9615 or LTC4311 for all I²C encoders.  
2. Upgrade J5 to NEMA 14 or increase gear reduction (safety factor 2×).  
3. Verify TMC2209 V_IO → connect only to Teensy 3.3V.  
4. Tune gravity-assist spring; relax heartbeat to 250–500 ms.  
5. Ensure E-Stop cuts **24V power**, not just EN lines.
