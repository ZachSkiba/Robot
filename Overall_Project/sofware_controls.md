Production-Grade 6-DOF Robot — Complete Setup, Rationale, and Runbook

Single document you can drop into your repo as ARCHITECTURE.md or README.md. Clean, exact, and actionable — all critical choices locked in.

Summary (one-line)

Use Teensy 4.1 + PlatformIO for all hard real-time motor control and ROS2 + Python (inside a local VS Code Dev Container) for planning, perception and supervision. Communicate via binary TCP (Ethernet recommended). Enforce safety in firmware and via a hardware safety relay.

Table of Contents

Goals & design rules

Final system architecture

Hardware & OS requirements

Repo layout & dev environment (Dev Container)

Firmware (PlatformIO) — timing and code skeleton

PC side (ROS2 + Python) — nodes & roles

Communication protocol — byte level (final)

Control law & PID tuning method (per joint)

Encoder sampling & filtering strategy

Safety system — hardware + firmware rules

Single-joint bring-up checklist (step-by-step)

CI / workflow / tests

Appendices: snippets, constants, and quick reference

1 — Goals & Design Rules (non-negotiable)

Separation: Python/ROS2 never implements hard real-time loops. MCU (Teensy) does.

Determinism: MCU runs control at kHz; PC sends high-level joint targets.

Safety first: Hardware E-Stop with feedback, firmware watchdogs, and local joint limits.

Reproducible environment: Dev Container + PlatformIO + single GitHub repo.

2 — Final System Architecture (locked)
PC (Ubuntu 22.04)
 ├─ VS Code + Dev Container (ROS2, Python, PlatformIO)
 └─ ROS2 nodes (planning, MoveIt2, trajectory_node, hardware_interface_node)
     ⇅  (Binary TCP, 250–500 Hz)
Teensy 4.1 (PlatformIO firmware)
 ├─ Encoder reads @ 10 kHz
 ├─ PID control @ 5 kHz
 ├─ Step/timer hardware outputs
 └─ Safety checks @ 5 kHz
Hardware
 ├─ Motor drivers (TMC2209 or DM556 per joint)
 ├─ Encoders (prefer SPI AS5047P; AS5600 if necessary)
 └─ Safety relay + E-Stop with feedback
3 — Hardware & OS (required)

Host OS: Ubuntu 22.04 LTS (bare metal preferred).

MCU: Teensy 4.1 (600 MHz).

Motor drivers: TMC2209 for small motors; DM556 for high-torque NEMA23 (base/shoulder).

Encoders: Prefer SPI absolute (AS5047P). If AS5600 (I²C), follow I²C rules below.

Network: Ethernet for final; USB CDC OK for bring-up.

Safety: Safety relay with feedback contacts, physical E-Stop, inline fuse, decoupling caps and TVS diodes as listed in your cart.

4 — Repo layout & Dev Container (exact)
robot-arm/
├── firmware/                 # PlatformIO (Teensy)
│   ├── platformio.ini
│   └── src/
│       └── main.cpp
├── ros_ws/                   # ROS2 workspace
│   └── src/
│       └── arm_control/
├── devcontainer/
│   └── devcontainer.json
├── requirements.txt
├── docker/
│   └── Dockerfile
└── README.md
devcontainer/devcontainer.json (final)
{
  "name": "Robotics Arm",
  "image": "ros:humble",
  "runArgs": ["--net=host", "--device=/dev/ttyACM0"],
  "postCreateCommand": "pip install -r /workspaces/robot-arm/requirements.txt",
  "customizations": {
    "vscode": {
      "extensions": ["ms-python.python","platformio.platformio-ide","ms-iot.vscode-ros"]
    }
  }
}
devcontainer/Dockerfile (minimal)

Use ros:humble base and install python3-pip, colcon and moveit as needed (you already have earlier content). Set WORKDIR /workspaces/robot-arm.

5 — Firmware (PlatformIO) — timing & skeleton
PlatformIO install
sudo apt install python3-pip
pip install platformio
platformio.ini (Teensy)
[env:teensy41]
platform = teensy
board = teensy41
framework = arduino
build_flags =
  -O3
  -DUSB_SERIAL
