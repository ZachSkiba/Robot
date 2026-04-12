# 6-DOF Robotic Arm Platform

This repository documents the design, simulation, and staged build-out of a 6-degree-of-freedom robotic arm with an emphasis on safety, telemetry, and disciplined systems engineering.

## What This Project Is

The goal of this project is to build a robotic arm platform that can move safely, log meaningful telemetry, and scale from early simulation work to hardware-in-the-loop validation and full physical deployment.

The project combines:

- mechanical design and fabrication planning
- ROS 2 / MoveIt development
- embedded control concepts
- telemetry, logging, and validation workflows

## Current Status

- Project architecture and planning documents are in place
- ROS 2 workspace and development container are configured
- `robot_control` package scaffolding exists in [`src/robot_control`](/workspace/Robot/src/robot_control)
- phase-by-phase planning documents are organized for staged execution

## Repository Structure

- [`Overall_Project`](/workspace/Robot/Overall_Project): project-wide vision, constraints, materials, risks, and system-level notes
- [`Phase0-Plan`](/workspace/Robot/Phase0-Plan): foundational planning, modeling, and early simulation documents
- [`Phase1-Arm`](/workspace/Robot/Phase1-Arm): physical arm build planning and telemetry goals
- [`Phase2-Trajectory`](/workspace/Robot/Phase2-Trajectory) through [`Phase11-Endgame`](/workspace/Robot/Phase11-Endgame): longer-range roadmap by project phase
- [`Project_Description`](/workspace/Robot/Project_Description): higher-level motivation and project framing
- [`Other`](/workspace/Robot/Other): working notes and utility documents that still need cleanup into permanent locations
- [`src/robot_control`](/workspace/Robot/src/robot_control): ROS 2 package scaffold for project code
- [`.devcontainer`](/workspace/Robot/.devcontainer): reproducible development environment for VS Code and Docker

## Getting Started

### Option 1: VS Code Dev Container

1. Open the [`Robot`](/workspace/Robot) folder in VS Code.
2. Reopen the project in the dev container.
3. Let the container finish dependency setup.
4. Open a terminal in the container and build the workspace as needed.

### Option 2: Existing ROS 2 Humble Environment

1. Source ROS 2 Humble.
2. From [`/workspace/Robot`](/workspace/Robot), build with `colcon build`.
3. Source `install/setup.bash`.

## Recommended Reading Order

If you are reviewing the project for the first time, start here:

1. [`Overall_Project/README.md`](/workspace/Robot/Overall_Project/README.md)
2. [`Overall_Project/system_overview.md`](/workspace/Robot/Overall_Project/system_overview.md)
3. [`Phase0-Plan/README.md`](/workspace/Robot/Phase0-Plan/README.md)
4. [`Phase1-Arm/Overview.md`](/workspace/Robot/Phase1-Arm/Overview.md)

## Professional Focus

This repository is being developed as both a technical project and a portfolio artifact. The intent is to show:

- structured systems thinking
- safety-aware robotics design
- staged validation instead of ad hoc prototyping
- clear technical communication across software and hardware work

## Next Cleanup Priorities

The highest-value repo cleanup tasks are:

1. Move polished documentation into a dedicated `docs/` area.
2. Rename phase folders with zero-padded numbers for cleaner sorting.
3. Rehome files from [`Other`](/workspace/Robot/Other) into permanent categories.
4. Replace placeholder package metadata in [`package.xml`](/workspace/Robot/src/robot_control/package.xml).
5. Use descriptive commit messages instead of repeated "End of day save" commits.
