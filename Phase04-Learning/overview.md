# Phase 4 - Reinforcement Learning on Real Hardware

**Duration:** ~6–8 weeks  
**Goal:** The robotic arm learns a control policy that outperforms hand-tuned and regression-based controllers.  

## Outcomes
- Formal RL problem definition (state, action, reward)  
- Safe real-world RL loop (no “YOLO” training)  
- Learned policy that improves task performance  
- Clear comparison:  
  - classical control  
  - learned correction (Phase 3)  
  - RL policy  
- Demo and report  

---

## Plan

#### STEP 4.1 — Define the RL Problem (Days 1–4)

**Together**
- Lock down one simple but meaningful task:  
  - Reach a target point  
  - Trace a line  
  - Minimize endpoint error under disturbance  
- Define:  
  - State: joint angles, velocities, error  
  - Action: joint deltas or velocity commands  
  - Reward: accuracy − energy − jerk − time  

**Zach (DS)**
- Formalize MDP mathematically  
- Normalize states & rewards  
- Ensure Markov property  

**Nicholas (MechE)**
- Verify actions are physically safe  
- Define actuator limits & constraints  
- Sanity-check reward realism  

**Coordination**
- Reward shaping is joint work — this is critical

---

#### STEP 4.2 — Build a Simulator from Real Data (Days 5–10)

**Together**
- Decide fidelity level:  
  - Learned dynamics (from Phase 3 data)  
  - Simple physics + learned residuals  

**Zach**
- Implement simulation environment (Gym-style)  
- Validate sim vs real trajectories  
- Add noise & delay models  

**Nicholas**
- Validate physical plausibility  
- Identify where sim diverges from the model  

**Coordination**
- Iterate until simulation ≈ real enough to transfer

---

#### STEP 4.3 — Train RL in Simulation (Days 11–20)

**Zach**
- Implement RL algorithm: PPO or SAC (recommended)  
- Train policies  
- Track convergence & stability  

**Nicholas**
- Monitor trajectory realism  
- Reject unsafe learned behaviors  
- Suggest reward adjustments  

**Coordination**
- Tight feedback between learning and physics

---

#### STEP 4.4 — Safe Sim-to-Real Transfer (Days 21–26)

**Together**
- Define safety envelope:  
  - action clipping  
  - emergency stop  
  - slow execution mode  

**Zach**
- Deploy policy with conservative gains  
- Log real-world performance  

**Nicholas**
- Observe hardware stress  
- Approve incremental expansion of limits  

**Coordination**
- Policy is never blindly trusted

---

#### STEP 4.5 — Compare Against Baselines (Days 27–32)

**Zach**
- Quantitative comparison:  
  - error  
  - time  
  - smoothness  
- Generate plots & tables  

**Nicholas**
- Qualitative assessment:  
  - stability  
  - wear  
  - robustness  

**Coordination**
- Jointly evaluate whether RL improves performance relative to the baselines.

---

#### STEP 4.6 — Phase 4 Deliverables (Days 33–40)

**Together**
- Produce:  
  - Clean repo with:  
    - simulator  
    - RL training  
    - deployment code  
  - Short demo video  
  - Clear README:  
    - why RL  
    - how it was done safely  
    - what worked / didn’t  

## Role Split

| Area                 | Zach (DS) | Nicholas (MechE) |
|----------------------|-----------|----------------|
| RL algorithms         | ✅        | ➖             |
| Simulator             | ✅        | ➖             |
| Reward design         | ✅        | ✅             |
| Safety constraints    | ➖        | ✅             |
| Real-world deployment | ➖        | ✅             |
| Evaluation            | ✅        | ✅             |
