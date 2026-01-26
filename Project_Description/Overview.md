# 🦾 Robotic Arm Project — Joint Roadmap

## Core Principle
**Every phase must produce data, metrics, and plots.**  
That’s what turns *“cool robot”* → *“serious engineering project.”*

---

## 🟢 Phase 0 (Weeks 1–2): Architecture + Simulation (No Hardware Yet)

### What You Build
Define:
- DOFs (start with **3 DOF**, cap at **5 DOF max**)  
- Joint limits  
- Link lengths  

Then:
- Build kinematics model  
- Simulate arm motion  

### Tools
- Python (NumPy, Matplotlib)  
- Optional: MATLAB / Simulink for verification  

### Roles (Both Involved)

**MechE**
- Kinematic chain  
- Physical feasibility  
- Joint constraints  

**Data Science**
- Forward kinematics equations  
- Visualization  
- Error metrics  

### 🎯 Output
- Simulated arm moving to targets  
- Plots of joint angles & end-effector paths  

✅ **Resume value:** *Robotic kinematics + simulation*

---

## 🟡 Phase 1 (Weeks 3–5): Physical Arm + Instrumentation

### What You Build
- 3 DOF arm with stepper motors  
- Hard stops + safety limits  
- Encoders or step counting  
- Automatic logging  

### Sensors (Simple but Powerful)
- Motor step counts  
- Time stamps  
- End-effector estimate (via kinematics)  

⚠️ **You do NOT manually time anything.**  
The microcontroller logs everything.

### Roles

**MechE**
- CAD  
- Gear ratios  
- Mounting & stiffness  

**Data Science**
- Serial data ingestion  
- Logging schema (CSV / SQLite)  
- Real-time plotting  

### 🎯 Output
- Arm moves repeatably  
- Data logged every run  

✅ **Resume value:** *Robotic hardware + telemetry pipeline*

---

## 🔵 Phase 2 (Weeks 6–8): Trajectory Optimization (No ML Yet)

### What You Optimize
Given:
- Start pose  
- End pose  

Optimize:
- Smoothness  
- Time  
- Overshoot  
- Energy proxy  

### Techniques (Resume Gold)
- Cost functions  
- Gradient-free optimization  
- Parameter sweeps  

### Roles

**MechE**
- Physical cost definitions  
- Constraint modeling  

**Data Science**
- Optimization algorithms  
- Experiment automation  
- Result comparison plots  

### 🎯 Output
- “Optimized” motion vs naïve motion  
- Clear quantitative improvement  

✅ **Resume value:** *Optimization applied to real robotic systems*

---

## 🟣 Phase 3 (Months 3–4): Learning From Error (Intro ML)

### What Learns
- Systematic joint bias  
- Backlash compensation  
- Timing correction  

> This is **not RL yet** — it’s smarter and cleaner.

### Data Collected Automatically
- Commanded vs actual pose  
- Error vectors  
- Trial number  

### Roles

**MechE**
- Interpret physical error sources  
- Validate realism  

**Data Science**
- Regression models  
- Error prediction  
- Performance curves  

### 🎯 Output
- Arm improves accuracy over time  
- Learning curves  

✅ **Resume value:** *Data-driven control improvement*

---

## 🔴 Phase 4 (Months 5–6): RL (Optional but Nuclear)

### RL Objective (Simple, Impressive)
- **State:** joint angles + target  
- **Action:** trajectory parameters  
- **Reward:** accuracy – time – jerk  

### Why This Works
- Small state space  
- Safe actions  
- Real hardware + simulation  

### Roles

**MechE**
- Reward shaping  
- Stability & safety  

**Data Science**
- RL implementation  
- Training pipeline  
- Evaluation  

### 🎯 Output
- Learned policy beats hand-tuned control  

✅ **Resume value:** *Reinforcement learning on physical robot*

---

## 🔧 Data Collection (Key Question You Asked)

### How Data Is Collected (Automatically)
Microcontroller logs:
- Step counts  
- Timestamps  
- Commanded targets  

Python listens over USB / WiFi.

Every run saved:
- No human timing  
- No manual labels  

You press **run**, the system records everything.  
This is how **real robotics labs** work.

---

## 🧠 Why This Is Perfect for BOTH of You

| Area | MechE | Data Science |
|----|----|----|
| Design | ✅ | ➖ |
| Control | ✅ | ✅ |
| Optimization | ✅ | ✅ |
| ML | ➖ | ✅ |
| Systems | ✅ | ✅ |

**No one gets sidelined.**

---

## Final Recommendation

Start with:
- **3 DOF**
- **Stepper motors**
- **Heavy logging**
- **No vision**

If you nail **Phases 0–2**, you already have:
- A strong project  
- A clean expansion path  
- Something interviewers respect  
