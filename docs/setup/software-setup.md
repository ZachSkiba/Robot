# 6-DOF Robotic Arm — Development Environment Setup
> **Stack:** ROS 2 Humble · Gazebo Fortress · MoveIt2 · ros2_control · Foxglove · WSL2 · VS Code Dev Container

---

## Stack Overview

| Component | Role |
|---|---|
| Windows 11 + WSL2 | Host OS + Linux virtualization |
| Ubuntu 22.04 | Development OS |
| ROS 2 Humble + MoveIt2 | Planning, kinematics, visualization |
| ros2_control | Hardware abstraction layer |
| Gazebo Fortress (Ignition) | GPU-accelerated simulation |
| Foxglove Studio | 3D telemetry + dashboards |
| Teensy 4.1 | Hard real-time PID, PWM, encoder interrupts |
| CycloneDDS | WSL2-stable DDS middleware |
| VS Code Dev Container | Reproducible team environment |
| Git + Git LFS | Version control with binary asset support |

---

## Phase 0 — Windows Preflight

### 0.1 Confirm Windows Version
```
winver
```
**Required:** Windows 11 22H2 or newer.

### 0.2 Confirm Virtualization
```
systeminfo
```
Look for: `A hypervisor has been detected`

If `Virtualization Enabled In Firmware: No` → enable **Intel VT-x** / **AMD SVM** in BIOS.

### 0.3 Confirm GPU Drivers
GPU acceleration is mandatory for Gazebo Fortress. Update to latest drivers and reboot Windows before proceeding.

---

## Phase 1 — Clean WSL2 Install

### 1.1 Install Ubuntu 22.04
```bash
wsl --install -d Ubuntu-22.04
```
Reboot Windows.

### 1.2 Confirm WSL2 Version
```bash
wsl -l -v
```
Must show: `Ubuntu-22.04  Running  2`

If version shows `1`:
```bash
wsl --set-version Ubuntu-22.04 2
```

---

## Phase 2 — Resource Allocation

Create `C:\Users\<you>\.wslconfig`:

```ini
[wsl2]
memory=12GB
processors=6
swap=8GB
localhostForwarding=true
```

**Guidelines:**
- 32 GB RAM → allocate 12–16 GB to WSL
- 16 GB RAM → 8 GB max

Apply and reopen Ubuntu:
```bash
wsl --shutdown
```

---

## Phase 2.5 — WSL Clock Sync

WSL2 clocks drift and will break TF trees and timestamps.

### Primary Method — ntpdate safeguard in `~/.bashrc`
```bash
sudo apt install ntpdate
```

Add to `~/.bashrc`:
```bash
# WSL2 clock safeguard
if grep -qi microsoft /proc/version; then
    sudo ntpdate -s time.windows.com > /dev/null 2>&1 || true
fi
```

### Plan B — Hardware Clock
```bash
sudo hwclock -s
```
Use if RViz or TF tree shows drift.

---

## Phase 3 — Ubuntu Base Setup

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y \
  build-essential git curl wget unzip python3-pip python3-venv \
  python3-dev cmake pkg-config mesa-utils net-tools \
  software-properties-common htop nano
```

---

## Phase 4 — GPU Acceleration Check

```bash
glxinfo -B
```
Must show: `Accelerated: yes`

Do not proceed to Gazebo until this passes.

---

## Phase 5 — Python Environment

```bash
mkdir -p ~/robot_ws
cd ~/robot_ws
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip setuptools wheel
pip install numpy scipy matplotlib pyserial pandas jupyterlab ipywidgets

deactivate
```

---

## Phase 6 — Teensy USB Handling

### 6.1 Install usbipd (Windows)
```bash
winget install usbipd
```

### 6.2 Attach Device
```bash
usbipd list
usbipd attach --wsl --busid <BUSID> --auto-attach
```

### 6.3 Verify in WSL
```bash
ls /dev/ttyACM*
```
Expected: `/dev/ttyACM0`

### 6.4 Fix Permissions
```bash
sudo usermod -a -G dialout $USER
wsl --shutdown
```

### 6.5 Optional udev Rule
```bash
sudo nano /etc/udev/rules.d/99-teensy.rules
```
```
KERNEL=="ttyACM[0-9]*", MODE="0666"
```
```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

### 6.6 Teensy CLI Upload
```bash
sudo apt install teensy-loader-cli
teensy_loader_cli --mcu=TEENSY41 -w firmware.hex
```

---

