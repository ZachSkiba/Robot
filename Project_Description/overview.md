# Robotic Arm Project Roadmap

## Principle
Each phase should produce measurable outputs: logged data, plots, validation metrics, or pass/fail criteria. The project should advance only when the current phase is stable and observable.

## Phase 0: Architecture and Simulation
**Timeline:** Weeks 1-2

### Scope
- Define a 3 DOF baseline model and cap early physical scope at 5 DOF
- Set joint limits and link lengths
- Implement forward and inverse kinematics
- Simulate motion and visualize trajectories

### Tools
- Python with NumPy and Matplotlib
- Optional MATLAB or Simulink for cross-checking

### Responsibilities
**Mechanical**
- Kinematic chain
- Physical feasibility
- Joint constraints

**Data**
- Forward kinematics implementation
- Visualization
- Error metrics

### Outputs
- Simulated motion to target poses
- Plots of joint angles and end-effector paths

## Phase 1: Physical Arm and Instrumentation
**Timeline:** Weeks 3-5

### Scope
- Build a 3 DOF arm with stepper motors
- Add hard stops and safety limits
- Instrument motion with encoders or step counting
- Log every run automatically

### Logged Signals
- Motor step counts
- Timestamps
- End-effector estimate from kinematics

### Responsibilities
**Mechanical**
- CAD
- Gear ratios
- Mounting and stiffness

**Data**
- Serial data ingestion
- Logging schema
- Real-time plotting

### Outputs
- Repeatable motion
- Per-run datasets

## Phase 2: Trajectory Optimization
**Timeline:** Weeks 6-8

### Scope
- Optimize motion between start and end poses
- Compare trajectories using smoothness, time, overshoot, and an energy proxy

### Methods
- Cost functions
- Gradient-free optimization
- Parameter sweeps

### Responsibilities
**Mechanical**
- Physical cost definitions
- Constraint modeling

**Data**
- Optimization algorithms
- Experiment automation
- Result comparison plots

### Outputs
- Baseline versus optimized trajectories
- Quantitative comparison plots

## Phase 3: Error Modeling and Compensation
**Timeline:** Months 3-4

### Scope
- Model systematic joint bias
- Estimate backlash
- Correct timing or calibration errors

### Data
- Commanded pose versus measured pose
- Error vectors
- Trial history

### Responsibilities
**Mechanical**
- Interpret physical error sources
- Validate proposed corrections

**Data**
- Regression or compensation models
- Error prediction
- Performance analysis

### Outputs
- Accuracy improvement across repeated trials
- Error model performance curves

## Phase 4: Reinforcement Learning
**Timeline:** Months 5-6  
**Status:** Optional

### Scope
- Use a limited state and action space
- Train against accuracy, time, and smoothness objectives
- Keep firmware-side safety constraints in place

### Preconditions
- Stable control
- Reliable logging
- Validated simulator or safe constrained hardware loop

### Outputs
- Policy comparison against hand-tuned or optimized controllers

## Data Collection
Microcontroller-side logging should record step counts, timestamps, and commanded targets. Host-side software should collect, store, and plot each run without manual timing or hand labeling.

## Initial Recommended Scope
Start with:
- 3 DOF
- Stepper motors
- Automatic logging
- No vision system in early phases

If Phases 0-2 are complete and measured well, the project already supports expansion into calibration, optimization, and learning.
