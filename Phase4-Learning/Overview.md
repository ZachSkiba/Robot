## 🔴 Phase 4 — Reinforcement Learning on Real Hardware (Capstone Phase)

**Duration:** ~6–8 weeks  
**Goal:** The robotic arm learns a control policy that outperforms hand-tuned and regression-based controllers.  

> This is the phase that turns your project into a top-tier ML + Robotics system.

---

### 🔹 Phase 4 Outcomes
- Formal RL problem definition (state, action, reward)  
- Safe real-world RL loop (no “YOLO” training)  
- Learned policy that improves task performance  
- Clear comparison:  
  - classical control  
  - learned correction (Phase 3)  
  - RL policy  
- Internship-level demo + report  

---

### 🧩 Step-by-Step Plan (with Roles)

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

**🔁 Interaction**
- Reward shaping is joint work — this is critical

---

#### STEP 4.2 — Build a Simulator from Real Data (Days 5–10)

> This avoids destroying hardware and is very resume-strong.

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

**🔁 Interaction**
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

**🔁 Interaction**
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

**🔁 Interaction**
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

**🔁 Interaction**
- Jointly answer:  
> “Does RL actually help?”  
- If yes → massive win  
- If no → still a strong scientific result

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

**🎯 Resume Sentence:**  
> “We trained and deployed a reinforcement learning policy on a real robotic arm.”  
> That is elite-tier for internships.

---

### 🧠 Role Balance (Phase 4)

| Area                 | Zach (DS) | Nicholas (MechE) |
|----------------------|-----------|----------------|
| RL algorithms         | ✅        | ➖             |
| Simulator             | ✅        | ➖             |
| Reward design         | ✅        | ✅             |
| Safety constraints    | ➖        | ✅             |
| Real-world deployment | ➖        | ✅             |
| Evaluation            | ✅        | ✅             |

> Both of you are essential every step.
