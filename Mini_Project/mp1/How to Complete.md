# Mini-Project C → Mini-Project 3 Substrate (Governed System Upgrade)

## Reclassification (Explicit)

### Old framing (insufficient)
> **“Build kinematic intuition”**

This framing is **educational**, not governed.  
It produces insight, not authority.

### Correct framing
> **“Provide a controllable, adversarial motion source to validate replay, judgment, and rejection logic.”**

The **2-link arm is not the goal**.  
It is **test ammunition** for Mini-Project 3.

---

## What Mini-Project C Already Covers (Mapped)

| Old C Requirement | MP3 Status |
|------------------|------------|
| FK correctness | ✅ prerequisite |
| IK correctness | ✅ prerequisite |
| Visualization | ✅ already exceeded |
| Smooth trajectories | ⚠️ insufficient |
| “Looks right” | ❌ irrelevant |

These provide **inputs**, not **judgment**.

---

## What MUST Be Added for MP3 Compliance

Below are **only the missing items**, scoped strictly to the 2-link Python arm.

---

## 1. Trajectory as a First-Class Object

**Problem:**  
Angles alone are anonymous and ungovernable.

**Requirement:**  
Define an explicit **trajectory contract**.

``python
trajectory = {
    "id": "...",
    "source": "scripted | human | adversarial",
    "dt": 0.002,
    "states": [...],
    "limits": {...}
}

## Why This Is Mandatory

- **MP3 judges intent + execution**
- Without metadata, behavior cannot be governed
- Anonymous arrays = **automatic MP3 failure**

---

## 2. Deliberately Bad IK & Trajectories (Red-Team)

### Problem
Your IK is trying to be *correct*.

That is insufficient.

### Mandatory Adversarial Cases
You must intentionally generate:

- IK branch flips
- Discontinuous solutions
- Near-singularity motion
- Elbow “snap” transitions
- Joint limit grazing

### Required Proof
You must demonstrate that:

- Replay **catches** these cases
- Judgment logic **rejects** them
- Visualization **exposes** the failure modes

If the system only sees “good math,” it is **untested**.

---

## 3. Kinematic Invariant Checks (Beyond Error)

### Problem
Spatial error alone is **not a safety metric**.

### Required Invariants (Minimum)

- **Joint continuity**  
  `|θ(t) − θ(t−1)| < Δθ_max`
- Velocity bounds
- Acceleration bounds
- Workspace constraints
- Forbidden configurations (self-collision proxy)

### Invariant Requirements
Each invariant must:
- Produce a boolean
- Emit a timestamp
- Feed directly into verdict logic

A solution can be mathematically valid and **operationally unsafe**.  
**MP3 must reject it.**

---

## 4. Time-Domain Validation

### Problem
Traditional Mini-Project C ignores time.  
**MP3 does not.**

### Required
The 2-link simulation must:

- Enforce fixed `dt`
- Detect `dt` violations
- Flag jitter
- Reject non-uniform sampling

A perfect FK/IK solution with bad timing is a **FAIL**.

This is where most simulators collapse.

---

## 5. Command Source Arbitration (Python-Level)

### Problem
All commands currently have implicit authority.

### Required Command Sources (Minimum)

- `scripted`
- `human_sim` (noise, jitter)
- `replay`

### Arbitration Requirements
They must:
- Compete for authority
- Be logged distinctly
- Be judgeable independently

If “human input” can bypass limits even in simulation, **MP3 is invalid**.

---

## 6. Machine-Readable Verdict Output

### Problem
Visuals and printed output do not enforce governance.

### Required Per Run
Each run must emit:

- Verdict JSON
- Failure list
- Severity
- Root cause attribution

### Example
``json
{
  "run_id": "2link_run_04",
  "overall": "FAIL",
  "failures": [
    {
      "type": "JOINT_CONTINUITY",
      "joint": "elbow",
      "t_start": 2.14,
      "severity": "CRITICAL"
    }
  ]
}

# Mini-Project 3 (MP3) — Governance & Failure Enforcement Requirements

> **No file → no automation → no MP3.**

---

## 7. Early Stop Conditions (Non-Negotiable)

### Problem
Traditional simulators always finish trajectories, even when violations occur.  
This behavior **invalidates governance**.

### Required Behavior
- Motion **halts immediately** on first violation  
- Replay **marks the exact termination point**  
- Verdict **records preemption** (cause + timestamp)

> If the simulator continues after a violation, **it is lying**.

---

## Minimal MP3-Compliant Upgrade Summary

### You do **NOT** need:
- More joints  
- More math  
- More visuals  

### You **DO** need:
- Intent metadata  
- Adversarial trajectories  
- Explicit invariants  
- Time-domain enforcement  
- Command arbitration  
- Verdict files  
- Early termination logic  

---

## Final Classification Statement

Mini-Project C is **complete** *only when* the 2-link arm can be used to:

- **Intentionally fail the system**, and  
- The system **correctly detects, halts, and rejects** the run.

### If it only demonstrates:
- Correct FK  
- Correct IK  
- Smooth plots  

Then it is **educational**, not **governed**, and **does not count as Mini-Project 3**.

