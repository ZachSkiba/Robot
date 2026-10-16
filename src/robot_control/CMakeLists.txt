cmake_minimum_required(VERSION 3.8)
project(robot_control)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)

add_library(robot_control_lib
  src/robot_node.cpp
)

target_include_directories(robot_control_lib PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include/${PROJECT_NAME}>
)

ament_target_dependencies(robot_control_lib rclcpp)

add_executable(robot_node src/node.cpp)
target_link_libraries(robot_node robot_control_lib)
ament_target_dependencies(robot_node rclcpp)

install(TARGETS
  robot_control_lib
  EXPORT export_robot_control_lib
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

install(TARGETS robot_node
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY include/
  DESTINATION include/${PROJECT_NAME}
)

ament_export_targets(export_robot_control_lib HAS_LIBRARY_TARGET)
ament_export_dependencies(rclcpp)

if(BUILD_TESTING)
  find_package(ament_cmake_gtest REQUIRED)

  ament_add_gtest(robot_node_test
    test/test_robot_node.cpp
  )

  if(TARGET robot_node_test)
    target_link_libraries(robot_node_test robot_control_lib)
    ament_target_dependencies(robot_node_test rclcpp)
  endif()
endif()

ament_package()
