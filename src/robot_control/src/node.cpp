#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "robot_control/robot_node.hpp"

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<robot_control::RobotNode>());
  rclcpp::shutdown();
  return 0;
}
