# 🔹 REFERENCES

## Mechanical & Structural

**Thor 6-DOF Robotic Arm — Hackaday.io**  
https://hackaday.io/project/12989-thor  
Reference for full-arm mechanical architecture and joint distribution. Used for baseline comparison of structural layout and load distribution strategies in multi-DOF arms.

**DIY 3D Printed Drive Comparison — How To Mechatronics**  
https://howtomechatronics.com/how-it-works/what-is-the-best-3d-printed-drive-for-your-next-robotic-project/

Reference for comparative analysis of 3D-printed drivetrain architectures, including belt drives, planetary gearboxes, and cycloidal reducers. Used as a design-level benchmark for evaluating efficiency, backlash, torque transmission, manufacturability, and wear behavior in additively manufactured robotic transmission systems.

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
https://ams-osram.com/products/sensor-solutions/position-sensors/ams-as5600-position-sensor 
Defines encoder resolution, interface constraints, and timing limitations; informs sampling strategy and fault detection logic.

**TMC2209 Stepper Driver — Analog Devices**  
https://www.analog.com/en/products/tmc2209.html  
Defines motor control behavior, microstepping configuration, and electrical noise constraints for actuator design.

---

## Control & Robotics Theory

**Modern Robotics (Lynch & Park)**  
https://hades.mech.northwestern.edu/images/7/7f/MR.pdf 
Primary theoretical reference for kinematics, forward/inverse kinematics, Jacobians, and trajectory generation used in system modeling and planning.

**Robotics Toolbox for Python (Corke)**  
https://github.com/petercorke/robotics-toolbox-python  
Reference implementation for robotic kinematics and control algorithms in Python; supports computational validation of DH modeling and trajectory logic.