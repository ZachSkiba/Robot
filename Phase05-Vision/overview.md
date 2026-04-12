# 🔵 Phase 5 — Vision-Guided Manipulation (Autonomy Layer)

**Duration:** ~6–10 weeks (can be extended indefinitely)  
**Goal:** The robotic arm perceives its environment and autonomously decides what to do, not just how to move.  

> This is where your system stops being “a robot arm” and becomes an intelligent robotic system.

---

### 🔹 Phase 5 Outcomes
- Camera-based perception pipeline  
- Object detection / localization  
- Hand–eye calibration  
- Closed-loop vision → motion  
- Autonomous task execution (single-step)  
- End-to-end demo  

**🎯 You can say:**  
> “We built a vision-guided robotic manipulator with learned control.”  
> Very strong for both MechE + DS.

---

### 🧩 Step-by-Step Plan (with Roles)

#### STEP 5.1 — Add Vision Hardware & Calibration (Days 1–7)

**Together**
- Decide camera setup:  
  - Fixed overhead camera **or**  
  - Wrist-mounted camera (harder, more impressive)  

**Nicholas (MechE)**
- Design & mount camera bracket  
- Ensure rigidity (no vibration)  
- Measure camera position relative to arm  

**Zach (DS)**
- Set up camera feed in Python  
- Handle frame capture & synchronization  
- Store images with timestamps  

**🔁 Interaction**
- Jointly validate:  
  - field of view  
  - resolution  
  - latency  

---

#### STEP 5.2 — Hand–Eye Calibration (Days 8–14)

> This is huge resume value.

**Together**
- Define coordinate frames:  
  - camera  
  - base  
  - end-effector  

**Zach**
- Implement calibration math  
- Solve camera → world transform  
- Validate reprojection error  

**Nicholas**
- Perform physical calibration motions  
- Ensure repeatable poses  
- Validate geometric correctness  

**🔁 Interaction**
- Verify:  
> “When the camera sees X, the arm knows where X is.”

---

#### STEP 5.3 — Object Detection & Localization (Days 15–22)

**Together**
- Choose task objects:  
  - blocks  
  - cups  
  - trash-like objects (future)  

**Zach**
- Implement perception:  
  - color segmentation (baseline) **or**  
  - simple CNN detector  
- Output object pose in world frame  

**Nicholas**
- Ensure lighting robustness  
- Adjust physical setup for reliability  
- Validate grasp feasibility  

**🔁 Interaction**
- Trade off:  
  - ML complexity vs reliability  

---

#### STEP 5.4 — Vision → Motion Integration (Days 23–30)

**Together**
- Define pipeline:  
  - detect object  
  - compute target pose  
  - plan motion  
  - execute safely  

**Zach**
- Integrate perception with planner  
- Handle uncertainty & confidence  
- Reject low-confidence detections  

**Nicholas**
- Validate physical feasibility  
- Tune approach angles & heights  
- Prevent collisions  

**🔁 Interaction**
> This is where software meets physics.

---

#### STEP 5.5 — Autonomous Task Demo (Days 31–40)

**Together**
- Pick one clean autonomous task:  
  - pick and place object  
  - sort objects by color  
  - place object in bin  

**Zach**
- Measure success rate  
- Log failure cases  
- Improve robustness  

**Nicholas**
- Tune mechanics for consistency  
- Improve gripper alignment  
- Reduce variance  

**🔁 Interaction**
- Iterate until:  
> “It works reliably, not just once.”

---

#### STEP 5.6 — Phase 5 Deliverables (Days 41–45)

**Together**
- Produce:  
  - End-to-end demo video  
  - Clear system diagram  
  - README explaining:  
    - perception  
    - control  
    - learning  
    - limitations  

**🎯 Final Statement:**  
> “This robotic system autonomously perceives, plans, and acts.”

---

### 🧠 Role Balance (Phase 5)

| Area                 | Zach (DS) | Nicholas (MechE) |
|----------------------|-----------|----------------|
| Vision algorithms     | ✅        | ➖             |
| Calibration math      | ✅        | ➖             |
| Mechanical mounting   | ➖        | ✅             |
| Motion feasibility    | ➖        | ✅             |
| System integration    | ✅        | ✅             |
| Evaluation            | ✅        | ✅             |

> Still fully collaborative.