## Phase 7 — ROS 2 Humble Setup

### 7.1 Add ROS 2 Repository
```bash
sudo apt install -y curl gnupg lsb-release
sudo mkdir -p /etc/apt/keyrings
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | \
  gpg --dearmor | sudo tee /etc/apt/keyrings/ros2.gpg > /dev/null
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/ros2.gpg] \
  http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | \
  sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```

### 7.2 Install Full Stack
```bash
sudo apt update
sudo apt install -y \
  ros-humble-desktop \
  ros-humble-ros-dev-tools \
  ros-humble-ros2-control \
  ros-humble-ros2-controllers \
  ros-humble-moveit \
  ros-humble-ros-gz \
  ros-humble-ros-gz-bridge \
  ros-humble-tf2-tools \
  ros-humble-foxglove-bridge
```

### 7.3 Auto-source ROS 2
```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### 7.4 Switch to CycloneDDS (WSL Stability)
```bash
sudo apt install -y ros-humble-rmw-cyclonedds-cpp
echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" >> ~/.bashrc
source ~/.bashrc
```

---

## Phase 8 — Gazebo Fortress Smoke Test

```bash
gz sim
```

Confirms GPU acceleration and Ignition Fortress integration with ros2_control. If the window fails to open or renders on CPU, revisit Phase 4.

---

## Phase 9 — ROS Workspace & colcon

```bash
sudo apt install -y python3-colcon-common-extensions
mkdir -p ~/robot_ws/src
cd ~/robot_ws
colcon build --symlink-install
echo "source ~/robot_ws/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

**Expected workspace structure:**
```
robot_ws/
├── src/
│   ├── robot_control/
│   ├── robot_description/
│   └── robot_bringup/
├── build/         # generated — never commit
├── install/       # generated — never commit
└── log/           # generated — never commit
```

---

## Phase 10 — Telemetry: PlotJuggler + Foxglove

### PlotJuggler
```bash
sudo apt install -y ros-humble-plotjuggler-ros
ros2 run plotjuggler plotjuggler
```

### Foxglove Bridge
```bash
ros2 launch foxglove_bridge bridge.launch.py
```

Teammates connect via browser → 3D robot state, camera feeds, diagnostics.

---

## Phase 11 — VS Code Dev Container

### Install VS Code (Windows)
Extensions required: **Remote – WSL**, **Python**, **ROS**, **C/C++**, **GitLens**

### Dockerfile (`.devcontainer/Dockerfile`)
```dockerfile
FROM ubuntu:22.04

ARG UID=1000
ARG GID=1000

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update && apt-get install -y \
  sudo git git-lfs wget curl build-essential cmake \
  python3 python3-pip python3-venv vim nano locales \
  lsb-release gnupg2 usbutils usbip ccache \
  ros-humble-desktop ros-humble-ros-dev-tools \
  ros-humble-ros2-control ros-humble-ros2-controllers \
  ros-humble-moveit ros-humble-ros-gz \
  ros-humble-ros-gz-bridge ros-humble-tf2-tools \
  ros-humble-foxglove-bridge && \
  rm -rf /var/lib/apt/lists/*

RUN locale-gen en_US.UTF-8

RUN groupadd -g $GID robotdev || true
RUN useradd -ms /bin/bash -u $UID -g $GID robotdev
RUN usermod -aG sudo,dialout robotdev
RUN echo "robotdev ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER robotdev
WORKDIR /workspace

RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
RUN echo "export ROS_DOMAIN_ID=${ROS_DOMAIN_ID:-1}" >> ~/.bashrc
RUN echo "export ROS_NAMESPACE=${ROS_NAMESPACE:-robot_arm}" >> ~/.bashrc

RUN pip3 install --upgrade pip setuptools wheel black
RUN git lfs install
```

### devcontainer.json (`.devcontainer/devcontainer.json`)
```json
{
  "name": "6DOF Arm Dev Container",
  "build": {
    "dockerfile": "Dockerfile",
    "context": "..",
    "args": { "UID": 1000, "GID": 1000 }
  },
  "settings": {
    "terminal.integrated.shell.linux": "/bin/bash",
    "editor.formatOnSave": true,
    "python.formatting.provider": "black"
  },
  "extensions": [
    "ms-python.python",
    "ms-vscode.cpptools",
    "ms-iot.vscode-ros",
    "ms-vscode.cmake-tools",
    "MS-vsliveshare.vsliveshare"
  ],
  "remoteUser": "robotdev",
  "workspaceFolder": "/workspace",
  "mounts": [
    "source=${localWorkspaceFolder},target=/workspace,type=bind,consistency=cached"
  ],
  "runArgs": [
    "--privileged", "--net=host", "--pid=host", "--ipc=host",
    "-e", "DISPLAY=${localEnv:DISPLAY}",
    "-v", "/tmp/.X11-unix:/tmp/.X11-unix",
    "--device=/dev/dri:/dev/dri"
  ]
}
```

