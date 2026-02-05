# Production-Grade 6-DOF Robot — Complete Setup, Rationale, and Runbook

Single document you can drop into your repo as `ARCHITECTURE.md` or `README.md`. Clean, exact, and actionable — all critical choices locked in.

## Summary

Use Teensy 4.1 + PlatformIO for all hard real-time motor control and ROS2 + Python (inside a local VS Code Dev Container) for planning, perception and supervision. Communicate via binary TCP (Ethernet recommended). Enforce safety in firmware and via a hardware safety relay.

## Table of Contents

- Goals & design rules
- Final system architecture
- Hardware & OS requirements
- Repo layout & dev environment (Dev Container)
- Firmware (PlatformIO) — timing and code skeleton
- PC side (ROS2 + Python) — nodes & roles
- Communication protocol — byte level (final)
- Control law & PID tuning method (per joint)
- Encoder sampling & filtering strategy
- Safety system — hardware + firmware rules
- Single-joint bring-up checklist (step-by-step)
- CI / workflow / tests
- Appendices: snippets, constants, and quick reference

---

## 1 — Goals & Design Rules

- **Separation:** Python/ROS2 never implements hard real-time loops. MCU (Teensy) does.  
- **Determinism:** MCU runs control at kHz; PC sends high-level joint targets.  
- **Safety first:** Hardware E-Stop with feedback, firmware watchdogs, and local joint limits.  
- **Reproducible environment:** Dev Container + PlatformIO + single GitHub repo.

---

## 2 — Final System Architecture

**PC (Ubuntu 22.04)**  
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
├─ Encoders (SPI AS5047P; fallback AS5600)
└─ Safety relay + E-Stop with feedback


---

## 3 — Hardware & OS Requirements

- **Host OS:** Ubuntu 22.04 LTS (bare-metal preferred)  
- **MCU:** Teensy 4.1 (600 MHz)  
- **Motor drivers:** TMC2209 for small motors; DM556 for high-torque NEMA23 (base/shoulder)  
- **Encoders:** Prefer SPI absolute (AS5047P); fallback I²C (AS5600)  
- **Network:** Ethernet recommended; USB CDC OK for bring-up  
- **Safety:** E-Stop relay with feedback contacts, inline fuse, decoupling caps, TVS diodes

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


### devcontainer/devcontainer.json

``json
{
  "name": "Robotics Arm",
  "image": "ros:humble",
  "runArgs": ["--net=host", "--device=/dev/ttyACM0"],
  "postCreateCommand": "pip install -r /workspaces/robot-arm/requirements.txt",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "platformio.platformio-ide",
        "ms-iot.vscode-ros"
      ]
    }
  }
}
docker/Dockerfile (minimal)
FROM ros:humble-ros-base-jammy
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-colcon-common-extensions \
    ros-humble-moveit \
    ros-humble-ros2-control \
    ros-humble-ros2-controllers \
    ros-humble-ros-gz \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /workspaces/robot-arm
5 — Firmware (PlatformIO) — Timing & Skeleton
platformio.ini
[env:teensy41]
platform = teensy
board = teensy41
framework = arduino
build_flags = -O3 -DUSB_SERIAL
lib_deps = teensyduino
monitor_speed = 115200
Timing Table
Task	Frequency
Encoder read	10 kHz
PID per joint	5 kHz
Safety checks	5 kHz
Comms RX/TX (serialize)	1 kHz
Trajectory buffer update	1 kHz
main.cpp Skeleton
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

## 6 — PC Side (ROS2 + Python) — Nodes & Responsibilities

- **trajectory_node:** Generate smooth joint trajectories with jerk/acceleration limits.  
- **kinematics_node:** Perform inverse kinematics and coordinate transforms (MoveIt2).  
- **hardware_interface_node:** Translate ROS2 commands ↔ MCU binary protocol; streams at 250–500 Hz.  
- **monitor_node:** Safety monitoring, logging, and GUI.

**ROS2 Rates:**  
- Controllers: 100–250 Hz  
- hardware_interface_node → MCU: 250–500 Hz

---

## 7 — Communication Protocol (Binary, Final)

- **Transport:** TCP/IP preferred; fallback USB CDC for bring-up  
- **Endianness:** Little-endian  
- **Timeout:** 20 ms → MCU disables motors; re-arm required  

### PC → MCU Packet (Command Packet)

