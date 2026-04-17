#!/bin/bash
# ─────────────────────────────────────────────
# 6-DOF Arm Dev Container — Setup Verification
# ─────────────────────────────────────────────

PASS=0
FAIL=0

check() {
  local label="$1"
  local cmd="$2"
  if eval "$cmd" &>/dev/null; then
    echo "  ✅  $label"
    ((PASS++))
  else
    echo "  ❌  $label"
    ((FAIL++))
  fi
}

check_val() {
  local label="$1"
  local expected="$2"
  local actual="$3"
  if [[ "$actual" == *"$expected"* ]]; then
    echo "  ✅  $label → $actual"
    ((PASS++))
  else
    echo "  ❌  $label → got: '$actual' (expected: '$expected')"
    ((FAIL++))
  fi
}

echo ""
echo "════════════════════════════════════════"
echo "  6-DOF ARM — ENVIRONMENT VERIFICATION"
echo "════════════════════════════════════════"

# ── 1. OS ─────────────────────────────────
echo ""
echo "[ OS ]"
check_val "Ubuntu 22.04" "22.04" "$(lsb_release -rs)"
check "WSLg present" "test -d /mnt/wslg"
check "DISPLAY set" "test -n \"$DISPLAY\""

# ── 2. ROS 2 ──────────────────────────────
echo ""
echo "[ ROS 2 ]"
check_val "ROS_DISTRO = humble"        "humble"              "$ROS_DISTRO"
check_val "RMW = CycloneDDS"           "rmw_cyclonedds_cpp"  "$RMW_IMPLEMENTATION"
check_val "ROS_DOMAIN_ID set"          ""                    "${ROS_DOMAIN_ID:-NOT SET}"
check_val "ROS_NAMESPACE set"          ""                    "${ROS_NAMESPACE:-NOT SET}"
check     "ROS 2 sourced (ros2 cli)"   "ros2 --help"
check     "ros2_control installed"     "ros2 pkg list | grep -q ros2_control"
check     "ros2_controllers installed" "ros2 pkg list | grep -q ros2_controllers"
check     "MoveIt2 installed"          "ros2 pkg list | grep -q moveit"
check     "tf2_tools installed"        "ros2 pkg list | grep -q tf2_tools"
check     "foxglove_bridge installed"  "ros2 pkg list | grep -q foxglove_bridge"
check     "plotjuggler installed"      "ros2 pkg list | grep -q plotjuggler"
check "xacro installed" "ros2 pkg list | grep -q '^xacro$'"
check "joint_state_publisher_gui" "ros2 pkg list | grep -q 'joint_state_publisher_gui'"
check "ros2 pkg list functional" "source install/setup.bash && ros2 pkg list | grep -q robot_control"
check "robot_node executable visible" "source install/setup.bash && ros2 run robot_control robot_node --help"

echo ""
echo "[ ROS Workspace Integrity ]"

check "inside ROS workspace root" "test -f /workspace/Robot/src/CMakeLists.txt || test -d /workspace/Robot/src"

check "colcon can index packages" "colcon list | grep -q robot_control"
check "colcon can index description pkg" "colcon list | grep -q my_arm_description"

check "no COLCON_IGNORE blocking build" "! find src -name COLCON_IGNORE | grep -q ."

echo ""
echo "[ ROS Package Structure ]"

check "robot_control package.xml exists" "test -f src/robot_control/package.xml"
check "robot_control CMakeLists exists" "test -f src/robot_control/CMakeLists.txt"
check "robot_control node.cpp exists" "test -f src/robot_control/src/node.cpp"

check "my_arm_description package.xml exists" "test -f src/my_arm_description/package.xml"
check "my_arm_description CMakeLists exists" "test -f src/my_arm_description/CMakeLists.txt"
check "my_arm_description urdf folder exists" "test -d src/my_arm_description/urdf"

echo ""
echo "[ CMake ↔ Package Consistency ]"

check "robot_control name match" "grep -q '<name>robot_control</name>' src/robot_control/package.xml"
check "my_arm_description name match" "grep -q '<name>my_arm_description</name>' src/my_arm_description/package.xml"

