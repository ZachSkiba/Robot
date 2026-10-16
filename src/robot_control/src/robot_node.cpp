#include "robot_control/robot_node.hpp"

namespace robot_control
{

RobotNode::RobotNode()
: rclcpp::Node("robot_node")
{
  RCLCPP_INFO(get_logger(), "robot_control node running");
}

}  // namespace robot_control