lib_deps =
  teensyduino
Timing table (firmware tasks)
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
ISR(control_timer) { // runs at 5 kHz
  read_encoders();
  compute_pid();
  update_step_outputs();
  run_safety_checks();
  handle_comm_tick(); // buffer RX/TX if necessary
}

Use hardware timers for step pulses.

6 — PC side (ROS2 + Python) — nodes & responsibilities

trajectory_node: Generate smooth joint trajectories (jerk/acceleration limits).

kinematics_node: Inverse kinematics, coordinate transforms (MoveIt2).

hardware_interface_node: Translate ROS2 commands ↔ binary protocol to MCU; run at 250–500 Hz.

monitor_node: Safety monitoring, logging, GUI.

Rates: ROS2 controllers at 100–250 Hz; hardware_interface_node streams to MCU at 250–500 Hz.

7 — Communication protocol (binary, final)

Transport: TCP/IP (prefer), fallback USB CDC for bring-up.
Endianness: Little-endian.
Timeout: 20 ms — on timeout, MCU disables motors; re-arm required.

PC → MCU (Command packet)

uint16_t header = 0xA55A (2 bytes)

uint16_t seq (2 bytes)

float q_des[6] (6 × 4 = 24 bytes)

float qd_des[6] (24 bytes)

uint16_t flags (2 bytes)

uint32_t crc32 (4 bytes)
Total: 58 bytes

MCU → PC (State packet)

uint16_t header (2)

uint16_t seq (2)

float q[6] (24)

float qd[6] (24)

float torque_est[6] (24)

uint16_t fault_flags (2)

uint32_t crc32 (4)
Total: 82 bytes

CRC: CRC32 over all fields prior to CRC field. Drop corrupted packets and raise comm error counters.

Packet rules

Fixed-size only. No variable-length messages.

Sequence number monotonic; if sequence gap too large, MCU treats as packet loss.

MCU sends state at fixed interval (e.g., 250–500 Hz).

8 — Control law & PID tuning (per joint) — exact math and method
Discrete PID (firmware, dt = 1/5000 = 0.0002 s)

Let:

e[k] = q_des[k] - q_meas[k]

dt = 0.0002

Equations:

P = Kp * e[k]
I = I_prev + Ki * e[k] * dt
I = clamp(I, -Imax, +Imax)
D = Kd * (e[k] - e[k-1]) / dt
u[k] = P + I + D

u[k] is target velocity (rad/s) → converted to step frequency with velocity limits and accelerations applied.

Safety clamps (mandatory)

u[k] saturate to ±velocity_limit

|u[k] - u[k-1]| <= accel_limit * dt (apply acceleration limiting)

I anti-windup clamp Imax ≈ 10–20% of maximum command magnitude (adjust per joint)

Tuning method (Frequency-Separated Manual Tuning)

Set Ki = 0, Kd = 0. Increase Kp until slight oscillation; then reduce Kp by 20–30%.

Add Kd to remove oscillation and damp; Kd should not dominate P.

Add Ki slowly to remove steady-state error, with strong anti-windup and small Ki.

Verify across trajectories (step, ramp, sinusoidal).

Use single-joint bring-up procedure below.

9 — Encoder sampling & filtering (exact)
Read & sample

Read raw encoder at 10 kHz (hardware interrupt or DMA where possible).

Control loop uses filtered reading at 5 kHz.

Filter (First-order IIR)

For angle θ:

θ_filt[k] = α * θ_raw[k] + (1 - α) * θ_filt[k-1]

Recommended α = 0.2–0.3 → reduces noise while keeping <1 ms delay.

Velocity
ω[k] = (θ_filt[k] - θ_filt[k-1]) / dt

Do not differentiate raw data. Differentiate filtered angle only.

Sanity checks (firmware must implement)

max_delta = max plausible change per sample (if exceeded → fault)

jump detection (sudden > threshold)

stale data detection (no updates)

encoder disconnect detection (I/O error)

On any sanity violation: disable joint, set fault flag, require reset.

10 — Safety system (hardware + firmware)
Hardware

E-Stop wired to safety relay that cuts 24 V to motor drivers.

