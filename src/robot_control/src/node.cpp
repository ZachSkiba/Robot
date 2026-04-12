#include "rclcpp/rclcpp.hpp"

class Node : public rclcpp::Node {
public:
  Node() : Node("robot_node") {
    RCLCPP_INFO(this->get_logger(), "robot_control node running");
  }
};

int main(int argc, char ** argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<Node>());
  rclcpp::shutdown();
  return 0;
}