check "robot_control project match" "grep -q 'project(robot_control)' src/robot_control/CMakeLists.txt"
check "description project match" "grep -q 'project(my_arm_description)' src/my_arm_description/CMakeLists.txt"

echo ""
echo "[ Build Readiness ]"

check "no missing CMake source refs (node.cpp)" "! grep -R 'add_executable' src | grep -q 'src/node.cpp' || test -f src/robot_control/src/node.cpp"

check "no empty install directives for missing dirs" "! grep -R 'install(DIRECTORY' src | grep -q 'urdf.*DOES_NOT_EXIST'"

echo ""
echo "[ Build Output Validation ]"

check "install space exists" "test -d install"
check "setup.bash generated" "test -f install/setup.bash"

echo ""
echo "[ Early Failure Detection ]"

check "no CMake project mismatch detected" "! grep -R 'project(robot_control)' src/my_arm_description"
check "no missing source files referenced in CMake" "! grep -R 'src/node.cpp' src/robot_control || test -f src/robot_control/src/node.cpp"

check "ROS masterless runtime OK" "ros2 node list"
check "ROS daemon responding" "ros2 doctor --report"

check "no broken ROS deps" "rosdep check --from-paths src --ignore-src -y"

check "colcon build succeeds" "colcon build --symlink-install --cmake-args -Werror"

check "robot_node is registered in ROS2" "ros2 pkg executables robot_control | grep -q robot_node"

check "no CMake project mismatch" "! grep -R 'project(robot_control)' src/my_arm_description"

check "all packages have project() defined" "grep -R 'project(' src | wc -l"

check "URDF folder non-empty if exists" "test ! -d src/my_arm_description/urdf || test \"$(ls src/my_arm_description/urdf)\""

check "robot_control visible" "bash -lc 'source install/setup.bash && ros2 pkg list | grep -q robot_control'"

# ── 3. Gazebo Fortress ────────────────────
echo ""
echo "[ Gazebo Fortress ]"
check     "ign binary exists"          "command -v ign"
check_val "Gazebo version = 6.x"       "6."   "$(ign gazebo --version 2>/dev/null | head -1)"
check     "ros_gz bridge installed"    "ros2 pkg list | grep -q ros_gz_bridge"

# ── 4. GPU ────────────────────────────────
echo ""
echo "[ GPU Acceleration ]"
check     "glxinfo available"          "command -v glxinfo"
check     "GPU accelerated"            "glxinfo -B 2>/dev/null | grep -q 'Accelerated: yes'"
check "OpenGL renderer exists" "glxinfo -B | grep -q 'OpenGL renderer'"
check "GLX context works" "glxinfo -B 2>/dev/null | grep -q 'OpenGL'"
check "NVIDIA runtime detected" "printenv NVIDIA_VISIBLE_DEVICES | grep -q 'all'"
check "nvidia-smi available" "command -v nvidia-smi"
echo "      Renderer: $(glxinfo -B 2>/dev/null | grep 'OpenGL renderer' | cut -d: -f2 | xargs)"

# ── 5. colcon & Workspace ─────────────────
echo ""
echo "[ Workspace ]"
check     "colcon installed"           "command -v colcon"
check     "Workspace src exists"       "test -d /workspace/Robot/src"
check     "Workspace sourced"          "test -f /workspace/Robot/install/setup.bash"
check     "ccache installed"           "command -v ccache"
check "workspace root exists" "test -d /workspace/Robot/src"

# ── 6. Python ─────────────────────────────
echo ""
echo "[ Python ]"
check     "python3 available"          "command -v python3"
check     "pip3 available"             "command -v pip3"
check     "numpy installed"            "python3 -c 'import numpy'"
check     "scipy installed"            "python3 -c 'import scipy'"
check     "pyserial installed"         "python3 -c 'import serial'"
check     "black installed"            "command -v black"

# ── 7. Git & LFS ──────────────────────────
echo ""
echo "[ Git & LFS ]"
check     "git installed"              "command -v git"
check     "git-lfs installed"          "command -v git-lfs"
check     "git-lfs initialized"        "git lfs env | grep -q 'git config filter.lfs'"

