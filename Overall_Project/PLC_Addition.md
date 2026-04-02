# Pick-and-Place Cycle with PLC as Master Controller

## The Concept

Your 6-DOF arm is already controlled by Python/Teensy. The upgrade is adding OpenPLC on the Mega 2560 as an **industrial-style supervisory controller** that manages the overall machine cycle — exactly how real robot cells work in factories.

In every real manufacturing cell at Daifuku, CNH, or Caterpillar:

- The PLC is the master — it manages states, safety, and sequencing
- The robot controller executes motion
- They talk to each other via I/O signals

You'd be replicating that architecture exactly, at your desk, for free.

---

## What It Looks Like Physically

```
[Limit Switch — Part Present]
         ↓
    [Mega 2560 / OpenPLC]  ←→  [E-Stop Button]
         ↓ (digital signal)
    [Teensy 4.1]
         ↓
    [6-DOF Arm executes pick and place]
         ↓ (motion complete signal back)
    [Mega 2560 / OpenPLC]
         ↓
    [Cycle counter increments]
    [Ready for next part]
```

All hardware already in your inventory.

---

## Hardware Used

| Component | From Your Inventory | Role |
|-----------|-------------------|------|
| Mega 2560 | ✅ Already owned | PLC brain running OpenPLC |
| Teensy 4.1 | ✅ Already owned | Motion controller for arm |
| KW12-3 Limit Switches | ✅ Already owned | Part present sensor + home detection |
| E-Stop Button | ✅ Already owned | Safety input to PLC |
| TMC2209 + NEMA 17s | ✅ Already owned | Arm joints |
| AS5600 Encoders | ✅ Already owned | Joint feedback |
| 24V PSU | ✅ Already owned | Main power |
| Capacitors + TVS Diodes | ✅ Already owned | Noise protection |

**Total additional cost: $0**

---

## PLC Logic — Five-State Machine

All programmed in Ladder Logic on the Mega 2560 via OpenPLC:

1. **IDLE** — waiting for part present signal from limit switch
2. **CYCLE START** — sends "go" signal to Teensy, starts cycle timer
3. **IN CYCLE** — monitors watchdog timer; if Teensy doesn't complete motion in time → FAULT
4. **CYCLE COMPLETE** — increments counter, logs cycle, returns to IDLE
5. **FAULT / E-STOP** — cuts enable signal to all drivers, requires manual reset

This state machine is exactly what a Daifuku engineer writes every day. It demonstrates industrial control logic from first principles.

---

## Why This Project Wins Interviews

It demonstrates five things simultaneously that no other single project can:

- **PLC programming** — Ladder Logic, state machine, I/O handling
- **Robot control** — 6-DOF kinematics, trajectory planning, Teensy firmware
- **System integration** — two controllers talking to each other via I/O signals
- **Safety engineering** — E-stop authority, watchdog timer, fault handling
- **Industrial architecture** — replication of a real manufacturing cell layout

When a Daifuku or CNH interviewer asks *"have you worked with industrial robot cells?"* you say:

> *"I built one. PLC as master controller handling cell state and safety, separate motion controller for the arm, part detection via limit switches, E-stop with hardware-dominant authority, cycle counting and fault logging. Here's the GitHub and the video."*

---

## GitHub Deliverables

Three things that make this portfolio-ready:

1. **Video** — arm executing a full pick-and-place cycle, E-stop test, fault recovery. 60–90 seconds, clean and edited
2. **Architecture diagram** — one page showing PLC ↔ Teensy ↔ hardware signal flow
3. **README** — explains the industrial analogy explicitly. Don't make recruiters guess why it matters

---

## Build Timeline

| Week | Task |
|------|------|
| 1 | Learn OpenPLC basics, simulate state machine in editor |
| 2 | Flash Mega 2560, wire limit switches and E-stop, test I/O |
| 3 | Write and validate full 5-state Ladder Logic program |
| 4 | Integrate Mega ↔ Teensy signal handshake |
| 5 | Full cycle testing, fault injection testing, E-stop validation |
| 6 | Film demo, write README, push to GitHub |

**Six weeks. One project. Closes the PLC gap, elevates the arm from "cool robot" to "industrial robot cell," and directly maps to every employer on the target list.**
