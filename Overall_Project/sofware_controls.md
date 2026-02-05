I'll update your ARCHITECTURE.md to incorporate the new plan (WSL2-first on ROG Flow X16, dual-boot as fallback for heavy GPU/real-time needs) and keep every original detail intact unless changed by the new plan. The document is split into three Markdown blocks so nothing is truncated — combine them locally into ARCHITECTURE.md if you want a single file.

BLOCK 1/3

# Production-Grade 6-DOF Robot — Complete Setup, Rationale, and Runbook

Single document you can drop into your repo as `ARCHITECTURE.md` or `README.md`. Clean, exact, and actionable — all critical choices locked in.

## Summary

Use Teensy 4.1 + PlatformIO for all hard real-time motor control and ROS2 + Python (inside a local VS Code Dev Container) for planning, perception and supervision. Communicate via binary TCP (Ethernet recommended). Enforce safety in firmware and via a hardware safety relay.

**New plan (Flow X16 / similar hybrid laptops):** Start WSL2-first on Windows (Ubuntu in WSL2 + VS Code WSL extension) for development, PlatformIO, and ROS2. Use USB passthrough (`usbipd`) for Teensy. Only move to dual-boot native Ubuntu 22.04 LTS (bare-metal) if you hit GPU/USB latency or Gazebo performance limits. For non-hybrid/standard dev machines, prefer bare-metal Ubuntu 22.04 LTS.

## Table of Contents

- Goals & design rules
- Final system architecture
- Hardware & OS requirements (includes WSL2 workflow)
- Repo layout & dev environment (Dev Container / WSL2 notes)
- Firmware (PlatformIO) — timing and code skeleton
- PC side (ROS2 + Python) — nodes & roles
- Communication protocol — byte level (final)
- Control law & PID tuning method (per joint)
- Encoder sampling & filtering strategy
- Safety system — hardware + firmware rules
- Single-joint bring-up checklist (step-by-step)
- CI / workflow / tests
- Appendices: snippets, constants, quick reference
- Software setup: WSL2-first steps and native Ubuntu instructions

---

## 1 — Goals & Design Rules

- **Separation:** Python/ROS2 never implements hard real-time loops. MCU (Teensy) does.  
- **Determinism:** MCU runs control at kHz; PC sends high-level joint targets.  
- **Safety first:** Hardware E-Stop with feedback, firmware watchdogs, and local joint limits.  
- **Reproducible environment:** Dev Container + PlatformIO + single GitHub repo.  
- **Laptop policy (new):** If using an ROG Flow X16 or similar hybrid laptop, use **WSL2-first** to avoid driver/UX breakage. Use native Ubuntu only when necessary.

---

## 2 — Final System Architecture

**PC (Ubuntu 22.04 or WSL2 Ubuntu)**  
├─ VS Code + Dev Container (ROS2, Python, PlatformIO)  
└─ ROS2 nodes (planning, MoveIt2, trajectory_node, hardware_interface_node)  
⇅ (Binary TCP, 250–500 Hz)

**Teensy 4.1 (PlatformIO firmware)**  
├─ Encoder reads @ 10 kHz  
├─ PID control @ 5 kHz  
├─ Step/timer hardware outputs  
└─ Safety checks @ 5 kHz

**Hardware**  
├─ Motor drivers (TMC2209 or DM556 per joint)  
├─ Encoders (prefer SPI AS5047P; AS5600 if necessary)  
└─ Safety relay + E-Stop with feedback

**Notes:** When running on Flow X16, the PC side can be either native Ubuntu (dual-boot) or Ubuntu in WSL2. Use WSL2 for day-to-day development; use native Ubuntu for GPU-heavy Gazebo runs or final hardware validation if USB/latency issues appear.

---

## 3 — Hardware & OS Requirements

- **Host OS (primary):**  
  - **Default** (team / lab machines): Ubuntu 22.04 LTS (bare-metal preferred).  
  - **Hybrid laptops (Flow X16):** WSL2 Ubuntu first; dual-boot native Ubuntu only if required.  
- **MCU:** Teensy 4.1 (600 MHz).  
- **Motor drivers:** TMC2209 for small motors; DM556 for high-torque NEMA23 (base/shoulder).  
- **Encoders:** Prefer SPI absolute (AS5047P). If AS5600 (I²C), follow I²C rules.  
- **Network:** Ethernet for final; USB CDC OK for bring-up (WSL2 supports USB passthrough via `usbipd`).  
- **Safety:** Safety relay with feedback contacts, physical E-Stop, inline fuse, decoupling caps and TVS diodes per cart.

**Important practical rule:** On Flow X16, keep Windows with Inventor installed; use WSL2 for the robotics stack until you prove you need native GPU/USB performance. This avoids "maintenance tax" from broken drivers (touchscreen, stylus, power mgmt).

