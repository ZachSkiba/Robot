# 6-DOF Robotic Arm — Professional Software Setup

Supported development environment for this repository.

The workflow is designed so a new contributor can clone the repo, open the container, build the workspace, and get the same result every time.

## Gold Path

The supported path for this repo is:

1. Windows 11
2. WSL2 with Ubuntu 22.04
3. Docker Desktop with WSL integration
4. VS Code Dev Containers
5. ROS 2 Humble inside the repo-owned container

If you follow this path, the host stays thin and the robotics stack lives in versioned repo config under `.devcontainer/`.

## What "Professional" Means Here

- One supported setup path, not three competing ones.
- Repo-owned dependencies, not ad-hoc local installs.
- Clean `colcon build --symlink-install` from a fresh container.
- Exact verification gates after each phase.
- Generated files never committed.
- `main` always builds.
- Hardware and simulation are layered on only after the base workspace is stable.

## Current Repo Scope

Today this repository validates these two ROS 2 packages:

- `robot_control`
- `my_arm_description`

The container already installs the larger stack we want long-term:

- ROS 2 Humble
- MoveIt 2
- `ros2_control`
- Gazebo / `ros_gz`
- Foxglove Bridge
- Teensy tooling

That does not mean the repo is already wired end-to-end for simulation and hardware. Right now the professional target is:

1. Open the repo in the dev container.
2. Build the workspace successfully.
3. Run the starter ROS 2 node successfully.
4. Add simulation and hardware bringup only after that base is stable.

## What Belongs In Git

Commit these:

- source code under `src/`
- launch files, URDF or Xacro, configs, meshes, and docs
- `.devcontainer/`
- `package.xml` and `CMakeLists.txt`
- optional dependency manifests such as `.repos` files

Do not commit these:

- `build/`
- `install/`
- `log/`
- `.venv/`
- ROS logs and local caches
- downloaded apt packages
- container filesystem contents
- anything installed under `/opt/ros`

Professional rule:

- Git stores source and configuration
- the container stores installed tools
- `build/`, `install/`, and `log/` are disposable local artifacts

If you need extra ROS packages, add them to the devcontainer image instead of dropping downloaded binaries into the repo.

## Phase 0 — Host Prerequisites

Install these on Windows:

- Windows 11 22H2 or newer
- WSL2
- Ubuntu 22.04
- Docker Desktop
- VS Code
- VS Code extension: `Dev Containers`

Recommended checks on Windows:

```powershell
winver
wsl -l -v
```

Expected:

- Windows 11
- `Ubuntu-22.04` on version `2`

If you want smoother Gazebo performance under WSLg, keep GPU drivers current and reboot after driver updates.

## Phase 1 — WSL2 Baseline

If Ubuntu 22.04 is not installed yet:

```powershell
wsl --install -d Ubuntu-22.04
```

Optional but recommended WSL tuning in `C:\Users\<you>\.wslconfig`:

```ini
[wsl2]
memory=12GB
processors=6
swap=8GB
localhostForwarding=true
```

Apply changes:

```powershell
wsl --shutdown
```

## Phase 2 — Clone And Open The Repo

Clone the repository, then open the `Robot` folder in VS Code.

In VS Code:

1. Open the `Robot` folder.
2. Accept the prompt to `Reopen in Container`.
3. Wait for the container build to finish.

Important:

- `Rebuild Container` is a local action.
- You do not need to commit or push first.
- Your uncommitted files stay in your workspace.
- Rebuilding is how changes in `.devcontainer/` actually take effect.

This repo's container is the source of truth for ROS, Gazebo-related packages, `colcon`, `rosdep`, and the other robotics tools. Do not manually install a second ROS stack inside the same workflow unless you are intentionally maintaining the container image.

If you need a new dependency:

- add Ubuntu or ROS packages to `.devcontainer/Dockerfile`
- add Python packages to the image or a tracked requirements file
- add source dependencies via a `.repos` manifest or as intentional source packages under `src/`

Then rebuild the container instead of committing installed outputs.

## Phase 3 — Verify The Container

Open a terminal in the container and confirm you are in the repo root:

```bash
pwd
```

Expected:

```text
/workspace/Robot
```

Then run:

```bash
source /opt/ros/humble/setup.bash
printenv ROS_DISTRO
colcon build --symlink-install
source install/setup.bash
ros2 run robot_control robot_node
```

Expected:

- `ROS_DISTRO` prints `humble`
- `colcon build --symlink-install` finishes successfully
- `ros2 run robot_control robot_node` prints that the node is running