| Field       | Size (bytes) |
|------------|-------------|
| header     | 2           |
| seq        | 2           |
| q_des[6]   | 24          |
| qd_des[6]  | 24          |
| flags      | 2           |
| crc32      | 4           |

**Total:** 58 bytes  
**Header value:** 0xA55A (uint16 little-endian)  

### MCU → PC Packet (State Packet)

| Field        | Size (bytes) |
|-------------|-------------|
| header      | 2           |
| seq         | 2           |
| q[6]        | 24          |
| qd[6]       | 24          |
| torque_est[6]| 24         |
| fault_flags | 2           |
| crc32       | 4           |

**Total:** 82 bytes  

**Rules:**  
- CRC32 over all fields except CRC itself; drop corrupted packets.  
- Fixed-size only, no variable-length messages.  
- Sequence numbers monotonic; large gaps → treated as packet loss.  
- MCU sends state at fixed intervals (250–500 Hz).  

---

## 8 — Control Law & PID Tuning (Per Joint)

**Discrete PID (Firmware, dt = 0.0002 s / 5 kHz)**

Let:

e[k] = q_des[k] - q_meas[k]
dt = 0.0002


Equations:

P = Kp * e[k]
I = I_prev + Ki * e[k] * dt
I = clamp(I, -Imax, +Imax)
D = Kd * (e[k] - e[k-1]) / dt
u[k] = P + I + D


- `u[k]` = target velocity (rad/s) → converted to step frequency with limits applied  
- **Safety clamps:**  
  - `u[k]` saturates to ±velocity_limit  
  - |u[k] - u[k-1]| ≤ accel_limit * dt  
- **I anti-windup:** Imax ≈ 10–20% of max command (adjust per joint)  

**Tuning Method (Frequency-Separated Manual)**

1. Set Ki = 0, Kd = 0  
2. Increase Kp until slight oscillation → reduce by 20–30%  
3. Add Kd to remove oscillation; ensure D does not dominate P  
4. Slowly add Ki to remove steady-state error  
5. Verify across step, ramp, sinusoidal trajectories  

---

## 9 — Encoder Sampling & Filtering (Exact)

- **Read raw encoder:** 10 kHz (hardware interrupt/DMA if available)  
- **Control loop uses:** filtered reading @ 5 kHz  

### First-Order IIR Filter

θ_filt[k] = α * θ_raw[k] + (1 - α) * θ_filt[k-1]


- Recommended α = 0.2–0.3 (reduces noise, <1 ms delay)  
- Velocity:  
ω[k] = (θ_filt[k] - θ_filt[k-1]) / dt

- **Do not differentiate raw data**; differentiate filtered angle only  

### Firmware Sanity Checks

- max_delta per sample → fault if exceeded  
- jump detection (sudden changes > threshold)  
- stale data detection (no updates)  
- encoder disconnect detection (I/O error)  

On any violation → disable joint, set fault flag, require manual reset

## 10 — Safety System (Hardware + Firmware)

### Hardware

- **E-Stop:** Wired to safety relay that cuts 24 V to motor drivers  
- **Feedback:** Relay must provide closed-loop feedback (aux contact) to MCU to verify E-Stop state  
- **Protection:** Inline fuses, TVS diodes on motor power lines, electrolytic caps per driver  
- **Filtering:** Ferrite beads on USB and power lines  

### Firmware

- **Watchdog timer:** Disables motor enables if firmware hangs  
- **Comm timeout (20 ms):** Disables motors  
- **Software limits:** Soft and hard limit switches for homing & protection  
- **Fault state machine:** Fault → latched disable → requires manual reset  

---

## 11 — Single-Joint Bring-Up Checklist

**Execute exactly as written**

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

### CI

- Build firmware in PlatformIO on each PR (do **not** auto-flash)  
- Run offline unit tests for trajectory generation & inverse kinematics  
- Run Gazebo integration tests with basic motions  
- Release: Tag firmware & container image; keep devcontainer.json and platformio.ini pinned  

### Daily Workflow

1. `git pull`  
2. Open VS Code → Reopen in Dev Container  
3. Build/flash firmware via PlatformIO  
4. Run ROS2 nodes (trajectory_node, hardware_interface_node)  
5. Execute single-joint tests → full-arm plan  

## 13 — Appendices / Quick Reference

### Constants & Recommended Starts