---

## 4 — Repo Layout & Dev Container



robot-arm/
├── firmware/ # PlatformIO (Teensy)
│ ├── platformio.ini
│ └── src/
│ └── main.cpp
├── ros_ws/ # ROS2 workspace
│ └── src/
│ └── arm_control/
├── devcontainer/
│ └── devcontainer.json
├── requirements.txt
├── docker/
│ └── Dockerfile
└── README.md


### devcontainer/devcontainer.json (recommended)

- Works for native Ubuntu or Docker-in-WSL2. Keep `runArgs` conservative; in WSL2 Docker volumes and device access are done via WSL integration.

``json
{
  "name": "Robotics Arm",
  "image": "ros:humble",
  "runArgs": ["--net=host"],
  "postCreateCommand": "pip install -r /workspaces/robot-arm/requirements.txt",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "platformio.platformio-ide",
        "ms-iot.vscode-ros",
        "ms-vscode-remote.remote-wsl"
      ]
    }
  }
}


Note (WSL2): If using WSL2, enable Docker for WSL integration or use the Dockerfile and devcontainer.json to build within WSL2. For USB passthrough use usbipd to attach /dev/ttyACM0 into WSL and then pass that device into PlatformIO tasks in the WSL environment (no special --device needed for devcontainer in WSL since VS Code runs inside WSL).

5 — Firmware (PlatformIO) — Timing & Skeleton
platformio.ini
[env:teensy41]
platform = teensy
board = teensy41
framework = arduino
build_flags = -O3 -DUSB_SERIAL
lib_deps = teensyduino
monitor_speed = 115200

Timing Table (firmware tasks)
Task	Frequency
Encoder read	10 kHz
PID per joint	5 kHz
Safety checks	5 kHz
Comms RX/TX (serialize)	1 kHz
Trajectory buffer update	1 kHz
main.cpp skeleton (concept)
#include <Arduino.h>

void setup() {
    // init encoders, timers, comms, safety GPIOs
}

void loop() {
    // low-priority tasks: telemetry, non-critical housekeeping
}

ISR(control_timer) {
    // runs at 5 kHz
    read_encoders();
    compute_pid();
    update_step_outputs();
    run_safety_checks();
    handle_comm_tick(); // buffer RX/TX if necessary
}


Use hardware timers for step pulses.


---

**BLOCK 2/3**

``markdown
## 6 — PC Side (ROS2 + Python) — Nodes & Responsibilities

- **trajectory_node:** Generate smooth joint trajectories with jerk/acceleration limits.  
- **kinematics_node:** Perform inverse kinematics and coordinate transforms (MoveIt2).  
- **hardware_interface_node:** Translate ROS2 commands ↔ MCU binary protocol; streams at 250–500 Hz.  
- **monitor_node:** Safety monitoring, logging, GUI.

**ROS2 Rates:**  
- Controllers: 100–250 Hz  
- hardware_interface_node → MCU: 250–500 Hz

**WSL2 notes:** When running under WSL2, run `hardware_interface_node` inside WSL2 so it can access `/dev/ttyACM0` (attached via `usbipd`) or use TCP/Ethernet to the MCU. Use `ROS_DOMAIN_ID` to isolate networks.

---

## 7 — Communication Protocol (Binary, Final)

- **Transport:** TCP/IP preferred; fallback USB CDC for bring-up (works in WSL2 with `usbipd`)  
- **Endianness:** Little-endian  
- **Timeout:** 20 ms → MCU disables motors; re-arm required

### PC → MCU Packet (Command Packet)

| Field     | Size (bytes) |
|-----------|--------------|
| header    | 2            |
| seq       | 2            |
| q_des[6]  | 24           |
| qd_des[6] | 24           |
| flags     | 2            |
| crc32     | 4            |

**Total:** 58 bytes  
**Header value:** `0xA55A` (uint16 little-endian)

### MCU → PC Packet (State Packet)

| Field         | Size (bytes) |
|---------------|--------------|
| header        | 2            |
| seq           | 2            |
| q[6]          | 24           |
| qd[6]         | 24           |
| torque_est[6] | 24           |
| fault_flags   | 2            |
| crc32         | 4            |

**Total:** 82 bytes

**Rules:**  
- CRC32 over all fields except CRC field; drop corrupted packets.  
- Fixed-size only; no variable-length messages.  
- Sequence numbers monotonic; large gaps → packet loss treatment.  
- MCU sends state at fixed intervals (250–500 Hz).

---

## 8 — Control Law & PID Tuning (Per Joint)

**Discrete PID (dt = 0.0002 s / 5 kHz)**

Let:



e[k] = q_des[k] - q_meas[k]
dt = 0.0002


Equations:



