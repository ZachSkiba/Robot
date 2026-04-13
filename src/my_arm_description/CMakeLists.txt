cmake_minimum_required(VERSION 3.8)
project(my_arm_description)

find_package(ament_cmake REQUIRED)

foreach(resource_dir IN ITEMS urdf meshes launch rviz config)
  if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/${resource_dir}")
    install(DIRECTORY
      ${resource_dir}
      DESTINATION share/${PROJECT_NAME}
    )
  endif()
endforeach()

ament_package()
