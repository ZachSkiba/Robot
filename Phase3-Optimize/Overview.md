## 🟣 Phase 3 — Learning From Error (Data-Driven Control)

**Duration:** ~4–6 weeks  
**Goal:** The arm systematically improves accuracy and repeatability by learning from its own execution data.  

> This is where your project clearly becomes robotics + data science, not just control.

---

### 🔹 Phase 3 Outcomes
- Measured commanded vs actual behavior  
- Identified systematic errors (bias, backlash, timing)  
- Learned correction models  
- Demonstrated performance improvement over time  
- Clean learning curves + plots  

---

### 🧩 Step-by-Step Plan (with Roles)

#### STEP 3.1 — Add State Feedback (Days 1–4)

**Together**
- Decide how you’ll measure “actual” state:  
  - Encoders **or**  
  - Improved estimation (step count + homing)  

**Nicholas (MechE)**
- Mount encoders (if used)  
- Ensure alignment & mechanical robustness  
- Identify sources of physical error:  
  - backlash  
  - flex  
  - missed steps  

**Zach (DS)**
- Integrate encoder data into logging  
- Synchronize timestamps  
- Validate signal quality  

**🔁 Interaction**
- Compare measured vs expected motion  
- Agree on what errors are real vs noise  

---

#### STEP 3.2 — Define Error Models (Days 5–7)

**Together**
- Define:  
  - What error means:  
    - joint error  
    - end-effector error  
  - When it’s measured (end of motion, during motion)  

**Zach**
- Formalize error vectors  
- Define features:  
  - target pose  
  - joint angles  
  - trajectory parameters  

**Nicholas**
- Sanity-check physical meaning:  
  - “Does this feature cause that error?”  
- Suggest simplifications  

**🔁 Interaction**
- Iterate until the model inputs make physical sense  

---

#### STEP 3.3 — Data Collection Campaign (Days 8–14)

**Zach**
- Automate experiments:  
  - many targets  
  - many trajectories  
- Log:  
  - commands  
  - actual state  
  - error  

**Nicholas**
- Monitor hardware health  
- Ensure repeatability  
- Adjust mechanical issues if needed  

**🔁 Interaction**
- Decide when dataset is “good enough”  
- Reject bad data intentionally  

---

#### STEP 3.4 — Learn Error Corrections (Days 15–22)

**Together**
- Decide learning approach:  
  - Linear regression  
  - Polynomial model  
  - Simple neural net (small)  

**Zach**
- Train models to predict error  
- Validate with held-out data  
- Plot learning curves  

**Nicholas**
- Interpret learned behavior:  
  - Is the model compensating for real physics?  
  - Flag unsafe corrections  

**🔁 Interaction**
- Keep learning conservative and stable  
- Reject black-box magic  

---

#### STEP 3.5 — Apply Corrections & Evaluate (Days 23–27)

**Zach**
- Apply learned correction to commands  
- Run before/after comparisons  
- Generate performance plots  

**Nicholas**
- Validate physically:  
  - smoother?  
  - more accurate?  
  - safer?  

**🔁 Interaction**
- Jointly answer:  
> “Does learning actually improve the robot?”  
- If yes → Phase 3 is a success

---

#### STEP 3.6 — Phase 3 Deliverables (Days 28–30)

**Together**
- Prepare:  
  - README:  
    - error sources  
    - learning approach  
  - Plots:  
    - error vs trial  
    - before vs after accuracy  
  - Short demo video  

**🎯 Resume Sentence:**  
> “We implemented data-driven error correction on a physical robotic arm.”  
> That’s extremely strong.

---

### 🧠 Role Balance (Phase 3)

| Area                   | Zach (DS) | Nicholas (MechE) |
|------------------------|-----------|----------------|
| Data pipeline           | ✅        | ➖             |
| Learning models         | ✅        | ➖             |
| Physical error analysis | ➖        | ✅             |
| Safety & constraints    | ➖        | ✅             |
| Evaluation              | ✅        | ✅             |

> Still fully collaborative.
