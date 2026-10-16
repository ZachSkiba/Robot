#include <memory>

#include <gtest/gtest.h>
#include <rclcpp/rclcpp.hpp>

#include "robot_control/robot_node.hpp"

class RobotNodeTest : public ::testing::Test
{
protected:
  static void SetUpTestSuite()
  {
    if (!rclcpp::ok()) {
      int argc = 0;
      char ** argv = nullptr;
      rclcpp::init(argc, argv);
    }
  }

  static void TearDownTestSuite()
  {
    if (rclcpp::ok()) {
      rclcpp::shutdown();
    }
  }
};

TEST_F(RobotNodeTest, RosContextInitializes)
{
  EXPECT_TRUE(rclcpp::ok());
}

TEST_F(RobotNodeTest, NodeHasExpectedName)
{
  auto node = std::make_shared<robot_control::RobotNode>();
  EXPECT_STREQ(node->get_name(), "robot_node");
}
