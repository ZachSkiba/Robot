#!/usr/bin/env bash
# 6-DOF Robot - Development Environment Verification
# Verifies ROS, workspace integrity, Python, hardware access,
# simulation/graphics, and development tools.
# Does not install packages or modify system configuration.

set -uo pipefail

ROOT="/workspace/Robot"
SYSTEM_PYTHON="/usr/bin/python3"
DEV_PYTHON="$ROOT/.venv/bin/python"

PASS=0
FAIL=0
WARN=0
SKIP=0

section() {
    printf '\n=== %s ===\n' "$1"
}

pass() {
    printf '  PASS: %s\n' "$1"
    ((PASS+=1))
}

fail() {
    printf '  FAIL: %s\n' "$1"
    ((FAIL+=1))
}

warn() {
    printf '  WARN: %s\n' "$1"
    ((WARN+=1))
}

skip() {
    printf '  SKIP: %s\n' "$1"
    ((SKIP+=1))
}

check() {
    local label="$1"
    shift
    if "$@" >/dev/null 2>&1; then
        pass "$label"
    else
        fail "$label"
    fi
}

optional_check() {
    local label="$1"
    shift
    if "$@" >/dev/null 2>&1; then
        pass "$label"
    else
        warn "$label (optional/unavailable)"
    fi
}

if [[ ! -d "$ROOT/src" ]]; then
    echo "ERROR: Workspace source directory missing: $ROOT/src"
    exit 2
fi

cd "$ROOT" || exit 2

# ------------------------------------------------------------
section "1. System and ROS Environment"

check "lsb_release available" command -v lsb_release

if command -v lsb_release >/dev/null 2>&1; then
    RELEASE="$(lsb_release -rs)"
    if [[ "$RELEASE" == "22.04" ]]; then
        pass "Ubuntu 22.04"
    else
        warn "Ubuntu version is $RELEASE (expected 22.04)"
    fi
fi

check "ROS Humble setup file exists" test -f /opt/ros/humble/setup.bash

if [[ -f /opt/ros/humble/setup.bash ]]; then
    # ROS setup scripts may reference unset variables.
    set +u
    # shellcheck disable=SC1091
    source /opt/ros/humble/setup.bash
    ROS_SOURCE_STATUS=$?
    set -u

    if (( ROS_SOURCE_STATUS == 0 )); then
        pass "ROS Humble underlay sources successfully"
    else
        fail "ROS Humble underlay sourcing"
    fi
else
    fail "ROS Humble underlay unavailable"
fi

check "ROS 2 CLI available" command -v ros2
check "colcon available" command -v colcon

if [[ "${ROS_DISTRO:-}" == "humble" ]]; then
    pass "ROS_DISTRO is humble"
else
    fail "ROS_DISTRO is not humble"
fi

if [[ "${RMW_IMPLEMENTATION:-}" == "rmw_cyclonedds_cpp" ]]; then
    pass "CycloneDDS RMW configured"
else
    fail "CycloneDDS RMW is not configured"
fi

if command -v ros2 >/dev/null 2>&1; then
    for pkg in ros2_control ros2_controllers tf2_tools xacro ros_gz_bridge; do
        if ros2 pkg list 2>/dev/null | grep -Fxq "$pkg"; then
            pass "ROS package: $pkg"
        else
            fail "Required ROS package missing: $pkg"
        fi
    done

    for pkg in moveit joint_state_publisher_gui foxglove_bridge plotjuggler; do
        if ros2 pkg list 2>/dev/null | grep -Fxq "$pkg"; then
            pass "Optional ROS package: $pkg"
        else
            warn "Optional ROS package unavailable: $pkg"
        fi
    done
else
    skip "ROS package discovery: ROS CLI unavailable"
fi

# ------------------------------------------------------------
section "2. ROS Workspace Integrity"

check "Workspace source directory" test -d "$ROOT/src"

for pkg in robot_control my_arm_description; do
    PKG_DIR="$ROOT/src/$pkg"

    if [[ ! -d "$PKG_DIR" ]]; then
        fail "Source package directory missing: $pkg"
        continue
    fi

    check "$pkg package.xml exists" test -f "$PKG_DIR/package.xml"
    check "$pkg CMakeLists.txt exists" test -f "$PKG_DIR/CMakeLists.txt"

    if [[ -f "$PKG_DIR/package.xml" ]]; then
        if grep -Eq "<name>[[:space:]]*$pkg[[:space:]]*</name>" "$PKG_DIR/package.xml"; then
            pass "$pkg manifest name matches expected package"
        else
            fail "$pkg manifest name mismatch"
        fi
    fi

    if [[ -f "$PKG_DIR/CMakeLists.txt" ]]; then
        if grep -Eq "project[[:space:]]*\\([[:space:]]*$pkg([[:space:])]|$)" "$PKG_DIR/CMakeLists.txt"; then
            pass "$pkg CMake project name matches"
        else
            fail "$pkg CMake project name mismatch"
        fi
    fi