Relay must provide closed-loop feedback (aux contact) to MCU so MCU can verify E-Stop state.

Inline fuses, TVS diodes on motor power lines, and electrolytic capacitors per driver (per your cart rules).

Ferrite beads on USB and power lines.

Firmware

Watchdog timer that disables motor enables if firmware hangs.

Comm timeout (20 ms) → disable motors.

Software soft limits and hard limit switches (wired) for homing & protection.

Fault state machine: fault -> latched disable -> require manual reset.

11 — Single-joint bring-up checklist (execute exactly)

Power off. Wire motor driver, encoder, limit switch, E-Stop relay. Verify wiring and fuses.

Power on (no motor enabled). Verify MCU boots and sends heartbeat.

Check encoder readings: run encoder monitor (raw) at low speed; verify monotonic motion and no jumps.

Homing: move slowly to limit switch; set q=home zero. Verify limit switch reporting.

Enable motor at very low gain: set Kp small, Ki=0, Kd=0. Apply small step (few degrees) at low velocity. Observe response.

Increase Kp until light oscillation, then reduce 20–30%. (Record value)

Increase Kd until oscillation gone. (Record value)

Add Ki slowly to remove steady error. Use very small increments and observe long time constants.

Test trajectories: ramp, step, sinusoid. Monitor encoder vs command, current draw, temperature.

Fault tests: cut comms, trigger limit switch, trip E-Stop — MCU must stop and latch.

Document tuned gains and limits in repo.

12 — CI / Workflow / tests

CI: Build firmware in CI (PlatformIO) on each PR; do not auto-flash.

Unit tests: Offline tests for trajectory generation and IK.

Integration tests: Simulation (Gazebo) CI job that runs basic motions.

Release: Tag firmware and container image. Keep devcontainer.json and platformio.ini pinned.

Daily workflow:

git pull

Open pc/ in VS Code → Reopen in Container

Build/flash firmware via PlatformIO extension

Run ROS nodes and hardware_interface_node

Execute single-joint tests then full-arm plan

13 — Appendices / Quick reference
Constants & recommended starts

control_rate = 5000 Hz (dt = 0.0002 s)

encoder_sample = 10000 Hz

comm_stream = 250–500 Hz

comm_timeout = 20 ms

IIR_alpha = 0.25 (start)

Imax ≈ 0.1 * u_max (tune per joint)

Packet header value

HEADER = 0xA55A (uint16 little-endian)

Example PC bring-up commands

ros2 run arm_control trajectory_node

ros2 run arm_control hardware_interface_node --ros-args (node-specific args for IP/port)

Final checklist before you move to hardware

 Ubuntu 22.04 installed on each teammate machine (or VM with USB passthrough tested)

 Dev container committed and verified (first build OK)

 PlatformIO build succeeds locally and in CI

 Ethernet comm channel validated in loopback (PC ↔ Teensy over TCP)

 Safety relay installed with feedback loop to Teensy GPIO

 Per-joint limits and emergency stop behavior tested in simulator

 Single-joint tuning completed and documented for each joint

Next actions I can produce immediately (pick any)

Full main.cpp firmware skeleton implementing ISR loop, IIR filter, PID, CRC, and comm framing.

Full hardware_interface_node Python/ROS2 implementation that packs/unpacks the binary protocol and streams at 250–500 Hz.

Single-joint PID worksheet (table + example values + test script).


Got it. I’ve reviewed your combined guide and cleaned it up into a fully corrected, step-by-step, Ubuntu 22.04 + ROS2 Humble + Gazebo Fortress + PlatformIO + Python + MATLAB setup guide that avoids the pitfalls with Gazebo11 and ensures a smooth simulation workflow. I also clarified virtual environments, udev rules for PlatformIO, and the ROS-Gazebo bridge.

Here’s the fixed, production-ready software setup guide:

6‑DOF Robot Arm — Complete Software Setup (Corrected)

Goal: Prepare Ubuntu 22.04 LTS for full simulation (ROS2 Humble, Gazebo Fortress, Python, MATLAB, PlatformIO). No hardware needed yet.

1. Install Ubuntu 22.04 LTS