| Parameter               | Value / Notes                                  |
|-------------------------|-----------------------------------------------|
| `control_rate`          | 5000 Hz (dt = 0.0002 s)                       |
| `encoder_sample`        | 10000 Hz                                       |
| `comm_stream`           | 250–500 Hz                                     |
| `comm_timeout`          | 20 ms                                          |
| `IIR_alpha`             | 0.25 (start, tune 0.2–0.3)                    |
| `Imax`                  | ≈ 0.1 × u_max (tune per joint)                |
| `HEADER`                | 0xA55A (uint16 little-endian)                 |

---

### Example PC Bring-Up Commands

``bash
# Trajectory generation node
ros2 run arm_control trajectory_node

# Hardware interface node (with optional ROS2 args)
ros2 run arm_control hardware_interface_node --ros-args

Final Checklist Before Hardware

Ubuntu 22.04 installed on each teammate machine (or VM with USB passthrough tested)

Dev Container committed and verified (first build OK)

PlatformIO build succeeds locally and in CI

Ethernet communication validated (PC ↔ Teensy over TCP)

Safety relay installed with feedback loop to Teensy GPIO

Per-joint limits and E-Stop behavior tested in simulator

Single-joint PID tuning completed and documented for each joint

Optional Next Actions

Full main.cpp firmware skeleton implementing ISR loop, IIR filter, PID, CRC, and comm framing

Full hardware_interface_node Python/ROS2 implementation for 250–500 Hz streaming

Single-joint PID worksheet with example values and test script

Stack Summary & Data Flow Layer
Layer	Role
MATLAB / Python	High-level math, planning, trajectory generation
ROS2	Sends joint commands, collects state, logging
Gazebo Fortress	Physics simulation, robot visualization, collision checks
PlatformIO / Teensy	Low-level motor control, real-time loop

All simulations, PID tuning, logging, and motion planning can be done before hardware arrival

PID parameters and trajectories can be ported directly from simulation to MCU

# 6‑DOF Robot Arm — Complete Software Setup (Ubuntu 22.04 + ROS2 Humble + Gazebo Fortress + Python + MATLAB + PlatformIO)

## Goal

Prepare Ubuntu 22.04 LTS for full simulation, Python math layer, MATLAB integration, ROS2 Humble, Gazebo Fortress, and PlatformIO for MCU firmware. Hardware optional at this stage.

---

## 1 — Install Ubuntu 22.04 LTS

