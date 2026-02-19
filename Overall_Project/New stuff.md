# Robot Design & Software Architecture Notes

## Mechanical Design
- Use **pulleys and belts** for all joints **except the gripper**.  
- The **gripper** uses a **worm drive** (self-locking).

---

## Software / OS Architecture
- **Windows**: Host OS, hardware owner, and CAD workstation.  
- **Ubuntu (WSL2)**: Robotics workstation, runs all control and trajectory software.  
- **WSL2 Usage**: Run **control software** inside WSL2.  
- **Windows Usage**: Handles **hardware connection**, USB stack, and CAD.

---

## How a Command Actually Moves the Robot

1. **Python (WSL2)** computes a trajectory segment.  
2. Python **serializes the segment** into a binary packet.  
3. The packet crosses the **WSL → Windows boundary**.  
4. **Windows USB stack** sends the packet to the Teensy.  
5. **Teensy** validates, buffers, and executes the motion autonomously.

---

## Latency Impact
- Step 3 (crossing WSL → Windows) adds roughly **0.1–0.3 ms**.  
- Completely invisible to the control loop due to **buffering**.  
- The motor and Teensy **never know WSL exists**.

---

## Hardware Updates
- New motor drives and components added to the **materials list**.
- New encoders are better

# Homing 540° Joints

## Problem
- Joint spins up to 540° (>360°)
- Need repeatable home without obstruction

## Solution
Use a **non-obstructive physical reference**:

| Method | Description | Pros | Cons |
|--------|------------|------|------|
| Lever switch + cam | Small tab triggers switch once per turn | Cheap, robust | Needs careful placement |
| Hall effect sensor + magnet | Magnet passes near sensor at home | Contactless, fast, no obstruction | Must secure magnet/sensor |
| Optical / IR flag | Small flag interrupts beam at home | Contactless, precise | Needs line-of-sight, dust sensitive |

> **Avoid:** putting a hard switch in the path of normal motion

## Homing Sequence
1. Slowly rotate joint toward reference
2. Detect sensor trigger
3. Back off slightly
4. Rotate slowly to re-trigger → define home
5. Set encoder + stepper as zero

## Mechanical Tips
- Tab/magnet should be small and rigid  
- Sensor must have tolerance to avoid misses  
- Ensure nothing else on the joint passes near it  
- Trigger only occurs at home position  

**Key Takeaway:**  
The reference **does not block normal motion**; it only triggers at home to provide a repeatable zero.
