#include "rclcpp/rclcpp.hpp"

class RobotNode : public rclcpp::Node {
public:
  RobotNode() : rclcpp::Node("robot_node") {
    RCLCPP_INFO(this->get_logger(), "robot_control node running");
  }
};

int main(int argc, char ** argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<RobotNode>());
  rclcpp::shutdown();
  return 0;
}
