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

if(BUILD_TESTING)
  find_package(ament_cmake_gtest REQUIRED)

  ament_add_gtest(robot_node_test
    test/test_robot_node.cpp
  )

  ament_target_dependencies(robot_node_test rclcpp)
endif()

ament_package()