---

## Phase 12 — GitHub + Git LFS

```bash
cd ~/robot_ws
git init
git remote add origin <repo_url>
git lfs track "*.stl"
git add .gitattributes
git commit -m "Enable Git LFS for meshes"
git push -u origin main
```

**Team workflow:** one branch per feature → pull before building → merge via PRs only.

---

## Phase 13 — GitHub Workflow Guardrails

### 13.1 Repo Root Structure

Run `git init` at the repo root, not inside `~/robot_ws`.

```
6dof-robot-arm/          ← git init here
├── .devcontainer/
│   ├── Dockerfile
│   └── devcontainer.json
├── src/                 ← all ROS 2 packages
├── .gitignore
├── .gitattributes
└── README.md
```

> `build/`, `install/`, and `log/` are never committed. colcon generates them inside the container.

### 13.2 `.gitignore`

```gitignore
# ROS 2 build artifacts
build/
install/
log/

# Dev Container caches
.ccache/
.vscode/

# Python
venv/
__pycache__/
*.pyc
*.pyo
*.pyd

# OS
.DS_Store
Thumbs.db
```

### 13.3 Branch Protection for `main`

On GitHub: **Settings → Branches → Add branch protection rule**

- Branch pattern: `main`
- ✅ Require a pull request before merging
- ✅ Require at least 1 approval
- ✅ Require status checks to pass before merging

### 13.4 Dependency Protocol

When a developer adds any new package or library:

1. Add it to `.devcontainer/Dockerfile`
2. Commit the Dockerfile to the feature branch
3. Teammates pull → VS Code prompts **"Rebuild Container?"** → click Yes

> **Never** run `pip install` or `apt install` manually inside the container for team-wide features.

### 13.5 Daily Team Loop

```
Start:    git pull origin main
          git checkout -b feature/<name>

Code:     Open in Dev Container
          Write code → colcon build → test in Gazebo/Foxglove

Save:     git add .
          git commit -m "Description of change"
          git push origin feature/<name>

Review:   Open a Pull Request on GitHub
          Teammate reviews and approves

Merge:    Merge to main
          Everyone pulls latest main
```

---

## Phase 14 — Pair Programming with VS Code Live Share

### 14.1 Add Extension

In `.devcontainer/devcontainer.json`, Live Share is already included:
```json
"MS-vsliveshare.vsliveshare"
```
Rebuild the container after adding it.

### 14.2 Session Workflow

**Host** (person with arm or simulation running):
1. Open project in VS Code → let the Dev Container launch fully
2. Click the **Live Share** button (bottom-left)
3. Sign in with GitHub
4. Send the generated link to teammates

**Guest** (can be anywhere):
1. Open VS Code locally (no container needed)
2. Live Share extension installed locally
3. **Live Share → Join Collaboration Session → Paste link**

### 14.3 Collaborative Features

| Feature | How |
|---|---|
| Co-editing | Live cursors, real-time edits |
| Follow mode | Click teammate name in Live Share panel |
| Shared terminal | Right-click terminal → Share Terminal → Read/Write |
| Shared ports | Gazebo, Foxglove, RViz auto-forwarded to `localhost:<port>` |

### 14.4 Team Rules

| Scenario | Protocol |
|---|---|
| Different subsystems | Each dev works in their own container; sync via GitHub |
| Same bug / debugging | Host runs Dev Container + Live Share; Guest joins; commit + push when done |

---

## Phase 15 — URDF / XACRO Robot Description

### 15.1 Create the Package
```bash
cd ~/robot_ws/src
ros2 pkg create --build-type ament_cmake my_arm_description
mkdir -p my_arm_description/urdf
mkdir -p my_arm_description/meshes
```

### 15.2 Write the URDF/XACRO (`my_arm_description/urdf/my_arm.urdf.xacro`)

Define 6 links (physical segments) and 6 joints (motor axes) with positions, rotation axes, and limits.

