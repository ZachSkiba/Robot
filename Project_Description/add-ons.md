# Phase 0-5 Scope Definition

## Purpose
Define which capabilities belong in Phases 0-5 of the robotic arm project and which should be deferred until the system is more mature.

## Included Capabilities

### PID Control
**Phase:** 2-3  
**Priority:** Core

- Joint-level position control
- Gain comparison
- Measurement of rise time, overshoot, and steady-state error

This establishes the baseline controller and creates the reference point for later improvements.

### System Identification
**Phase:** 4-5  
**Priority:** Core

- Estimate motor constants, friction, gear ratios, and delay from experiments
- Fit simplified models
- Validate models against measured motion

This connects the hardware to a usable analytical model.

### Lightweight Trajectory Optimization
**Phase:** Late 5  
**Priority:** Allowed

- Optimize point-to-point motion
- Minimize time, energy proxy, or smoothness cost
- Compare optimized motion against the PID baseline

Scope should remain narrow. Full optimal-control work is not required at this stage.

### Kinematics-Based Simulator
**Phase:** 5  
**Priority:** Allowed

- Simple simulator parameterized by measured values
- Used for visualization and sanity checks

This is not a full digital twin and should not be described as one.

## Deferred Capabilities

### Reinforcement Learning
**Phase:** 8+

- Requires stable control
- Requires large, clean datasets
- Requires a reliable simulator or strong safety constraints

Reinforcement learning should remain future work until the system is instrumented and repeatable.

### Predictive Maintenance
**Phase:** 10+

- Requires long-term degradation data
- Requires meaningful failure signatures over time

This does not fit early development phases.

## Recommended Add-Ons Within Phase 0-5

### Calibration Pipeline
**Phase:** 3-4

- Automatic homing
- Zero-offset estimation
- Repeatability testing

### Constraint-Aware Motion Planning
**Phase:** 4-5

- Joint-limit enforcement
- Velocity limits
- Unsafe-motion rejection
- Defined collision-free regions where practical

### Data Infrastructure
**Phase:** 3-5

- Automatic logging of joint states, commands, and errors
- Structured datasets
- Plots and quantitative metrics

### Performance Benchmarking
**Phase:** 5

- Accuracy
- Repeatability
- Energy or effort proxy
- Controller-to-controller comparison

### Model Validation
**Phase:** 5

- Predict motion using the identified model
- Compare prediction against measured behavior
- Quantify mismatch

### PS5 Controller Integration
**Phase:** 3-4  
**Status:** Optional

Use the controller as a teleoperation and data-collection interface, not as a substitute for autonomous control.

#### Appropriate Uses
- Manual trajectory collection
- Baseline comparison against PID and optimized motion
- Safety and limit testing
- Mode switching between manual, autonomous, and replay modes

#### Minimal Technical Scope
- Controller input mapping
- Joint-velocity commands
- Logging of input, joint state, and timestamps
- Replay of recorded motions

## Phase 0-5 Checklist

### In Scope
- 3 DOF robotic arm
- Sensors and automatic logging
- PID control
- System identification
- Lightweight optimization
- Kinematics-based simulation
- Calibration and benchmarking

### Out of Scope
- Reinforcement learning
- Full digital twin
- Predictive maintenance
- Large perception or vision additions
