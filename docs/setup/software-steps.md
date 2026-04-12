# Software Setup Steps

This document captures a step-by-step setup workflow for the 6-DOF robotic arm environment.

## Included Components

- Gazebo Fortress (Ignition), no legacy Gazebo 11 confusion.
- `ros2_control` Hardware Interface for Teensy ↔ ROS2 integration.
- Foxglove Studio for modern 3D telemetry.
- Complete, step-by-step, production-grade workflow for your team.

## 🧱 PHASE 0 — Windows Preflight

0.1 Confirm Windows Version

```text
winver
Required: Windows 11 22H2 or newer
```

0.2 Confirm Virtualization is Active

```text
systeminfo
Look for: A hypervisor has been detected
If Virtualization Enabled In Firmware: No → enable Intel VT-x / AMD SVM in BIOS
```

0.3 Confirm GPU Drivers

For Gazebo Fortress (Ignition), GPU acceleration is mandatory.
Update to latest drivers and reboot Windows.

## 🖥 PHASE 1 — Clean WSL2 Install

1.1 Install Ubuntu 22.04

```bash
wsl --install -d Ubuntu-22.04
```
Reboot Windows

1.2 Confirm WSL2 Version

```bash
wsl -l -v
```
Must show: Ubuntu-22.04 Running 2
If version 1:
```bash
wsl --set-version Ubuntu-22.04 2
```

## 🧠 PHASE 2 — Resource Allocation

Create C:\Users\<you>\.wslconfig:

```ini
[wsl2]
memory=12GB
processors=6
swap=8GB
localhostForwarding=true
```

Guidelines:

- 32GB RAM → 12–16GB for WSL
- 16GB RAM → 8GB max

Apply:
```bash
wsl --shutdown
```
Reopen Ubuntu

## 🕒 PHASE 2.5 — WSL Clock & Time Sync

Primary Method: ntpdate safeguard in ~/.bashrc:

```bash
sudo apt install ntpdate
```

Add:

```bash
# WSL2 clock safeguard
if grep -qi microsoft /proc/version; then
    sudo ntpdate -s time.windows.com > /dev/null 2>&1 || true
fi
```

Plan B (Hardware Clock):

```bash
sudo hwclock -s
```
Use if RVIZ or TF tree shows drift

## 🧰 PHASE 3 — Ubuntu Base Setup

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y \
build-essential git curl wget unzip python3-pip python3-venv \
python3-dev cmake pkg-config mesa-utils net-tools \
software-properties-common htop nano
```

## 🎮 PHASE 4 — GPU Acceleration Check

```bash
glxinfo -B
```
Must show: Accelerated: yes

## 🔐 PHASE 5 — Python Environment

```bash
mkdir -p ~/robot_ws
cd ~/robot_ws
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip setuptools wheel
pip install numpy scipy matplotlib pyserial pandas jupyterlab ipywidgets

deactivate
```

## 🔌 PHASE 6 — Teensy USB Handling

6.1 Install usbipd (Windows)

```bash
winget install usbipd
```

6.2 Attach Device

```bash
usbipd list
usbipd attach --wsl --busid <BUSID> --auto-attach
```

6.3 Verify in WSL

```bash
ls /dev/ttyACM*
```
Should see /dev/ttyACM0

6.4 Fix Permissions

```bash
sudo usermod -a -G dialout $USER
wsl --shutdown
```

6.5 Optional udev Rule

```bash
sudo nano /etc/udev/rules.d/99-teensy.rules
```
```text
KERNEL=="ttyACM[0-9]*", MODE="0666"
```
```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

6.6 Teensy CLI Upload

```bash
sudo apt install teensy-loader-cli
teensy_loader_cli --mcu=TEENSY41 -w firmware.hex
```

## 🤖 PHASE 7 — ROS2 Humble Setup (Updated)

7.1 Add ROS2 Repository

