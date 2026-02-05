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