P = Kp * e[k]
I = I_prev + Ki * e[k] * dt
I = clamp(I, -Imax, +Imax)
D = Kd * (e[k] - e[k-1]) / dt
u[k] = P + I + D


- `u[k]` = target velocity (rad/s) → converted to step frequency with velocity/accel limits applied.  
- **Safety clamps:**  
  - `u[k]` saturates to ±velocity_limit.  
  - |u[k] - u[k-1]| ≤ accel_limit * dt.  
  - I anti-windup: Imax ≈ 10–20% of max command (tune per joint).

**Tuning Method (Frequency-Separated Manual)**

1. Set Ki = 0, Kd = 0.  
2. Increase Kp until slight oscillation; reduce by 20–30%.  
3. Add Kd to remove oscillation.  
4. Slowly add Ki to remove steady-state error.  
5. Verify across step, ramp, sinusoidal trajectories.

---

## 9 — Encoder Sampling & Filtering (Exact)

- **Raw read:** 10 kHz (hardware interrupt/DMA if available).  
- **Control loop uses:** filtered reading @ 5 kHz.

### First-order IIR



θ_filt[k] = α * θ_raw[k] + (1 - α) * θ_filt[k-1]


- Recommended α = 0.2–0.3 (reduces noise, <1 ms delay).  
- Velocity:



ω[k] = (θ_filt[k] - θ_filt[k-1]) / dt


- **Do not differentiate raw data.** Differentiate filtered angle only.

### Firmware sanity checks

- max_delta per sample → fault if exceeded.  
- jump detection (sudden > threshold).  
- stale data detection (no updates).  
- encoder disconnect detection (I/O error).  

On any violation → disable joint, set fault flag, require manual reset.


BLOCK 3/3

## 10 — Safety System (Hardware + Firmware)

### Hardware

- **E-Stop:** Wired to safety relay that cuts 24 V to motor drivers.  
- **Feedback:** Relay must provide closed-loop feedback (aux contact) to MCU for verification.  
- **Protection:** Inline fuses, TVS diodes on motor power lines, electrolytic caps per driver.  
- **Filtering:** Ferrite beads on USB and power lines.

### Firmware

- **Watchdog:** Disables motor enables if firmware hangs.  
- **Comm timeout (20 ms):** Disables motors.  
- **Software limits:** Soft and hard limit switches for homing & protection.  
- **Fault state machine:** Fault → latched disable → manual reset.

---

## 11 — Single-Joint Bring-Up Checklist (Execute exactly)

1. Power off. Wire motor driver, encoder, limit switch, E-Stop relay. Verify wiring and fuses.  
2. Power on (no motor enabled). Verify MCU boots and sends heartbeat.  
3. Check encoder readings: run raw monitor at low speed; verify monotonic motion and no jumps.  
4. Homing: move slowly to limit switch; set q = home zero. Verify limit switch reporting.  
5. Enable motor at very low gain: Kp small, Ki=0, Kd=0. Apply small step (few degrees) at low velocity. Observe.  
6. Increase Kp until light oscillation, then reduce 20–30%. Record value.  
7. Increase Kd until oscillation gone. Record value.  
8. Add Ki slowly to remove steady-state error. Use very small increments; observe long time constants.  
9. Test trajectories: ramp, step, sinusoid. Monitor encoder vs command, current draw, temperature.  
10. Fault tests: cut comms, trigger limit switch, trip E-Stop → MCU must stop and latch.  
11. Document tuned gains and limits in repo.

---

## 12 — CI / Workflow / Tests

- **CI:** Build firmware (PlatformIO) on each PR (no auto-flash).  
- **Unit tests:** Trajectory generation & IK offline.  
- **Integration tests:** Gazebo simulation basic motions in CI.  
- **Release:** Tag firmware & container image; pin `devcontainer.json` & `platformio.ini`.

**Daily workflow**
``bash
git pull
Open VS Code → Reopen in Dev Container (or Remote-WSL)
Build/flash firmware via PlatformIO
Run ROS2 nodes (trajectory_node, hardware_interface_node)
Execute single-joint tests → full-arm plan

13 — Appendices / Quick Reference
Constants & Recommended Starts
Parameter	Value / Notes
control_rate	5000 Hz (dt = 0.0002 s)
encoder_sample	10000 Hz
comm_stream	250–500 Hz
comm_timeout	20 ms
IIR_alpha	0.25 (start, tune 0.2–0.3)
Imax	≈ 0.1 × u_max (tune per joint)
HEADER	0xA55A (uint16 little-endian)
Example PC Bring-Up Commands
# Trajectory generation node
ros2 run arm_control trajectory_node

# Hardware interface node (with optional ROS2 args)
ros2 run arm_control hardware_interface_node --ros-args

Final Checklist Before Hardware

Ubuntu 22.04 installed on each teammate machine (or WSL2 verified for Flow X16).