done

if [[ -f "$ROOT/src/robot_control/src/node.cpp" ]]; then
    pass "robot_control node source exists"
else
    fail "robot_control node source missing"
fi

IGNORE_FILES="$(find "$ROOT/src" -name COLCON_IGNORE -type f -print 2>/dev/null || true)"
if [[ -z "$IGNORE_FILES" ]]; then
    pass "No COLCON_IGNORE files found"
else
    warn "COLCON_IGNORE files exist; inspect whether packages are intentionally excluded"
    printf '%s\n' "$IGNORE_FILES"
fi

if [[ -d "$ROOT/src/my_arm_description/urdf" ]] &&
   find "$ROOT/src/my_arm_description/urdf" -type f 
       \( -name '*.urdf' -o -name '*.xacro' \) -print -quit | grep -q .; then
    pass "URDF/Xacro source files exist"
else
    warn "Robot description URDF/Xacro not implemented or not in expected directory"
fi

# ------------------------------------------------------------
section "3. Python Environment Integrity"

if [[ -x "$SYSTEM_PYTHON" ]]; then
    check "System Python imports NumPy, OpenCV and cv_bridge" 
        "$SYSTEM_PYTHON" -c 
        'import numpy, cv2; from cv_bridge import CvBridge'

    if "$SYSTEM_PYTHON" -c '
import numpy as np
from cv_bridge import CvBridge
bridge = CvBridge()
image = np.zeros((16, 16, 3), dtype=np.uint8)
message = bridge.cv2_to_imgmsg(image, encoding="bgr8")
result = bridge.imgmsg_to_cv2(message, desired_encoding="bgr8")
assert result.shape == image.shape
assert result.dtype == image.dtype
'; then
        pass "System Python cv_bridge round-trip"
    else
        fail "System Python cv_bridge round-trip"
    fi

    if "$SYSTEM_PYTHON" -c '
import sys
bad = [p for p in sys.path if "/.local/" in p or "/home/" in p]
if bad:
    print("Unexpected user paths:", bad)
    raise SystemExit(1)
'; then
        pass "System Python has no unexpected user-site paths"
    else
        warn "System Python contains user/home paths; inspect for ROS dependency shadowing"
    fi

    if "$SYSTEM_PYTHON" -c '
import numpy, os
assert os.path.isfile(numpy.__file__)
assert "/usr/lib/python3/dist-packages/" in numpy.__file__
'; then
        pass "System NumPy resolves to the expected system package path"
    else
        warn "System NumPy source path differs from expected apt path"
    fi
else
    fail "System Python missing"
fi

if [[ -x "$DEV_PYTHON" ]]; then
    check "Development Python numerical/serial imports" 
        "$DEV_PYTHON" -c 'import numpy, scipy, pandas, serial'

    "$DEV_PYTHON" -c '
import sys, numpy, scipy, pandas, serial
print("  Interpreter:", sys.executable)
print("  NumPy:", numpy.__version__)
print("  SciPy:", scipy.__version__)
print("  pandas:", pandas.__version__)
print("  pyserial: available")
' 2>/dev/null

    optional_check "Development Black formatter" "$DEV_PYTHON" -m black --version
else
    fail "Development virtual environment missing: $DEV_PYTHON"
fi

# ------------------------------------------------------------
section "4. Build, Registration and Automated Tests"

if colcon build --symlink-install; then
    pass "Workspace build succeeds"
else
    fail "Workspace build failed"
fi

if [[ -f "$ROOT/install/setup.bash" ]]; then
    # Source in the current shell so ROS package checks see the overlay.
    # Restore the original nounset state rather than always enabling it.
    HAD_NOUNSET=0
    [[ $- == *u* ]] && HAD_NOUNSET=1

    set +u
    # shellcheck disable=SC1091
    source "$ROOT/install/setup.bash"
    OVERLAY_STATUS=$?

    if (( HAD_NOUNSET )); then
        set -u
    else
        set +u
    fi

    if (( OVERLAY_STATUS == 0 )); then
        pass "Workspace setup sourcing succeeds"
    else
        fail "Workspace setup sourcing failed"
    fi
else
    fail "install/setup.bash missing"
fi

if command -v ros2 >/dev/null 2>&1; then
    if ros2 pkg list 2>/dev/null | grep -Fxq robot_control; then
        pass "robot_control registered"
    else
        fail "robot_control not registered"
    fi

    if ros2 pkg list 2>/dev/null | grep -Fxq my_arm_description; then
        pass "my_arm_description registered"
    else
        fail "my_arm_description not registered"
    fi

    if ros2 pkg executables robot_control 2>/dev/null |
       grep -Eq '(^|[[:space:]])robot_node$'; then
        pass "robot_node registered"
    else
        fail "robot_node not registered"
    fi