This is the first hard gate. If this does not pass, do not move on to Gazebo, MoveIt, Teensy, or Foxglove yet.

## Phase 4 — Daily Development Rules

Inside the container:

```bash
cd /workspace/Robot
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
```

Rules:

- Build before pushing.
- Never commit `build/`, `install/`, or `log/`.
- Keep `.devcontainer/` changes intentional and reviewed.
- Prefer small branches and pull requests over direct pushes to `main`.
- If the container config changes, use `Dev Containers: Rebuild Container`.

Related docs:

- [how-to-commit.md](./how-to-commit.md)
- [colaborating-dev-container.md](./colaborating-dev-container.md)

## Phase 5 — Optional Simulation Readiness

Only do this after Phase 3 passes.

GPU / OpenGL smoke test inside the container:

```bash
glxinfo -B
```

Gazebo smoke test:

```bash
gz sim
```

What this proves:

- WSLg graphics are working
- the container can open GPU-backed simulation tools

What it does not prove:

- that this repo already has a completed Gazebo world
- that `ros2_control` hardware interfaces are finished
- that MoveIt planning pipelines are configured

Those are repo implementation milestones, not machine setup milestones.

## Phase 6 — Optional Hardware / Teensy Readiness

Only do this after Phase 3 passes.

On Windows, install `usbipd` if needed:

```powershell
winget install usbipd
usbipd list
usbipd attach --wsl --busid <BUSID> --auto-attach
```

Inside WSL or the container, verify the device:

```bash
ls /dev/ttyACM*
```

Expected:

```text
/dev/ttyACM0
```

If serial permissions are wrong:

```bash
sudo usermod -a -G dialout $USER
```

Then fully restart the WSL or container session.

## Common Failure Modes

### `ModuleNotFoundError: No module named 'ament_package'`

Cause:

- ROS environment was not sourced before running `colcon`

Fix:

```bash
source /opt/ros/humble/setup.bash
colcon build --symlink-install
```

### `colcon` works for one shell but not another

Cause:

- one shell has ROS sourced and the other does not

Fix:

- use the integrated terminal in the dev container
- source `/opt/ros/humble/setup.bash` before building

### Warnings about `/workspace/install/...` or `not found: "/workspace/install/local_setup.bash"`

Cause:

- stale build or install artifacts from an older container layout
- old `AMENT_PREFIX_PATH` or `CMAKE_PREFIX_PATH` entries baked into generated setup files

Fix:

1. Rebuild the dev container.
2. Open a fresh terminal.
3. Remove generated workspace artifacts.
4. Re-source ROS and rebuild from scratch.

Commands:

```bash
cd /workspace/Robot
rm -rf build install log
source /opt/ros/humble/setup.bash
rosdep install --from-paths src --ignore-src -y
colcon build --symlink-install
source /workspace/Robot/install/setup.bash
```

### Gazebo opens slowly or fails to render

Cause:

- WSLg / GPU / Docker Desktop graphics issue

Fix:

- update Windows GPU drivers
- restart WSL
- rebuild or restart the container
- verify `glxinfo -B` before retrying `gz sim`

### No `/dev/ttyACM0`

Cause:

- the Teensy is not attached through `usbipd`
- the container or WSL session was started before the device was attached

Fix:

- re-run `usbipd attach --wsl ...`
- reopen the terminal or restart the container

## What Not To Do

- Do not install random ROS packages directly on the host as a workaround.
- Do not mix a separate Python virtual environment into the ROS build path unless you know exactly why.
- Do not debug simulation before the workspace builds.
- Do not treat build errors as a machine problem until the repo configuration is checked first.

## Industry-Grade Definition Of Done

This setup is in a strong professional state when all of the following are true:

- A new teammate can clone the repo and open it in the container without custom instructions.
- `colcon build --symlink-install` passes from a fresh container.
- `ros2 run robot_control robot_node` runs without manual repair steps.
- The setup document matches the repo exactly.
- Build artifacts stay out of Git.
- Branch protection and code review are enforced on `main`.
- Simulation and hardware setup are added as separate verified layers, not mixed into initial onboarding.

## Recommended Next Upgrades

Once the base workflow is stable, the next professional upgrades are:

1. Add a `robot_bringup` package with launch files.
2. Add real URDF or Xacro content under `my_arm_description`.
3. Add a Gazebo launch path and a simulation smoke test script.
4. Add `ros2_control` interfaces for hardware.
5. Add CI so pull requests run the same build gate automatically.

That is how this becomes "top industry": not by making the setup longer, but by making it reproducible, validated, and honest.