sudo apt install -y curl gnupg lsb-release
sudo mkdir -p /etc/apt/keyrings
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | \
gpg --dearmor | sudo tee /etc/apt/keyrings/ros2.gpg > /dev/null
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/ros2.gpg] \
http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | \
sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

7.2 Install ROS2 + ros2_control + MoveIt2 + Gazebo Fortress + Foxglove

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

7.3 Auto-source ROS2

echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc

7.4 Switch to CycloneDDS for WSL Stability

sudo apt install -y ros-humble-rmw-cyclonedds-cpp
echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" >> ~/.bashrc
source ~/.bashrc
🌍 PHASE 8 — Gazebo Fortress Simulation
gz sim
Confirms Ignition Fortress GPU acceleration and integration with ros2_control
🏗 PHASE 9 — ROS Workspace & colcon
sudo apt install -y python3-colcon-common-extensions
mkdir -p ~/robot_ws/src
cd ~/robot_ws
colcon build --symlink-install
echo "source ~/robot_ws/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
Workspace structure:
robot_ws/
  src/
    robot_control/
    robot_description/
    robot_bringup/
  build/
  install/
  log/
📊 PHASE 10 — Telemetry: PlotJuggler + Foxglove
sudo apt install -y ros-humble-plotjuggler-ros
ros2 run plotjuggler plotjuggler
Foxglove Bridge runs inside container:
ros2 launch foxglove_bridge bridge.launch.py
Teammates access via browser → 3D robot state, camera feeds, diagnostics
🖥 PHASE 11 — VS Code + Dev Container (Updated)
Install VS Code (Windows)
Extensions: Remote – WSL, Python, ROS, C/C++, GitLens

Dev Container Dockerfile (Updated for Fortress + Foxglove + UID/GID):

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

devcontainer.json

{
  "name": "6DOF Arm Dev Container",
  "build": {
    "dockerfile": "Dockerfile",
    "context": "..",
    "args": {"UID": 1000, "GID": 1000}
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
    "ms-vscode.cmake-tools"
  ],
  "remoteUser": "robotdev",
  "workspaceFolder": "/workspace",
  "mounts": ["source=${localWorkspaceFolder},target=/workspace,type=bind,consistency=cached"],
  "runArgs": ["--privileged","--net=host","--pid=host","--ipc=host","-e","DISPLAY=${localEnv:DISPLAY}","-v","/tmp/.X11-unix:/tmp/.X11-unix","--device=/dev/dri:/dev/dri"]
}
🔥 PHASE 12 — GitHub + Git LFS
cd ~/robot_ws
git init
git remote add origin <repo_url>
git lfs track "*.stl"
git add .gitattributes
git commit -m "Enable Git LFS for meshes"
git push -u origin main
Workflow: one branch per feature, pull before building, merge via PRs
🧠 ROS ↔ Teensy Professional Interface
Use ros2_control Hardware Interface: Teensy appears as a driver node identical to Gazebo simulation.
Provides:
Enforced joint limits
Velocity / position safety
Packet drop handling → prevents singularity disasters
ROS: planning, kinematics, visualization, logging
Teensy: hard real-time PID, PWM, encoder interrupts
⚡ Build Persistence & ccache
export CCACHE_DIR=/workspace/.ccache
export PATH="/usr/lib/ccache:$PATH"
Persistent cache → lightning-fast rebuilds
✅ Summary of Features
Feature	Status
Gazebo Fortress (Ignition)	✅
ROS2 Humble + MoveIt2	✅
ros2_control + Hardware Interface	✅
Foxglove 3D Telemetry	✅
GPU-accelerated simulation	✅
Stable USB + Teensy integration	✅
CycloneDDS WSL2 stability	✅
Persistent build cache	✅
GitHub + Git LFS	✅
VS Code Dev Container	✅
TF/Kinematics consistency	✅
Python + C++ formatting	✅
ROS_DOMAIN_ID isolation	✅

This is the fully integrated, production-grade, 2026 stack. Your team can open VS Code → reopen in container → build → simulate → run real arm with zero hidden pitfalls.