Dev Container committed and verified (first build OK).

PlatformIO build succeeds locally and in CI.

Ethernet comm validated (PC ↔ Teensy over TCP) or USB passthrough validated in WSL2.

Safety relay installed with feedback loop to Teensy GPIO.

Per-joint limits and E-Stop tested in simulator.

Single-joint tuning completed and documented for each joint.

14 — Complexity & Daily Workflow
Aspect	Difficulty	Notes
Ubuntu + dual-boot	6–7/10	Shrinking Windows partitions; backup required
ROS2 Humble + Gazebo Fortress	7/10	Must install step-by-step; avoid Gazebo11
Python + MATLAB integration	3–4/10	Virtual environment critical
PlatformIO + Teensy USB	4–5/10	udev rules; rarely adjusted after setup
URDF / 3D model	8/10	Requires accurate joint and collision definitions
Daily workflow	2–3/10	Python scripts, ROS2 nodes, Gazebo mostly click-and-run

Takeaway: First 1–2 days are heavy setup; afterward, simulations and logging are straightforward.

15 — Safety Considerations
PC / Software Safety

Dual-boot: safe once installed; risk during partitioning.

Docker Dev Container: isolates system; crash? Delete container.

ROS2 network: set custom ROS_DOMAIN_ID to isolate nodes.

Robot / Hardware Safety

Simulation-first workflow allows PID tuning and trajectory testing without motors.

Port simulation parameters to hardware directly.

Network / Data Safety

ROS2 uses multicast by default → isolate via ROS_DOMAIN_ID.

Avoid exposing topics on public networks.

Team Collaboration

Dev Container ensures identical environments.

VS Code Live Share for real-time collaboration.

Git for version control to prevent conflicts.

Verdict

Effort: Medium-high initially (7/10).

Safety: Very safe for PC and simulation; hardware risk eliminated if sim-first workflow used.

Collaboration: Excellent with Dev Container + Git + Live Share.

Time saved: Hundreds of hours by avoiding troubleshooting after first setup.

16 — Software Setup: WSL2-First (Flow X16) — Step-by-step (exact commands)

A. Enable WSL2 (PowerShell as Admin)

wsl --install
wsl --set-default-version 2


Reboot if prompted.

B. Install Ubuntu (22.04 recommended)

From Microsoft Store install Ubuntu 22.04 LTS, launch, create user, then:

sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential git curl python3-pip cmake udev


C. Install usbipd-win (Windows host) and attach Teensy

(PowerShell on Windows)

winget install --id=Microsoft.UsbIpdWin
usbipd list
# find Teensy busid and attach:
usbipd wsl attach --busid <BUSID>


Inside WSL:

ls /dev/ttyACM*
# should show /dev/ttyACM0
sudo usermod -aG dialout $USER
newgrp dialout


D. VS Code & WSL Integration

Install VS Code for Windows and extensions:

Remote - WSL

PlatformIO IDE

Python

ROS

Open VS Code → “Remote-WSL: New Window” → open repo inside WSL.

E. PlatformIO & udev rules inside WSL

pip install platformio
curl -fsSL https://raw.githubusercontent.com/platformio/platformio-core/master/scripts/99-platformio-udev.rules | sudo tee /etc/udev/rules.d/99-platformio-udev.rules
sudo udevadm control --reload-rules


Test:

pio boards teensy41


F. ROS2 Humble inside WSL

sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository universe
sudo apt update
sudo apt install -y ros-humble-desktop python3-colcon-common-extensions
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc


G. Docker / Dev Containers in WSL2

Enable Docker Desktop WSL2 integration on Windows, or install Docker inside WSL2.

Use devcontainer.json to open the repo in container inside WSL.

H. Latency notes (WSL2)

Typical USB latency with usbipd + WSL2 → ~0.5–2 ms round-trip.

PC loopback TCP latency inside WSL2 is sub-ms.

For most development and 250–500 Hz streaming, this is acceptable. Use native Ubuntu only if you require lower jitter or direct GPU for Gazebo.

17 — Final Checklist (WSL2-aware)

Confirm /dev/ttyACM0 inside WSL and PlatformIO can upload.

Confirm ros2 run arm_control hardware_interface_node inside WSL connects to MCU.

Run latency measurement (MCU timestamp → ROS2 read) and confirm < 2 ms typical.

Confirm Dev Container builds in WSL/Docker.

Simulate in Gazebo in WSL or Windows (if heavy rendering, prefer native Ubuntu).

Only move to dual-boot if you hit performance or USB/driver issues not solvable in WSL2.

Optional Next Actions

Full main.cpp firmware skeleton implementing ISR loop, IIR filter, PID, CRC, and comm framing.

Full hardware_interface_node Python/ROS2 implementation for 250–500 Hz streaming.