fi

if command -v rosdep >/dev/null 2>&1; then
    if rosdep check --from-paths "$ROOT/src" --ignore-src -y; then
        pass "rosdep dependency check"
    else
        fail "rosdep dependency check"
    fi
else
    warn "rosdep unavailable; dependency validation not performed"
fi

# Run package tests only after a successful build.
if command -v colcon >/dev/null 2>&1 && [[ -d "$ROOT/build" ]]; then
    if colcon test --return-code-on-test-failure; then
        pass "colcon test command"
    else
        fail "colcon test reported an execution or test failure"
    fi

    if colcon test-result --all --verbose; then
        pass "colcon test-result report generated"
    else
        fail "colcon test-result reported failures or could not run"
    fi
else
    skip "Automated ROS tests: colcon/build prerequisites unavailable"
fi

# ------------------------------------------------------------
section "5. Hardware Access"

check "USB bus directory exists" test -d /dev/bus/usb
optional_check "usbip utility installed" command -v usbip
optional_check "Teensy loader installed" command -v teensy_loader_cli
optional_check "Serial monitor tio installed" command -v tio
optional_check "Git LFS installed" command -v git-lfs

if [[ -d /dev/bus/usb ]]; then
    if find /dev/bus/usb -type c -print -quit 2>/dev/null | grep -q .; then
        pass "USB character devices visible"
    else
        warn "No USB character devices visible; confirm passthrough and connected hardware"
    fi
fi

SERIAL_FOUND=0
for dev in /dev/ttyACM* /dev/ttyUSB*; do
    [[ -e "$dev" ]] || continue
    SERIAL_FOUND=1
    if [[ -r "$dev" && -w "$dev" ]]; then
        pass "Serial device accessible: $dev"
    else
        warn "Serial device exists but current user lacks read/write access: $dev"
    fi
done

if (( SERIAL_FOUND == 0 )); then
    skip "No /dev/ttyACM* or /dev/ttyUSB* device connected"
fi

if id -nG 2>/dev/null | tr ' ' '\n' | grep -Fxq dialout; then
    pass "Current user belongs to dialout group"
else
    warn "Current user is not in dialout group; device access may depend on udev permissions"
fi

# ------------------------------------------------------------
section "6. Simulation, GUI and Graphics"

if command -v ign >/dev/null 2>&1; then
    pass "Gazebo Ignition executable available"
    ign gazebo --version 2>/dev/null || true
elif command -v gz >/dev/null 2>&1; then
    pass "Gazebo executable available"
    gz sim --version 2>/dev/null || true
else
    warn "Gazebo executable unavailable"
fi

if command -v ros2 >/dev/null 2>&1 &&
   ros2 pkg list 2>/dev/null | grep -Fxq ros_gz_bridge; then
    pass "ros_gz_bridge registered"
else
    warn "ros_gz_bridge unavailable"
fi

if [[ -n "${DISPLAY:-}" || -n "${WAYLAND_DISPLAY:-}" ]]; then
    pass "Display environment configured"
else
    skip "No GUI display configured; headless session is allowed"
fi

if [[ -d /mnt/wslg ]]; then
    pass "WSLg mount exists"
else
    skip "WSLg mount absent"
fi

if [[ -d /tmp/.X11-unix ]]; then
    pass "X11 socket directory exists"
else
    skip "X11 socket directory absent"
fi

if command -v glxinfo >/dev/null 2>&1; then
    pass "OpenGL diagnostic tool installed"
    RENDERER="$(glxinfo -B 2>/dev/null |
        sed -n 's/^[[:space:]]*OpenGL renderer string: //p' | head -n 1)"
    echo "  Renderer: ${RENDERER:-unavailable}"

    if [[ -z "$RENDERER" ]]; then
        warn "OpenGL renderer could not be queried"
    elif printf '%s' "$RENDERER" | grep -qiE 'llvmpipe|softpipe|software rasterizer'; then
        warn "Software rendering detected; hardware acceleration not verified"
    else
        pass "OpenGL renderer reports a non-obvious software renderer"
    fi
else
    skip "glxinfo unavailable; graphics acceleration not checked"
fi

optional_check "NVIDIA utility available" command -v nvidia-smi
optional_check "ccache installed" command -v ccache

# ------------------------------------------------------------
section "Summary"

printf '  PASSED:   %d\n' "$PASS"
printf '  FAILED:   %d\n' "$FAIL"
printf '  WARNINGS: %d\n' "$WARN"
printf '  SKIPPED:  %d\n' "$SKIP"

if (( FAIL > 0 )); then
    echo "RESULT: FAIL"
    exit 1
else
    echo "RESULT: PASS (review warnings and skipped checks)"
    exit 0
fi
