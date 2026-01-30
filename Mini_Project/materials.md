# Mini-Projects – Materials List (Phase 0)

## **General / Shared Materials**
| Item | Quantity | Notes |
|------|---------|------|
| Teensy 4.1 or Arduino Mega / ESP32 | 1 | Microcontroller for Mini-Projects A & B (Teensy preferred for real-time control) |
| USB cable (Micro-USB / USB-C) | 1 | Connect microcontroller to computer for programming & logging |
| Breadboard | 1 | Temporary prototyping, wire connections |
| Jumper wires | 20–30 | Signal connections and sensor wiring (duplication recommended) |
| Computer with Python | 1 | Data logging, plotting, and controller interface |
| Python libraries | N/A | `matplotlib`, `pyserial`, `numpy` (plotting/logging) |
| Power supply (5–24V, 2–5A) | 1 | Motor supply; stable voltage required |
| Basic hand tools | As needed | Screwdriver, pliers, wire strippers, scissors |
| Multimeter | 1 | Debugging voltages/currents and continuity |

---

## **Mini-Project A – Single-Axis Smart Joint**
| Item | Quantity | Notes |
|------|---------|------|
| Stepper motor (NEMA 17 recommended) | 1 | High torque enough for joint test |
| Stepper driver (TMC2209, L298N, TB6600, etc.) | 1 | Silent driver preferred for PID tuning |
| Encoder (AS5600 or similar) | 1 | Absolute or incremental encoder for feedback |
| Mounting hardware | Few | Screws, nuts, washers |
| Small platform, bracket, or clamp | 1 | Hold motor securely for testing |
| Heat shrink tubing / insulation | As needed | Protect wiring and prevent shorts |
| Optional: 3D-printed mount | 1 | If no bracket is available; helps for stable testing |

---

## **Mini-Project B – Controller → Motor**
| Item | Quantity | Notes |
|------|---------|------|
| PS5 controller | 1 | Input device for human-in-the-loop testing |
| USB dongle or Bluetooth adapter | 1 | Connect PS5 controller to computer or Teensy/ESP32 |
| Same motor + driver from Mini-Project A | 1 | Hardware reuse encouraged |
| Wires & connectors | As needed | Connect controller input to logging/motor interface |
| Optional: Microcontroller shield / breakout | 1 | Simplifies wiring for sensor and driver connections |

---

## **Mini-Project C – 2-Link Arm Python Simulation (Optional / Virtual)**
| Item | Quantity | Notes |
|------|---------|------|
| Computer with Python | 1 | Simulation environment |
| Python libraries | N/A | `matplotlib`, `numpy` (FK/IK visualization) |
| Optional: Jupyter Notebook | 1 | Interactive simulation and plotting |
| Optional: 2D/3D plotting library | N/A | `plotly`, `pygame`, or `matplotlib.animation` for visualization |

---

## **Notes**
- Materials are scoped for **Phase 0 mini-projects only** — Phase 1 full-arm hardware is **not included**.  
- Mini-Project A and B **reuse the same motor, driver, and wiring** wherever possible.  
- Keep a few **spare wires, connectors, and resistors**; early testing often requires adjustments.  
- Tools listed are **hand tools only**; no heavy machinery required.  
- Optional 3D-printed mounts or brackets help, but simple platforms work for testing.  
- Consider adding **pull-up resistors (2.2 kΩ) and decoupling capacitors (100 µF)** for encoder noise suppression if using I²C encoders.