I can now generate a single-page, High-Octane Quick-Start README.md that your 2-3 developers can literally follow without missing a single step.Absolutely. Here’s the fully polished 2026-ready workflow, integrating Gemini’s GitHub guardrails without changing any previous steps, while keeping your ROS2 / Dev Container / Gazebo Fortress / Foxglove setup intact.

🧱 PHASE 0–12 (As previously defined, unchanged)

Everything from the original “Golden Image” setup remains identical:

Windows 11 + WSL2
Ubuntu 22.04
GPU acceleration verified
ROS 2 Humble + MoveIt2 + ros2_control
Teensy real-time hardware interface
Gazebo Fortress simulation
Foxglove telemetry
VS Code Dev Container
CycloneDDS
Persistent ccache
Python + C++ formatting
ROS_DOMAIN_ID isolation

No changes here. All previous instructions are preserved verbatim.

🟢 PHASE 13 — GitHub Workflow Guardrails (New)

This section adds the final polish to make your repo bulletproof for teamwork.

13.1 Git Root Folder Correction

Your Git repo must contain the Dev Container and ROS workspace at the root, not inside ~/robot_ws.

Repo Structure (root):

6dof-robot-arm/          <-- Run `git init` HERE
├── .devcontainer/       <-- Dockerfile & devcontainer.json
│   ├── Dockerfile
│   └── devcontainer.json
├── src/                 <-- All ROS 2 packages (robot_description, robot_control, etc.)
├── .gitignore           <-- (See Step 13.2)
├── .gitattributes       <-- For Git LFS
└── README.md

Note: build/, install/, log/ are never committed. Colcon generates them inside the container.

13.2 Bulletproof .gitignore

Create a .gitignore in the repo root before the first commit:

# ROS 2 Build files
build/
install/
log/

# VS Code & Dev Container Caches
.ccache/
.vscode/

# Python
venv/
__pycache__/
*.pyc
*.pyo
*.pyd

# OS generated files
.DS_Store
Thumbs.db
Prevents accidentally committing compiled binaries, Python caches, or virtual environments.
13.3 GitHub Branch Protection ("Do Not Break Main")

On GitHub.com:

Go to Settings → Branches → Add branch protection rule
Branch pattern: main
Enable:
Require a pull request before merging
Require at least 1 approval
Require status checks to pass before merging (forces build/test to pass)
Protects the main branch from broken builds or accidental deletions.
13.4 Adding Dependencies Protocol

Whenever a developer adds a system package, ROS package, or Python library:

Modify the Dockerfile in .devcontainer/ to include the dependency.
Commit the Dockerfile to the feature branch.

When another teammate pulls, VS Code will prompt:

“Dev Container configuration changed. Rebuild?”

Clicking Yes rebuilds the container, ensuring identical environments for all team members.
Never run pip/apt install manually inside the container for team-wide features.
Guarantees everyone stays in sync.
13.5 Team Daily Loop

With these guardrails, the workflow is clean and reproducible:

Start Work:
  git pull origin main
  git checkout -b feature/new-gripper

Code & Test:
  Open in Dev Container
  Write code
  colcon build
  Test in Gazebo/Foxglove

Save:
  git add .
  git commit -m "Added gripper logic"
  git push origin feature/new-gripper

Review:
  Open a Pull Request on GitHub
  Teammate reviews and approves

Merge:
  Merge to main
  Everyone pulls latest main
No more 5GB binaries, broken branches, or environment drift.
Ensures reproducibility and stability.
✅ Recap of Additions
Feature	Status
Git repo root includes .devcontainer & src	✅
.gitignore prevents build/venv pollution	✅
Branch protection for main	✅
Dockerfile-based dependency protocol	✅
Team workflow fully documented	✅

Everything from Phase 0–12 remains untouched. Phase 13 adds GitHub discipline only, no other workflow changes.

If you want, I can now map out the exact architecture for the first ROS 2 package, including:

robot_description URDF setup
ros2_control hardware interface node for the Teensy
MoveIt2 + Foxglove integration

So that the 6-DOF arm immediately shows up in simulation and telemetry, ready for your team to iterate.

Do you want me to produce that next?🟢 PHASE 14 — Pair Programming with VS Code Live Share

This phase enables real-time collaboration on the same Dev Container, letting your team work together on the 6-DOF arm safely and efficiently. It complements your GitHub workflow: only one person needs to run the physical arm or the simulation, while others can join remotely.

14.1 Update Dev Container Extensions
Open your .devcontainer/devcontainer.json.
Add the Live Share extension to your extensions list:
"extensions": [
    "ms-python.python",
    "ms-vscode.cpptools",
    "ms-iot.vscode-ros",
    "ms-vscode.cmake-tools",
    "MS-vsliveshare.vsliveshare"  // <-- ADD THIS LINE
]
Save the file.
Rebuild the container when prompted by VS Code (Rebuild Container) to ensure the extension is installed inside the container.

✅ This ensures Live Share is always ready for pair programming sessions.

14.2 Real-Time Workflow

This workflow defines Host and Guest roles.

Step 1 — Host Setup
The Host is the person with the physical arm connected or running the Gazebo simulation.
Open the project folder in VS Code.
Let the Dev Container launch fully.

Start a Live Share session:

Look at the bottom-left of the VS Code window. Click the Live Share button.
Sign in using your GitHub account.
A collaboration link is automatically copied to your clipboard.
Send this link to your teammate(s).

🔑 Only the Host needs to run the simulation or connect to the Teensy arm.

Step 2 — Guest Join
The Guest can be anywhere, even miles away.
Open VS Code on their Windows machine (no container needed initially).
Ensure the Live Share extension is installed locally.
Click Live Share → Join Collaboration Session → Paste the Host’s link.
Step 3 — Collaborative Features

Once connected, you can work in "Google Docs mode" with superpowers:

Co-Editing
Both developers see live cursors and edits.
Example: Host types a function, Guest can immediately add the next line.
Following
By default, guests are independent in file navigation.
To follow someone, click their name in the Live Share panel.
The screen will lock to their cursor and view.
Shared Terminal
By default, the Guest can read the Host’s terminal.
To allow write access:
Right-click Terminals → Share Terminal → Read/Write
Guest can now run commands inside the Dev Container (e.g., colcon build, ros2 run).
Shared Servers
Ports opened in the container (Gazebo, Foxglove, RVIZ) are automatically forwarded.
Guests can view telemetry dashboards via localhost:<port> in their browser.
14.3 Team Rules

To prevent confusion or conflicts:

Scenario	Protocol
Different parts of the robot	Each dev works in their own container; sync via GitHub only.
Same bug / problem solving	Host runs Dev Container and Live Share. Guest joins session. Work together, then commit & push to GitHub.

✅ This ensures safe, isolated development when independent and real-time collaboration when necessary.

14.4 Key Benefits
Only one person runs the robot hardware or simulation.
No need to worry about USB/Teensy conflicts.
Guests can co-edit code, build, and trigger robot motion safely.
Foxglove dashboards and Gazebo windows are fully shareable via network port forwarding.
Works seamlessly with the GitHub workflow, branch protection, and Docker-based environment.

Next Step:

With Phase 14 in place, your environment is fully collaborative, reproducible, and professional. The next natural step is Phase 15 — ROS 2 Package Architecture, including:

robot_description URDF
ros2_control hardware interface node
Integration with MoveIt2 and Foxglove

This will get your 6-DOF arm moving in both simulation and real-time telemetry.

If you want, I can now draft Phase 15 as a fully detailed, professional architecture guide, mapping the first ROS 2 package from URDF → ros2_control → MoveIt2 → Foxglove telemetry, with proper folder structure, package.xml, CMakeLists.txt, and initial nodes ready for development.

