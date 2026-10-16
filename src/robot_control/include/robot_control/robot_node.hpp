#ifndef ROBOT_CONTROL__ROBOT_NODE_HPP_
#define ROBOT_CONTROL__ROBOT_NODE_HPP_

#include "rclcpp/rclcpp.hpp"

namespace robot_control
{

class RobotNode : public rclcpp::Node
{
public:
  RobotNode();
};

}  // namespace robot_control

#endif  // ROBOT_CONTROL__ROBOT_NODE_HPP_