Example — Joint 1 → Joint 2:
```xml
<link name="link1">
  <visual>
    <geometry>
      <cylinder radius="0.02" length="0.3"/>
    </geometry>
    <material name="blue"/>
  </visual>
</link>

<joint name="joint1" type="revolute">
  <parent link="base_link"/>
  <child link="link1"/>
  <origin xyz="0 0 0.1" rpy="0 0 0"/>
  <axis xyz="0 0 1"/>
  <limit lower="-1.57" upper="1.57" effort="5" velocity="1"/>
</joint>
```

### 15.3 Test Visualization
```bash
ros2 launch my_arm_description display.launch.py
```

The arm should appear in Foxglove or RViz.

> **Critical:** Incorrect joint axes or link lengths will break control and motion planning downstream.

---

## Phase 16 — ros2_control Hardware Interface

### 16.1 Create the Package
```bash
cd ~/robot_ws/src
ros2 pkg create --build-type ament_cmake my_arm_hw_interface
```

### 16.2 Add `<ros2_control>` Block to URDF

Use modern ROS 2 Humble + Gazebo Fortress syntax. Replace any legacy `<transmission>` tags.

```xml
<ros2_control name="GazeboSimSystem" type="system">
  <hardware>
    <plugin>gz_ros2_control/GazeboSimSystem</plugin>
  </hardware>

  <joint name="joint1">
    <command_interface name="position">
      <param name="min">-1.57</param>
      <param name="max">1.57</param>
    </command_interface>
    <state_interface name="position"/>
    <state_interface name="velocity"/>
  </joint>

  <!-- Repeat for joints 2–6 -->
</ros2_control>

<gazebo>
  <plugin filename="gz_ros2_control-system"
          name="gz_ros2_control::GazeboSimROS2ControlPlugin">
    <parameters>$(find my_arm_bringup)/config/ros2_controllers.yaml</parameters>
  </plugin>
</gazebo>
```

### 16.3 C++ Hardware Interface

Implement two methods:
- `read()` — pull current joint states from simulation or hardware
- `write()` — send velocity/position commands with safety checks and joint limits

> When swapping from simulation to real hardware, only the plugin target changes. MoveIt2 is untouched.

### 16.4 Launch
```bash
ros2 launch my_arm_description my_arm_control.launch.py
```

The arm now holds position and accepts commands in simulation.

---

## Phase 17 — Motion Planning & Telemetry

### 17.1 MoveIt2 Setup
```bash
ros2 launch moveit_setup_assistant setup_assistant.launch.py
```
- Import `my_arm.urdf.xacro`
- Generate motion planning pipelines and controllers (already compatible with ros2_control)

### 17.2 Foxglove Telemetry
```bash
ros2 launch my_arm_bringup foxglove.launch.py
```

Visualize joint states, arm motion, and camera feeds in 3D from any browser.

---

## Build Cache (ccache)

For fast rebuilds across all sessions:

```bash
export CCACHE_DIR=/workspace/.ccache
export PATH="/usr/lib/ccache:$PATH"
```

Add both lines to `~/.bashrc`.

---

## Architecture Summary

```
ROS 2 (Ubuntu 22.04 / WSL2)
├── MoveIt2          ← motion planning
├── ros2_control     ← hardware abstraction
│   ├── GazeboSimSystem   ← simulation driver
│   └── TeensyHardwareInterface  ← real hardware driver (swap in)
├── Foxglove Bridge  ← 3D telemetry
└── CycloneDDS       ← WSL-stable DDS middleware

Teensy 4.1
├── Hard real-time PID
├── PWM output
└── Encoder interrupts
```

---

## Feature Checklist

| Feature | Status |
|---|:---:|
| Gazebo Fortress (Ignition) | ✅ |
| ROS 2 Humble + MoveIt2 | ✅ |
| ros2_control + Hardware Interface | ✅ |
| Foxglove 3D Telemetry | ✅ |
| GPU-accelerated simulation | ✅ |
| Stable USB + Teensy integration | ✅ |
| CycloneDDS WSL2 stability | ✅ |
| Persistent build cache (ccache) | ✅ |
| GitHub + Git LFS | ✅ |
| VS Code Dev Container | ✅ |
| TF / Kinematics consistency | ✅ |
| Python + C++ formatting (black) | ✅ |
| ROS_DOMAIN_ID isolation | ✅ |
| Branch protection on main | ✅ |
| Dockerfile dependency protocol | ✅ |
| VS Code Live Share pair programming | ✅ |
| Sim-to-Real hardware abstraction | ✅ |