cmake_minimum_required(VERSION 3.8)
project(robot_control)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)

add_executable(robot_node src/node.cpp)
ament_target_dependencies(robot_node rclcpp)

install(TARGETS
  robot_node
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()