1. Download ISO: [Ubuntu 22.04 Desktop](https://ubuntu.com/download/desktop)  
2. Create bootable USB (Rufus on Windows recommended)  
3. Install Ubuntu  
   - Select "Normal installation"  
   - Check "Install third-party software for graphics" for NVIDIA/AMD drivers  
4. Reboot into Ubuntu  
⚠️ **Dual-boot recommended** for Gazebo GPU performance.

---

## 2 — Update System & Install Basics

``bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl build-essential cmake unzip udev
3 — Install Docker & Docker-Compose
sudo apt install -y docker.io docker-compose
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
Log out and back in (or reboot) to allow Docker usage without sudo

Test:

docker --version
docker run hello-world
4 — Install VS Code & Extensions
# Download .deb from https://code.visualstudio.com
sudo dpkg -i ~/Downloads/code*.deb
sudo apt -f install
Extensions to install:

PlatformIO IDE

Python

ROS

C/C++ (optional)

5 — Install PlatformIO & Configure USB Access
pip install platformio
Add udev rules for Teensy/ESP32:

curl -fsSL https://raw.githubusercontent.com/platformio/platformio-core/master/scripts/99-platformio-udev.rules | sudo tee /etc/udev/rules.d/99-platformio-udev.rules
sudo udevadm control --reload-rules
6 — Install ROS2 Humble
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository universe
sudo apt update
sudo apt install -y ros-humble-desktop
Setup ROS2 environment:

echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
Install build tools:

sudo apt install -y python3-colcon-common-extensions
Verify:

ros2 --version
7 — Install Gazebo Fortress + ROS-Gazebo Bridge
sudo apt install -y ros-humble-ros-gz
Test:

ros2 launch gazebo_ros empty_world.launch.py
ROS2 Humble + Gazebo Fortress officially supported

Enables joint control from ROS2 nodes

8 — Python Setup (Math Layer)
Ubuntu 22.04 default Python 3.10

Create virtual environment (mandatory):

python3 -m venv ~/robot-env
source ~/robot-env/bin/activate
Install packages:

pip install numpy==1.26.4 scipy pyserial pyyaml matplotlib
Always activate virtual environment before running simulations:

source ~/robot-env/bin/activate
9 — MATLAB Integration (Optional)
Install MATLAB 2023b or 2024a

Install MATLAB Engine API for Python:

cd /usr/local/MATLAB/R2024a/extern/engines/python
python3 setup.py install
Ensure Python version matches MATLAB-supported Python (3.10)

10 — ROS2 Workspace Setup
mkdir -p ~/robot-arm/ros_ws/src
cd ~/robot-arm/ros_ws
colcon build
source install/setup.bash
cd src
ros2 pkg create arm_control --build-type ament_python
11 — Docker + Dev Container (Optional, Recommended)
Dockerfile (docker/Dockerfile):

FROM ros:humble-ros-base-jammy
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-colcon-common-extensions \
    ros-humble-moveit \
    ros-humble-ros2-control \
    ros-humble-ros2-controllers \
    ros-humble-ros-gz \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /ros_ws
VS Code dev container (devcontainer/devcontainer.json):

{
  "name": "6DOF Robot Arm",
  "build": { "dockerfile": "../docker/Dockerfile" },
  "runArgs": ["--net=host", "--device=/dev/ttyACM0"],
  "postCreateCommand": "pip install -r requirements.txt",
  "customizations": {
    "vscode": {
      "extensions": ["ms-iot.vscode-ros","ms-python.python","platformio.platformio-ide"]
    }
  }
}
Open VS Code → Reopen in Container → all dependencies pre-installed

12 — PlatformIO MCU Workspace Setup
mkdir -p ~/robot-arm/firmware/src
cd ~/robot-arm/firmware
platformio.ini:

[env:teensy41]
platform = teensy
board = teensy41
framework = arduino
build_flags = -O3 -DUSB_SERIAL
lib_deps = teensyduino
monitor_speed = 115200
Add skeleton main.cpp implementing ISR loop, encoder filtering, PID, CRC, and communication framing

13 — Test the Stack
Python simulation:

python3 simulate_arm.py
Gazebo simulation:

ros2 launch gazebo_ros empty_world.launch.py
ROS2 nodes:

ros2 run arm_control trajectory_node
PlatformIO build:

pio run
Optional MATLAB engine test:

python3 test_matlab.py

## 14 — Complexity & Daily Workflow

| Aspect                        | Difficulty | Notes                                           |
|-------------------------------|-----------|------------------------------------------------|
| Ubuntu + dual-boot            | 6–7/10    | Shrinking Windows partitions; backup required |
| ROS2 Humble + Gazebo Fortress | 7/10      | Must install step-by-step; avoid Gazebo11     |
| Python + MATLAB integration   | 3–4/10    | Virtual environment critical                  |
| PlatformIO + Teensy USB       | 4–5/10    | udev rules; rarely adjusted after setup       |
| URDF / 3D model               | 8/10      | Requires accurate joint and collision definitions |
| Daily workflow                | 2–3/10    | Python scripts, ROS2 nodes, Gazebo mostly click-and-run |

**Takeaway:** First 1–2 days are heavy setup; afterward, simulations and logging are straightforward.

---

## 15 — Safety Considerations

### PC / Software Safety
- **Dual-boot:** safe once installed; risk during partitioning  
- **Docker Dev Container:** isolates system; crash? Delete container  
- **ROS2 network:** set custom `ROS_DOMAIN_ID` to isolate nodes  

### Robot / Hardware Safety
- Simulation-first workflow allows PID tuning and trajectory testing without motors  
- Port simulation parameters to hardware directly  

### Network / Data Safety
- ROS2 uses multicast by default → isolate via `ROS_DOMAIN_ID`  
- Avoid exposing topics on public networks  

### Team Collaboration
- Dev Container ensures identical environments  
- VS Code Live Share for real-time collaboration  
- Git for version control to prevent conflicts  

### Verdict
- **Effort:** Medium-high initially (7/10)  
- **Safety:** Very safe for PC and simulation; hardware risk eliminated if sim-first workflow used  
- **Collaboration:** Excellent with Dev Container + Git + Live Share  
- **Time saved:** Hundreds of hours by avoiding troubleshooting after first setup