Download ISO: https://ubuntu.com/download/desktop

Create a bootable USB (Rufus on Windows).

Install Ubuntu (dual-boot recommended).

Select "Normal installation."

Check "Install third-party software for graphics" for NVIDIA/AMD drivers.

Reboot into Ubuntu.

⚠️ Dual-boot is strongly recommended — Gazebo requires direct GPU access for smooth 3D simulation.

2. Update System & Install Basics
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl build-essential cmake unzip udev
3. Install Docker & Docker-Compose
sudo apt install -y docker.io docker-compose
sudo systemctl enable --now docker
sudo usermod -aG docker $USER

Log out and back in (or reboot) to allow Docker usage without sudo.

Test Docker:

docker --version
docker run hello-world
4. Install VS Code & Extensions

Download .deb from https://code.visualstudio.com

Install:

sudo dpkg -i ~/Downloads/code*.deb
sudo apt -f install

Open VS Code → Install Extensions:

PlatformIO IDE

Python

ROS

C/C++ (optional)

5. Install PlatformIO & Configure USB Access

Install PlatformIO IDE inside VS Code.

Add udev rules (required for Teensy/ESP32 upload):

curl -fsSL https://raw.githubusercontent.com/platformio/platformio-core/master/scripts/99-platformio-udev.rules | sudo tee /etc/udev/rules.d/99-platformio-udev.rules
sudo udevadm control --reload-rules
6. Install ROS2 Humble
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository universe
sudo apt update
sudo apt install -y ros-humble-desktop

Setup ROS2 environment automatically:

echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc

Install build tools:

sudo apt install -y python3-colcon-common-extensions

Verify:

ros2 --version
7. Install Gazebo Fortress + ROS-Gazebo Bridge

ROS2 Humble is officially supported with Gazebo Fortress, not Gazebo11.

sudo apt install -y ros-humble-ros-gz

Test Gazebo:

ros2 launch gazebo_ros empty_world.launch.py

This installs Fortress + ROS-Gazebo bridge, allowing ROS2 nodes to control joints.

8. Python Setup (Math Layer)

Ubuntu 22.04 system Python is 3.10.

Create virtual environment (mandatory):

python3 -m venv ~/robot-env
source ~/robot-env/bin/activate

Install required packages:

pip install numpy==1.26.4 scipy pyserial pyyaml matplotlib

Always source ~/robot-env/bin/activate before running Python simulations.

9. MATLAB Integration (Optional)

Install MATLAB 2023b or 2024a for Ubuntu.

Install MATLAB Engine API for Python:

cd /usr/local/MATLAB/R2024a/extern/engines/python
python3 setup.py install

Ensure Python version matches MATLAB-supported Python (3.10 on Ubuntu 22.04).

10. ROS2 Workspace Setup
mkdir -p ~/robot-arm/ros_ws/src
cd ~/robot-arm/ros_ws
colcon build
source install/setup.bash
cd src
ros2 pkg create arm_control --build-type ament_python
11. Docker + Dev Container (Optional, Recommended)

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
    "vscode": { "extensions": ["ms-iot.vscode-ros","ms-python.python","platformio.platformio-ide"] }
  }
}

Open VS Code → Reopen in Container → all dependencies pre-installed.

12. PlatformIO MCU Workspace Setup
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

Add skeleton main.cpp with control loop, encoder filtering, PID, as per your MCU specs.

13. Test the Stack

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
✅ Stack Summary & Data Flow
Layer	Role
MATLAB/Python	High-level math, planning, trajectory generation
ROS2	Sends joint commands, collects state, logging
Gazebo Fortress	Physics simulation, robot visualization, collision checks
PlatformIO / Teensy	Low-level motor control, real-time loop

All simulations, PID tuning, logging, and motion planning can be done before hardware arrival.

This version avoids Gazebo11 pitfalls, ensures ROS2 Humble + Gazebo Fortress are compatible, and includes correct Python and PlatformIO setup.

If you want, I can also provide a ready-to-use bash script that will install Ubuntu dependencies, ROS2 Humble, Gazebo Fortress, Python venv, Docker, and VS Code extensions automatically — this would fully automate all steps above.
