# Phase 0 – Materials

Phase 0 is primarily **simulation, planning, and design verification**. Physical hardware is mostly optional, but some small components can help with reference testing.

---

## **Hardware (Minimal / Optional)**

| Item | Purpose | Notes |
|------|---------|-------|
| Laptop or Desktop | Run Python / simulation | Required |
| Notebook + Pen / Sketching Tools | Mechanical design, kinematics derivations | Required |
| Arduino / Teensy 4.1 | Optional microcontroller reference testing | Optional, can mimic step pulses or test small circuits |
| Stepper Motor + Driver (A4988, DRV8825, TMC2209) | Optional verification of motion concepts | Use only for small tests; main hardware comes in Phase 1 |
| USB Cable | Arduino / Teensy communication | Optional, needed only if testing microcontrollers |
| Basic Tools | Screwdrivers, pliers, multimeter | Optional reference hardware checks |

> **Note:** No heavy stepper motors, drivers, or mechanical assembly is required in Phase 0.

---

## **Software (Required)**

| Item | Purpose |
|------|---------|
| Python 3.10+ | Kinematics, trajectory planning, simulation |
| Libraries | `numpy` (numerical computing), `matplotlib` (plotting), `scipy` (optimization / IK) |
| Jupyter Notebook or VS Code | Interactive coding and visualization |
| Git | Version control |
| GitHub repository | Backup and collaboration |

---

## **Optional / Nice-to-Have Software**

| Item | Purpose |
|------|---------|
| MATLAB + Simulink | Cross-check kinematics, simulate arm dynamics |
| LaTeX / Markdown Editor | Professional documentation for reports / README |
| Blender / CAD software | Visualizing arm sketches, plotting trajectories, optional 3D simulation |

---

## **Consumables / Small Electronics (Optional for Reference)**

| Item | Purpose | Notes |
|------|---------|-------|
| Resistors / Capacitors | Noise suppression for test circuits | Only needed if testing stepper drivers on a small scale |
| Level shifters / Ferrite beads | Signal conditioning / EMI suppression | Useful for testing TMC2209 drivers safely |
| Breadboard | Rapid wiring & testing | Optional; small test circuits only |

> **Focus:** Phase 0 is **simulation, FK/IK derivations, trajectory planning, and logging**.  
> Physical components are **optional reference tools**, but documentation and sketches are **critical** for smooth Phase 1 hardware implementation.

---

## **Procurement Planning Notes (Phase 0 Relevance)**

- **Cart 1: Mini-Project Electronics Kit (~$213)**  
  - Useful for testing **single-axis stepper control, drivers, and encoders**.  
  - Can be partially skipped if only planning in software.

- **Cart 2: Heavy Metal / Mechanical Kit (~$378)**  
  - **Not needed in Phase 0** — only required for Phase 1 hardware assembly.

> **Key Takeaways:**  
> - Capacitors are critical for driver stability even in small test circuits.  
> - Ferrite beads help prevent USB/power EMI in simulation test setups.  
> - No heavy motors or drivers required yet — focus on planning, calculations, and software validation.