# Mini-Projects – System Overview (Phase 0)

## **Purpose**
The Phase 0 system is designed to **validate core robotics skills** before building the full robotic arm.  
It provides a simple, modular architecture to test **motors, sensors, controllers, and software**, minimizing risk and complexity.

---

## **System Components**

### **1. Hardware**
- **Motor (Servo or Stepper)**  
  - Provides actuation for single-axis movement.  
  - Behaves as the primary controllable joint in Mini-Project A and B.  
- **Sensor (Encoder / Step Counter)**  
  - Provides real-time feedback on joint position or steps.  
  - Used for closed-loop control in Mini-Project A.  
- **Microcontroller (Arduino Mega / ESP32)**  
  - Executes motor commands.  
  - Reads sensor data.  
  - Interfaces with Python scripts or joystick input.  
- **Motor Driver (if needed)**  
  - Interfaces microcontroller with motor power requirements.  
  - Ensures safe current delivery to the motor.  

---

### **2. Software**
- **Python Scripts**  
  - Send commands to motor (Mini-Project A).  
  - Log sensor and motor data.  
  - Plot error vs time for PID tuning.  
  - Interface with joystick (Mini-Project B).  
- **Microcontroller Firmware**  
  - Implements PID control loops (Mini-Project A).  
  - Reads joystick or sensor inputs.  
  - Sends data to Python for logging/visualization.  
- **Optional Simulation (Mini-Project C)**  
  - Python-only FK/IK simulation for 2-link arm.  
  - Visualizes joint angles and reachable workspace.  

---

## **System Flow – Mini-Project A**
1. Python script sends position command → microcontroller.  
2. Microcontroller outputs PWM/current to motor driver.  
3. Motor moves → sensor measures position.  
4. Microcontroller compares sensor reading → PID calculates correction.  
5. Feedback loop continues until joint reaches commanded position.  
6. Data logged and plotted in Python for analysis.  

---

## **System Flow – Mini-Project B**
1. Joystick input (PS5 controller) sent to Python/microcontroller.  
2. Input mapped to motor velocity or position commands.  
3. Motor moves → sensor feedback optional for logging.  
4. Data logged: joystick vs motor response.  
5. Trajectories can be replayed for analysis.  

---

## **System Flow – Mini-Project C (Optional)**
1. Python simulates 2 joints in software.  
2. Forward kinematics calculates end-effector position.  
3. Inverse kinematics calculates joint angles for target points.  
4. Motion visualized in plots to build intuition for future hardware design.  

---

## **Key Design Principles**
- **Modularity:** Each mini-project can be completed independently.  
- **Safety:** Single-joint tests reduce risk of hardware damage.  
- **Skill-Focused:** Every loop (command → feedback → logging) is a learning opportunity.  
- **Stop Conditions:** Projects stop once objectives are achieved; no over-optimization.  

---

**Notes:**  
- This system is **temporary** — designed only for skill acquisition.  
- Components and software from Mini-Project A/B will **directly scale into Phase 1** full-arm development.  
- Mini-Project C is purely educational and optional; it introduces FK/IK without hardware stress.