Do you want me to do that next?🟢 PHASE 15–17 — Simulation & Control of the 6-DOF Arm

You now have a complete Dev Container, Gazebo Fortress, and Foxglove setup. Phase 15–17 is where the simulation comes alive, and your software team can start controlling the arm before any hardware exists.

This is the essence of Sim-to-Real: fully test and debug software in simulation so that when the physical arm is built, it just works.

🟢 PHASE 15 — Building the Simulation (URDF / XACRO)

Goal: Make ROS 2 aware of your 6-DOF arm so Gazebo and Foxglove can visualize it.

Steps:

Create a ROS 2 package for the robot description

cd ~/robot_ws/src
ros2 pkg create --build-type ament_cmake my_arm_description
mkdir -p my_arm_description/urdf
mkdir -p my_arm_description/meshes
Write the URDF/XACRO
Create my_arm_description/urdf/my_arm.urdf.xacro
Define:
6 links → Physical segments of the arm
6 joints → NEMA motor axes
Joint positions, rotation axes, and limits

Example snippet for Joint 1 → Joint 2:

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

Test visualization

ros2 launch my_arm_description display.launch.py
You should see your digital 6-DOF arm in Foxglove or RViz.

✅ Result: The arm exists in the simulation world.

🟢 PHASE 16 — Hardware Interface (ros2_control)

Goal: Allow ROS 2 to command the motors, even in simulation, using modern ROS 2 Humble + Gazebo Fortress syntax.

Steps:

Create the hardware interface package

cd ~/robot_ws/src
ros2 pkg create --build-type ament_cmake my_arm_hw_interface

Define <ros2_control> in your URDF
Replace legacy <transmission> tags with modern ROS 2 syntax:

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

    <!-- Repeat joint blocks for joints 2–6 -->
</ros2_control>

<gazebo>
    <plugin filename="gz_ros2_control-system" name="gz_ros2_control::GazeboSimROS2ControlPlugin">
        <parameters>$(find my_arm_bringup)/config/ros2_controllers.yaml</parameters>
    </plugin>
</gazebo>
Write the C++ hardware interface
For now, it talks to GazeboSimSystem.
Later, swap to TeensyHardwareInterface with no changes to MoveIt2.
Implement:
read() → current joint states from simulation/hardware
write() → send velocity/position commands
Safety checks & joint limits

Launch simulation with ros2_control

ros2 launch my_arm_description my_arm_control.launch.py
The arm now holds position and accepts commands.

✅ Result: Arm is fully controllable in simulation. Swapping in real hardware is seamless.

🟢 PHASE 17 — Motion Planning & Telemetry

Goal: Use MoveIt2 and Foxglove Studio for planning, debugging, and telemetry.

Steps:

MoveIt2

Create a MoveIt2 configuration package:

ros2 launch moveit_setup_assistant setup_assistant.launch.py
Import your my_arm.urdf.xacro
Generate motion planning pipelines and controllers (already compatible with ros2_control).
Foxglove Studio
Use ros-humble-foxglove-bridge

Launch:

ros2 launch my_arm_bringup foxglove.launch.py
Visualize joint states, arm motion, and optionally camera feeds in 3D from any browser.

✅ Result: Your software team can now develop algorithms, test kinematics, and visualize telemetry before hardware exists.

Key Notes & Best Practices
URDF Accuracy → Incorrect joint axes or link lengths break control & motion planning.
Hardware Interface Abstraction → Treat GazeboSimSystem like a “dummy Teensy.” Swap real hardware later.
Version Control → Commit my_arm_description and my_arm_hw_interface without build/install/log/.
Sim-to-Real Philosophy → Everything tested in simulation will work on hardware once plugged in.

If you want, I can generate the complete my_arm.urdf.xacro boilerplate with all 6 links/joints, the full <ros2_control> block, and example ros2_controllers.yaml, so your team can copy-paste it directly and see a working digital arm in Gazebo immediately.

Do you want me to produce that next?