# ── 8. User & Permissions ─────────────────
echo ""
echo "[ User & Permissions ]"
check_val "Running as devuser"        "devuser"  "$(whoami)"
check     "In dialout group"           "groups | grep -q dialout"
check     "sudo works (no password)"   "sudo -n true"

# ── 9. Dev Tools ──────────────────────────
echo ""
echo "[ Dev Tools ]"
check     "cmake installed"            "command -v cmake"
check     "build-essential present"    "dpkg -l build-essential | grep -q '^ii'"
check     "usbip available"            "command -v usbip"

# ── 10. bashrc Sanity ─────────────────────
echo ""
echo "[ .bashrc Entries ]"
check     "ROS 2 sourced in bashrc"    "grep -q 'source /opt/ros/humble/setup.bash' ~/.bashrc"
check     "workspace sourced in bashrc" "grep -q 'robot_ws/install/setup.bash' ~/.bashrc"
check     "CycloneDDS in bashrc"       "grep -q 'RMW_IMPLEMENTATION' ~/.bashrc"
check     "clock sync in bashrc"       "grep -q 'ntpdate' ~/.bashrc"
check     "ccache in bashrc"           "grep -q 'CCACHE_DIR' ~/.bashrc"

# ── 11. GUI & Display ─────────────────────
echo ""
echo "[ GUI & Display ]"
check_val "DISPLAY variable set" ":" "${DISPLAY:-NOT SET}"
check "X11 socket mounted" "test -d /tmp/.X11-unix"
check "WSLg mount exists" "test -d /mnt/wslg"

# ── 12. Hardware Tools ────────────────────
echo ""
echo "[ Hardware & Teensy ]"
check "tio (Serial Monitor) installed" "command -v tio"
check "teensy_loader_cli installed" "command -v teensy_loader_cli"
check "USB bus mounted" "test -d /dev/bus/usb"

# Other
check "sys.path clean (no user-site)" "
python3 -c '
import sys
bad = [p for p in sys.path if \"/.local\" in p or \"/home\" in p]
print(bad)
assert not bad ' "
check "numpy from apt only" "
python3 -c 'import numpy; import inspect; import numpy; assert \"/usr/lib/python3/dist-packages\" in numpy.__file__ ' "
check "cv_bridge ABI roundtrip" "
python3 -c '
from cv_bridge import CvBridge
import numpy as np
b = CvBridge()
img = np.zeros((100,100,3), dtype=np.uint8)
msg = b.cv2_to_imgmsg(img)
out = b.imgmsg_to_cv2(msg)
assert out.shape == img.shape ' "
check "AMENT_PREFIX_PATH cardinality" 'python3 -c "import os; p = os.environ.get(\"AMENT_PREFIX_PATH\", \"\").split(\":\"); print(p); assert len(p) <= 2"'

check "AMENT_PREFIX_PATH exact structure" 'python3 -c "import os; p = os.environ.get(\"AMENT_PREFIX_PATH\", \"\").split(\":\"); allowed = [\"/opt/ros/humble\", \"/workspace/Robot/install\"]; [assert any(a in x for a in allowed) for x in p]"'

check "no pip site-packages leak" 'python3 -c "import site; paths = site.getsitepackages() + [site.getusersitepackages()]; print(paths); assert all(\".local\" not in p for p in paths)"'

check "numpy ABI + source valid" 'python3 -c "import numpy; assert hasattr(numpy, \"__file__\"); assert \"dist-packages\" in numpy.__file__"'

check "robot_control visible in environment" "ros2 pkg list | grep -q robot_control"

check "no venv active" 'python3 -c "import sys; assert not any(\"venv\" in p for p in sys.path)"'

check "no duplicate ROS overlay entries" 'python3 -c "import os; p = os.environ.get(\"AMENT_PREFIX_PATH\", \"\").split(\":\"); assert len(p) == len(set(p))"'

# ── RESULT ────────────────────────────────
echo ""
echo "════════════════════════════════════════"
echo "  PASSED: $PASS   FAILED: $FAIL"
echo "════════════════════════════════════════"
echo ""
if [ $FAIL -eq 0 ]; then
  echo "  🟢 Environment is clean. You're good to build."
else
  echo "  🔴 $FAIL check(s) failed. Fix the ❌ items above before proceeding."
fi
echo ""