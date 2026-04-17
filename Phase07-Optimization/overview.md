# Phase 7 - Research-Level Optimization and Evaluation

**Duration:** Open-ended (4–12+ weeks)  
**Goal:** Extend the system with stronger modeling, robustness testing, and system-level evaluation.  

## Outcomes
- System-level optimization  
- Learning + classical methods combined  
- Robustness to uncertainty  
- Quantitative evaluation  
- Publication-style documentation  
- Technical documentation and benchmark results  

---

## Plan

#### STEP 7.1 — System Identification & Modeling (Weeks 1–2)

**Together**
- Define what to model:  
  - motor dynamics  
  - joint friction  
  - load effects  
  - delay / noise  

**Nicholas (MechE)**
- Design excitation experiments  
- Interpret physical parameters  
- Validate model realism  

**Zach (DS)**
- Fit models from data  
- Compare linear vs nonlinear models  
- Quantify model error  

**Coordination**
- Align model structure with measured physical behavior.

---

#### STEP 7.2 — Hybrid Control (Classical + Learning) (Weeks 3–5)

**Together**
- Define control stack:  
  - classical controller (PID / MPC)  
  - learning layer for residuals or tuning  

**Zach**
- Train learning components  
- Compare RL vs optimization  
- Measure stability & convergence  

**Nicholas**
- Guarantee safety bounds  
- Analyze stability margins  
- Validate real-world behavior  

**Coordination**
- Keep learned components bounded by explicit safety and stability constraints.

---

#### STEP 7.3 — Robustness & Generalization (Weeks 6–7)

**Together**
- Test under:  
  - different payloads  
  - lighting changes  
  - sensor noise  
  - slight hardware changes  

**Zach**
- Analyze failure modes  
- Quantify robustness metrics  
- Improve generalization  

**Nicholas**
- Physically induce variations  
- Identify mechanical sensitivities  
- Improve repeatability  

---

#### STEP 7.4 — Optimization at the System Level (Weeks 8–9)

**Optimize**
- energy usage  
- task time  
- wear / smoothness  
- success probability  

**Zach**
- Multi-objective optimization  
- Pareto front analysis  
- Data-driven tradeoffs  

**Nicholas**
- Interpret tradeoffs physically  
- Suggest mechanical improvements  
- Validate feasibility  

---

#### STEP 7.5 — Evaluation & Benchmarking (Weeks 10–11)

**Together**
- Define metrics:  
  - accuracy  
  - speed  
  - success rate  
  - robustness  

**Zach**
- Statistical analysis  
- Plots, tables, ablations  

**Nicholas**
- Experimental protocol  
- Repeatability checks  
- Hardware consistency  


---

#### STEP 7.6 — Documentation and Presentation (Weeks 12+)

**Together**
- Create:  
  - clean GitHub repo  
  - architecture diagrams  
  - short technical write-up  
  - demo video(s)  

**Zach**
- ML / control explanations  
- Results visualization  
- README clarity  

**Nicholas**
- CAD renders  
- Mechanical diagrams  
- Build documentation  

## Role Split

| Area                    | Zach (DS) | Nicholas (MechE) |
|-------------------------|-----------|----------------|
| Modeling & learning      | ✅        | ➖             |
| Physical interpretation  | ➖        | ✅             |
| Optimization             | ✅        | ➖             |
| Experimental design      | ➖        | ✅             |
| Evaluation               | ✅        | ✅             |
| Presentation             | ✅        | ✅             |
