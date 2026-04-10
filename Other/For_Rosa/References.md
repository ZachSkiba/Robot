# 🔹 REFERENCES

## Mechanical & Structural

**Thor 6-DOF Robotic Arm — Hackaday.io**  
https://hackaday.io/project/157114-thor  
Reference for full-arm mechanical architecture and joint distribution. Used for baseline comparison of structural layout and load distribution strategies in multi-DOF arms.

**DIY Robot Arm Project — How To Mechatronics**  
https://howtomechatronics.com/projects/diy-robot-arm-project/  
Reference for practical robotic arm construction, actuator integration, and general mechanical implementation constraints. Used as a build-level reference, not a design authority.

---

## Software & Simulation

**ROS2 Control Framework (ros2_control)**  
https://github.com/ros-controls/ros2_control  
Core abstraction layer for actuator control and hardware interface design in ROS2-based systems.

**URDF Tutorial (ROS)**  
https://github.com/ros/urdf_tutorial  
Reference for robot description format, kinematic tree structure, joint definitions, and coordinate frame conventions used in CAD-to-simulation pipeline.

**Niryo One ROS Stack**  
https://github.com/NiryoRobotics/niryo_one_ros  
Reference for system architecture separating high-level planning and embedded execution; informs split-brain control design approach.

---

## Hardware & Datasheets

**AS5600 Magnetic Encoder — AMS OSRAM**  
https://ams-osram.com/products/sensor-solutions/position-sensors/as5600  
Defines encoder resolution, interface constraints, and timing limitations; informs sampling strategy and fault detection logic.

**TMC2209 Stepper Driver — Analog Devices**  
https://www.analog.com/en/products/tmc2209.html  
Defines motor control behavior, microstepping configuration, and electrical noise constraints for actuator design.

---

## Control & Robotics Theory

**Modern Robotics (Lynch & Park)**  
https://modernrobotics.northwestern.edu/nu-geared-up-for-robotics/  
Primary theoretical reference for kinematics, forward/inverse kinematics, Jacobians, and trajectory generation used in system modeling and planning.

**Robotics Toolbox for Python (Corke)**  
https://github.com/petercorke/robotics-toolbox-python  
Reference implementation for robotic kinematics and control algorithms in Python; supports computational validation of DH modeling and trajectory logic.