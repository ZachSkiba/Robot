# Mini-Project Strategy

## Purpose
Mini-projects are short validation exercises used to de-risk the full arm build. Each one should answer a narrow technical question, produce a measurable result, and stop once the objective is met.

## Mini-Project A: Single-Axis Joint
**Duration:** 5-7 days  
**Priority:** Required

### Scope
- One motor
- One controller
- One feedback loop
- One Python script for commands, logging, and plots

### Deliverables
- Position command interface
- Logged response data
- Error-versus-time plot

### Stop Criteria
- The joint reaches commanded positions repeatably
- Response data is logged
- Error can be plotted and reviewed

### Out of Scope
- Multi-axis coordination
- Machine learning
- Hardware redesign after basic functionality is proven

### Reuse
- This setup can become Joint 1 of the arm

## Mini-Project B: Teleoperation to Motor
**Duration:** 3-5 days  
**Priority:** Recommended

### Scope
- PS5 controller or equivalent input device
- Manual velocity control of one motor
- Logging of user input and motor response

### Deliverables
- Teleoperation interface
- Logged controller and motor data
- Replay of one recorded motion

### Stop Criteria
- Manual motion is smooth and bounded
- At least one recorded motion can be replayed

### Value
- Validates human-in-the-loop control
- Produces trajectory data for later analysis
- Exposes actuator saturation and limit handling

## Mini-Project C: Two-Link Simulation
**Duration:** 2-3 days  
**Priority:** Optional

### Scope
- Python-only model
- Two joints
- Forward and inverse kinematics
- Basic visualization

### Stop Criteria
- Forward kinematics produces expected positions
- Inverse kinematics works for reachable targets
- Plots and animations match the model

### When to Use It
- Use this when hardware work is blocked or when kinematic intuition is missing

## Avoid These Expansions
- Full arm construction before single-axis validation
- Reinforcement learning before stable control and logging
- Long theory-first detours without hardware or simulation output
- Large side projects that do not reduce integration risk

## Suggested Sequence
**Week 1**
- Complete Mini-Project A
- Split hardware and data tasks, then swap once

**Week 2**
- Complete Mini-Project B, or
- Start the first physical arm phase if Mini-Project A is stable

## Success Condition
At the end of the pre-project stage, the team should be able to command one joint, measure the result, and review the logged response.
