#!/usr/bin/env bash
# 6-DOF Robot - Development Environment Verification
# Verifies the ROS workspace, Python environments, hardware visibility,
# simulation/graphics, and development tools without installing packages.

set -uo pipefail

ROOT="/workspace/Robot"
SYSTEM_PYTHON="/usr/bin/python3"
DEV_PYTHON="$ROOT/.venv/bin/python"

MODE="${1:-audit}"

if [[ "$MODE" != "audit" && "$MODE" != "full" ]]; then
    printf 'Usage: %s [audit|full]\n' "$0" >&2
    exit 2
fi

PASS=0
FAIL=0
WARN=0
SKIP=0

section() {
    printf '\n=== %s ===\n' "$1"
}

pass() {
    printf '  PASS: %s\n' "$1"
    PASS=$((PASS + 1))
}

fail() {
    printf '  FAIL: %s\n' "$1"
    FAIL=$((FAIL + 1))
}

warn() {
    printf '  WARN: %s\n' "$1"
    WARN=$((WARN + 1))
}

skip() {
    printf '  SKIP: %s\n' "$1"
    SKIP=$((SKIP + 1))
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

source_setup() {
    local setup_file="$1"
    local had_nounset=0
    local status

    [[ $- == *u* ]] && had_nounset=1
    set +u
    # shellcheck disable=SC1090
    source "$setup_file"
    status=$?

    if (( had_nounset )); then
        set -u
    else
        set +u
    fi
    return "$status"
}

summary() {
    printf '\n=== Summary ===\n'
    printf '  PASSED:   %d\n' "$PASS"
    printf '  FAILED:   %d\n' "$FAIL"
    printf '  WARNINGS: %d\n' "$WARN"
    printf '  SKIPPED:  %d\n' "$SKIP"

    if (( FAIL > 0 )); then
        printf 'RESULT: FAIL\n'
        return 1
    elif (( WARN > 0 || SKIP > 0 )); then
        printf 'RESULT: PASS WITH WARNINGS\n'
        return 0
    else
        printf 'RESULT: PASS\n'
        return 0
    fi
}

if [[ ! -d "$ROOT" ]]; then
    fail "Workspace root missing: $ROOT"
    summary
    exit 1
fi

if [[ ! -d "$ROOT/src" ]]; then
    fail "Workspace source directory missing: $ROOT/src"
    summary
    exit 1
fi

cd "$ROOT" || {
    fail "Cannot enter workspace root: $ROOT"
    summary
    exit 1
}

# Remove inherited ROS overlay paths so package discovery starts from the
# Humble underlay, not from whichever ROS workspace launched this script.
unset AMENT_PREFIX_PATH CMAKE_PREFIX_PATH COLCON_PREFIX_PATH ROS_PACKAGE_PATH
unset ROS_VERSION ROS_PYTHON_VERSION ROS_DISTRO

section "1. System and ROS Environment"

check "Workspace root exists" test -d "$ROOT"
check "Workspace source directory exists" test -d "$ROOT/src"

for tool in lsb_release git cmake make g++; do
    check "$tool available" command -v "$tool"
done

if command -v lsb_release >/dev/null 2>&1; then
    RELEASE="$(lsb_release -rs 2>/dev/null)"
    if [[ "$RELEASE" == "22.04" ]]; then
        pass "Ubuntu 22.04"
    else
        fail "Ubuntu version is ${RELEASE:-unavailable} (expected 22.04)"
    fi
fi

ROS_UNDERLAY_OK=0
if [[ -r /opt/ros/humble/setup.bash ]]; then
    if source_setup /opt/ros/humble/setup.bash; then
        ROS_UNDERLAY_OK=1
        pass "ROS Humble underlay sources successfully"
    else
        fail "ROS Humble underlay sourcing failed"
    fi
else
    fail "ROS Humble setup file is missing or unreadable"
fi

if [[ "${ROS_DISTRO:-}" == "humble" ]]; then
    pass "ROS_DISTRO is humble"
else
    fail "ROS_DISTRO is ${ROS_DISTRO:-unset} (expected humble)"
fi

if [[ "${RMW_IMPLEMENTATION:-}" == "rmw_cyclonedds_cpp" ]]; then
    pass "CycloneDDS RMW configured"
else
    fail "RMW_IMPLEMENTATION is ${RMW_IMPLEMENTATION:-unset} (expected rmw_cyclonedds_cpp)"
fi

ROS_CLI_OK=0
if command -v ros2 >/dev/null 2>&1; then
    ROS_CLI_OK=1
    pass "ROS 2 CLI available"
else
    fail "ROS 2 CLI unavailable"
fi

COLCON_OK=0
if command -v colcon >/dev/null 2>&1; then
    COLCON_OK=1
    pass "Colcon available"
else
    fail "Colcon unavailable"
fi

ROS_PACKAGE_LIST=""
ROS_PACKAGE_LIST_OK=0
if (( ROS_UNDERLAY_OK && ROS_CLI_OK )); then
    if ROS_PACKAGE_LIST="$(ros2 pkg list 2>&1)"; then
        ROS_PACKAGE_LIST_OK=1
        pass "ROS package discovery from Humble underlay"
    else
        fail "ROS package discovery from Humble underlay failed"
        printf '    %s\n' "$ROS_PACKAGE_LIST" | head -n 5
    fi
else
    skip "ROS package discovery: underlay or ROS CLI unavailable"
fi

if (( ROS_PACKAGE_LIST_OK )); then
    for pkg in controller_manager joint_state_broadcaster joint_trajectory_controller tf2_tools xacro ros_gz_bridge; do
        if grep -Fxq -- "$pkg" <<<"$ROS_PACKAGE_LIST"; then
            pass "Required ROS package: $pkg"
        else
            fail "Required ROS package missing: $pkg"
        fi
    done

    for pkg in moveit joint_state_publisher_gui foxglove_bridge plotjuggler; do
        if grep -Fxq -- "$pkg" <<<"$ROS_PACKAGE_LIST"; then
            pass "Optional ROS package: $pkg"
        else
            warn "Optional ROS package unavailable: $pkg"
        fi
    done
else
    skip "Required and optional ROS package checks: package list unavailable"
fi

section "2. ROS Workspace Integrity"

for pkg in robot_control my_arm_description; do
    PKG_DIR="$ROOT/src/$pkg"
    MANIFEST="$PKG_DIR/package.xml"
    CMAKE_FILE="$PKG_DIR/CMakeLists.txt"

    if [[ -d "$PKG_DIR" ]]; then
        pass "$pkg source directory exists"
    else
        fail "Source package directory missing: $pkg"
        continue
    fi

    if [[ -r "$MANIFEST" ]]; then
        pass "$pkg package.xml exists and is readable"
        if grep -Eq "<name>[[:space:]]*${pkg}[[:space:]]*</name>" "$MANIFEST"; then
            pass "$pkg manifest name matches"
        else
            fail "$pkg manifest name does not match its directory"
        fi
    else
        fail "$pkg package.xml is missing or unreadable"
    fi

    if [[ -r "$CMAKE_FILE" ]]; then
        pass "$pkg CMakeLists.txt exists and is readable"
        if grep -Eq "^[[:space:]]*project[[:space:]]*\\([[:space:]]*${pkg}([[:space:]]|\\))" "$CMAKE_FILE"; then
            pass "$pkg CMake project name matches"
        else
            fail "$pkg CMake project name does not match its directory"
        fi
    else
        fail "$pkg CMakeLists.txt is missing or unreadable"
    fi
done

for source_file in \
    src/robot_control/src/node.cpp \
    src/robot_control/src/robot_node.cpp \
    src/robot_control/include/robot_control/robot_node.hpp \
    src/robot_control/test/test_robot_node.cpp; do
    check "$source_file exists and is readable" test -r "$ROOT/$source_file"
done

check "Setup documentation exists and is readable" test -r "$ROOT/docs/setup/devcontainer-setup.md"
check "Teensy workflow documentation exists and is readable" \
    test -r "$ROOT/docs/board-workflow/teensy-flashing-running-code.md"

if [[ -r "$ROOT/docs/setup/setup-checks.sh" ]]; then
    check "Verification script syntax" bash -n "$ROOT/docs/setup/setup-checks.sh"
else
    fail "Verification script is missing or unreadable"
fi

if command -v shellcheck >/dev/null 2>&1; then
    check "ShellCheck verification script" shellcheck "$ROOT/docs/setup/setup-checks.sh"
else
    skip "ShellCheck unavailable"
fi

if [[ ! -d "$ROOT/docs/backups" ]]; then
    pass "Backup directory removed; no backup packages to discover"
elif [[ -f "$ROOT/docs/backups/COLCON_IGNORE" ]]; then
    pass "Backup directory excluded from Colcon discovery"
else
    fail "docs/backups exists without COLCON_IGNORE"
fi

SOURCE_IGNORE_FILES=""
if SOURCE_IGNORE_FILES="$(find "$ROOT/src" -type f -name COLCON_IGNORE -print 2>/dev/null)"; then
    if [[ -n "$SOURCE_IGNORE_FILES" ]]; then
        printf '  INFO: COLCON_IGNORE files under src:\n'
        while IFS= read -r ignore_file; do
            [[ -n "$ignore_file" ]] && printf '    %s\n' "$ignore_file"
        done <<<"$SOURCE_IGNORE_FILES"
    else
        pass "No COLCON_IGNORE files under src"
    fi
else
    warn "Could not inspect COLCON_IGNORE files under src"
fi

for pkg in robot_control my_arm_description; do
    for ignore_file in "$ROOT/src/COLCON_IGNORE" "$ROOT/src/$pkg/COLCON_IGNORE"; do
        if [[ -f "$ignore_file" ]]; then
            fail "$ignore_file excludes expected package $pkg"
        fi
    done
done

COLCON_DISCOVERY_OK=0
COLCON_LIST_OUTPUT=""
if (( COLCON_OK )); then
    if COLCON_LIST_OUTPUT="$(colcon list --base-paths "$ROOT")"; then
        COLCON_DISCOVERY_OK=1
        pass "Colcon discovers workspace packages from the root"

        for pkg in robot_control my_arm_description; do
            if awk -v wanted="$pkg" '$1 == wanted { found = 1 } END { exit !found }' \
                <<<"$COLCON_LIST_OUTPUT"; then
                pass "Colcon discovers expected package: $pkg"
            else
                fail "Colcon does not discover expected package: $pkg"
            fi
        done

        DUPLICATE_PACKAGES="$(printf '%s\n' "$COLCON_LIST_OUTPUT" |
            awk 'NF { count[$1]++ } END { for (name in count) if (count[name] > 1) print name }')"
        if [[ -z "$DUPLICATE_PACKAGES" ]]; then
            pass "No duplicate package names in root Colcon discovery"
        else
            fail "Duplicate package names in root Colcon discovery:"
            printf '    %s\n' "$DUPLICATE_PACKAGES"
        fi

        BACKUP_PACKAGES="$(awk '$2 ~ /(^|\/)docs\/backups(\/|$)/ { print $1 " (" $2 ")" }' \
            <<<"$COLCON_LIST_OUTPUT")"
        if [[ -z "$BACKUP_PACKAGES" ]]; then
            pass "Colcon does not discover packages from docs/backups"
        else
            fail "Colcon discovered package(s) from docs/backups:"
            printf '    %s\n' "$BACKUP_PACKAGES"
        fi
    else
        fail "Colcon package discovery failed from the workspace root"
    fi
else
    skip "Colcon package discovery: Colcon unavailable"
fi

DESCRIPTION_DIR="$ROOT/src/my_arm_description/urdf"
if [[ -d "$DESCRIPTION_DIR" ]]; then
    if DESCRIPTION_FILES="$(find "$DESCRIPTION_DIR" -type f \( -name '*.urdf' -o -name '*.xacro' \) -print 2>/dev/null)"; then
        if [[ -n "$DESCRIPTION_FILES" ]]; then
            pass "Robot description URDF/Xacro files exist"
            while IFS= read -r description_file; do
                [[ -n "$description_file" ]] || continue
                case "$description_file" in
                    *.xacro)
                        if command -v xacro >/dev/null 2>&1; then
                            if xacro "$description_file" >/dev/null 2>&1; then
                                pass "Xacro expands: ${description_file#"$ROOT"/}"
                            else
                                fail "Xacro expansion failed: ${description_file#"$ROOT"/}"
                            fi
                        else
                            skip "Xacro validation unavailable for ${description_file#"$ROOT"/}"
                        fi
                        ;;
                    *.urdf)
                        if command -v check_urdf >/dev/null 2>&1; then
                            if check_urdf "$description_file" >/dev/null 2>&1; then
                                pass "URDF parses: ${description_file#"$ROOT"/}"
                            else
                                fail "URDF parser rejected ${description_file#"$ROOT"/}"
                            fi
                        else
                            skip "check_urdf unavailable for ${description_file#"$ROOT"/}"
                        fi
                        ;;
                esac
            done <<<"$DESCRIPTION_FILES"
        else
            warn "No URDF/Xacro files under src/my_arm_description/urdf"
        fi
    else
        fail "Could not inspect src/my_arm_description/urdf"
    fi
else
    warn "Robot description directory is not implemented: src/my_arm_description/urdf"
fi

section "3. Python Environment Integrity"

if [[ -x "$SYSTEM_PYTHON" ]]; then
    if SYSTEM_IMPORT_INFO="$("$SYSTEM_PYTHON" - <<'PY' 2>&1
import cv2
import numpy
from cv_bridge import CvBridge

print("NumPy:", numpy.__version__, numpy.__file__)
print("OpenCV:", cv2.__version__)
print("cv_bridge:", CvBridge.__module__)
PY
    )"; then
        pass "System Python imports NumPy, OpenCV and cv_bridge"
        printf '    %s\n' "$SYSTEM_IMPORT_INFO"
    else
        fail "System Python imports NumPy, OpenCV and cv_bridge"
        printf '    %s\n' "$SYSTEM_IMPORT_INFO" | head -n 5
    fi

    if SYSTEM_ROUNDTRIP_OUTPUT="$("$SYSTEM_PYTHON" - <<'PY' 2>&1
import numpy as np
from cv_bridge import CvBridge

image = np.zeros((16, 16, 3), dtype=np.uint8)
bridge = CvBridge()
message = bridge.cv2_to_imgmsg(image, encoding="bgr8")
result = bridge.imgmsg_to_cv2(message, desired_encoding="bgr8")

assert message.encoding == "bgr8", message.encoding
assert result.shape == image.shape, (result.shape, image.shape)
assert result.dtype == image.dtype, (result.dtype, image.dtype)
assert np.array_equal(result, image), "round-trip pixels differ"
print(f"shape={result.shape}, dtype={result.dtype}, encoding={message.encoding}")
PY
    )"; then
        pass "System Python cv_bridge image round-trip"
        printf '    %s\n' "$SYSTEM_ROUNDTRIP_OUTPUT"
    else
        fail "System Python cv_bridge image round-trip"
        printf '    %s\n' "$SYSTEM_ROUNDTRIP_OUTPUT" | head -n 5
    fi
else
    fail "System Python missing or not executable: $SYSTEM_PYTHON"
fi

if [[ -x "$DEV_PYTHON" ]]; then
    if DEV_PYTHON_INFO="$("$DEV_PYTHON" - "$ROOT/.venv" <<'PY' 2>&1
from pathlib import Path
import sys

import numpy
import pandas
import scipy
import serial

expected_prefix = Path(sys.argv[1]).resolve()
actual_prefix = Path(sys.prefix).resolve()
if actual_prefix != expected_prefix:
    raise SystemExit(
        f"Interpreter prefix {actual_prefix} is outside expected environment {expected_prefix}"
    )

print("Interpreter:", sys.executable)
print("Environment:", sys.prefix)
print("NumPy:", numpy.__version__)
print("SciPy:", scipy.__version__)
print("pandas:", pandas.__version__)
print("pyserial:", serial.__version__)
PY
    )"; then
        pass "Development virtual environment imports expected packages"
        printf '    %s\n' "$DEV_PYTHON_INFO"
    else
        fail "Development virtual environment imports expected packages"
        printf '    %s\n' "$DEV_PYTHON_INFO" | head -n 5
    fi
    optional_check "Development Black formatter available" "$DEV_PYTHON" -m black --version
else
    fail "Development virtual environment missing or not executable: $DEV_PYTHON"
fi

section "3A. Firmware Toolchain"

DEV_PYTHON="/opt/robot-tools-venv/bin/python"

if [[ -x "$DEV_PYTHON" ]]; then
    pass "Canonical development Python exists"

    if "$DEV_PYTHON" -c "import serial, numpy, scipy, pandas"; then
        pass "Core development Python dependencies import"
    else
        fail "Core development Python dependencies cannot import"
    fi
else
    fail "Canonical development Python missing"
fi

if command -v pio >/dev/null 2>&1; then
    pass "PlatformIO CLI available"
    pio --version
elif "$DEV_PYTHON" -m platformio --version >/dev/null 2>&1; then
    pass "PlatformIO available through development Python"
else
    warn "PlatformIO unavailable; firmware builds not verified"
fi

if /opt/robot-tools-venv/bin/python -m platformio --version; then
    pass "PlatformIO CLI starts successfully"
else
    fail "PlatformIO CLI failed to start"
fi

section "4. Build, Registration and Automated Tests"

BUILD_OK=0
if [[ "$MODE" == "full" ]] && (( ROS_UNDERLAY_OK && COLCON_OK && COLCON_DISCOVERY_OK )); then
    if colcon build --symlink-install; then
        BUILD_OK=1
        pass "Workspace colcon build succeeds"
    else
        fail "Workspace colcon build failed"
    fi
else
    if [[ "$MODE" == "audit" ]]; then
        skip "Workspace build not run in read-only audit mode"
        warn "Existing build/test artifacts were not revalidated in audit mode"
    else
        skip "Workspace build: ROS underlay, Colcon, or package discovery unavailable"
    fi
fi

OVERLAY_OK=0
if (( BUILD_OK )); then
    if [[ -r "$ROOT/install/setup.bash" ]]; then
        pass "Generated workspace install/setup.bash exists and is readable"
        if source_setup "$ROOT/install/setup.bash"; then
            OVERLAY_OK=1
            pass "Workspace overlay sources after the Humble underlay"
        else
            fail "Workspace overlay sourcing failed"
        fi
    else
        fail "Build succeeded but install/setup.bash is missing or unreadable"
    fi
else
    skip "Workspace overlay sourcing: current build did not succeed"
fi

if (( OVERLAY_OK && ROS_CLI_OK )); then
    if OVERLAY_PACKAGE_LIST="$(ros2 pkg list 2>&1)"; then
        for pkg in robot_control my_arm_description; do
            if grep -Fxq -- "$pkg" <<<"$OVERLAY_PACKAGE_LIST"; then
                pass "$pkg registered in the freshly sourced workspace overlay"
            else
                fail "$pkg not registered in the freshly sourced workspace overlay"
            fi
        done

        if EXECUTABLE_LIST="$(ros2 pkg executables robot_control 2>&1)"; then
            if awk '$1 == "robot_control" && $2 == "robot_node" { found = 1 } END { exit !found }' \
                <<<"$EXECUTABLE_LIST"; then
                pass "robot_control/robot_node executable registered"
            else
                fail "robot_control/robot_node executable not registered"
                printf '    %s\n' "$EXECUTABLE_LIST" | head -n 5
            fi
        else
            fail "Could not query robot_control executable registration"
            printf '    %s\n' "$EXECUTABLE_LIST" | head -n 5
        fi
    else
        fail "ROS package discovery failed after sourcing the workspace overlay"
        printf '    %s\n' "$OVERLAY_PACKAGE_LIST" | head -n 5
    fi
else
    skip "Overlay package/executable registration: build or ROS CLI unavailable"
fi

if command -v rosdep >/dev/null 2>&1; then
    if (( ROS_UNDERLAY_OK )); then
        if rosdep check --from-paths "$ROOT/src" --ignore-src --rosdistro humble; then
            pass "rosdep dependency check"
        else
            fail "rosdep dependency check"
        fi
    else
        skip "rosdep dependency check: ROS underlay unavailable"
    fi
else
    warn "rosdep unavailable; dependency validation not performed"
fi

if (( BUILD_OK && COLCON_OK )); then
    TEST_START_MARKER="$(mktemp)"
    TEST_COMMAND_OK=0
    if colcon test --return-code-on-test-failure; then
        TEST_COMMAND_OK=1
        pass "colcon test command completed successfully"
    else
        fail "colcon test command reported an execution or test failure"
    fi

    TEST_REPORT_FILE="$(mktemp)"
    if colcon test-result --all --verbose >"$TEST_REPORT_FILE" 2>&1; then
        TEST_RESULT_STATUS=0
    else
        TEST_RESULT_STATUS=$?
    fi
    cat "$TEST_REPORT_FILE"
    FRESH_TEST_RESULTS=0

    if [[ -d "$ROOT/build" ]] &&
    find "$ROOT/build" -type f -path '*/test_results/*' \
        -name '*.xml' -newer "$TEST_START_MARKER" -print -quit |
        grep -q .; then
        FRESH_TEST_RESULTS=1
    fi

    rm -f -- "$TEST_START_MARKER"
    TEST_SUMMARY="$(grep -E '^Summary:' "$TEST_REPORT_FILE" | tail -n 1 || true)"
    rm -f -- "$TEST_REPORT_FILE"

    if (( ! TEST_COMMAND_OK )); then
        fail "Colcon test command failed"
    elif (( ! FRESH_TEST_RESULTS )); then
        fail "No fresh test-result XML files were generated by this run"
    elif (( TEST_RESULT_STATUS != 0 )); then
        fail "colcon test-result returned status $TEST_RESULT_STATUS"
    elif [[ "$TEST_SUMMARY" =~ ^Summary:\ ([0-9]+)\ tests?,\ ([0-9]+)\ errors?,\ ([0-9]+)\ failures?,\ ([0-9]+)\ skipped? ]]; then
        TEST_COUNT="${BASH_REMATCH[1]}"
        TEST_ERRORS="${BASH_REMATCH[2]}"
        TEST_FAILURES="${BASH_REMATCH[3]}"
        if (( TEST_COUNT > 0 && TEST_ERRORS == 0 && TEST_FAILURES == 0 )); then
            pass "Current Colcon test results: $TEST_COUNT tests, no errors or failures"
        else
            fail "Colcon test results are not a non-empty zero-failure suite"
        fi
    else
        fail "Could not verify a Colcon test-result summary"
    fi

    if (( ! TEST_COMMAND_OK )); then
        printf '  INFO: A successful result summary does not override the failed test command.\n'
    fi
else
    skip "Automated tests and test-result summary: current build did not succeed"
fi

section "5. Hardware and Serial Access"

if [[ -d /dev/bus/usb ]]; then
    pass "USB bus directory is visible"
    if USB_DEVICE="$(find /dev/bus/usb -type c -print -quit 2>/dev/null)"; then
        if [[ -n "$USB_DEVICE" ]]; then
            pass "USB character devices are visible"
        else
            skip "No USB character devices are currently visible"
        fi
    else
        warn "Could not enumerate USB character devices"
    fi
else
    warn "USB bus directory is unavailable; USB passthrough is not visible"
fi

optional_check "usbip utility available" command -v usbip
optional_check "Teensy loader available" command -v teensy_loader_cli
optional_check "Serial monitor tio available" command -v tio

if command -v git-lfs >/dev/null 2>&1; then
    pass "Git LFS utility installed"
    if LFS_FILES="$(git -C "$ROOT" lfs ls-files 2>&1)"; then
        if [[ -n "$LFS_FILES" ]]; then
            if git -C "$ROOT" lfs env >/dev/null 2>&1; then
                pass "Git LFS configuration is usable for tracked LFS files"
            else
                warn "Git LFS files are tracked but Git LFS configuration is unavailable"
            fi
        else
            skip "No Git LFS-tracked files in this repository"
        fi
    else
        warn "Could not inspect Git LFS-tracked files"
        printf '    %s\n' "$LFS_FILES" | head -n 3
    fi
else
    warn "Git LFS utility unavailable"
fi

SERIAL_FOUND=0
for device in /dev/ttyACM* /dev/ttyUSB*; do
    [[ -e "$device" ]] || continue
    SERIAL_FOUND=1
    if [[ -r "$device" && -w "$device" ]]; then
        pass "Serial device has read/write access: $device"
    else
        warn "Serial device exists without read/write access: $device"
    fi
done

if (( SERIAL_FOUND == 0 )); then
    skip "No /dev/ttyACM* or /dev/ttyUSB* device connected"
fi

if command -v id >/dev/null 2>&1; then
    if id -nG 2>/dev/null | tr ' ' '\n' | grep -Fxq dialout; then
        pass "Current user belongs to dialout group"
    else
        warn "Current user is not in dialout group; serial access may depend on device permissions"
    fi
else
    warn "Cannot check dialout membership because id is unavailable"
fi

section "6. Simulation, GUI and Graphics"

if command -v ign >/dev/null 2>&1; then
    if GAZEBO_VERSION="$(ign gazebo --version 2>&1)"; then
        pass "Gazebo Ignition executable and version query"
        printf '    %s\n' "$GAZEBO_VERSION" | head -n 2
    else
        warn "ign is installed but its Gazebo version query failed"
        printf '    %s\n' "$GAZEBO_VERSION" | head -n 3
    fi
elif command -v gz >/dev/null 2>&1; then
    if GAZEBO_VERSION="$(gz sim --version 2>&1)"; then
        pass "Gazebo executable and version query"
        printf '    %s\n' "$GAZEBO_VERSION" | head -n 2
    else
        warn "gz is installed but its Gazebo version query failed"
        printf '    %s\n' "$GAZEBO_VERSION" | head -n 3
    fi
else
    warn "Gazebo executable unavailable (ign and gz not found)"
fi

if [[ -n "${DISPLAY:-}" || -n "${WAYLAND_DISPLAY:-}" ]]; then
    pass "Display environment configured"
else
    skip "No GUI display configured; headless sessions are allowed"
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
    if [[ -n "${DISPLAY:-}" || -n "${WAYLAND_DISPLAY:-}" ]]; then
        if GLX_OUTPUT="$(glxinfo -B 2>&1)"; then
            RENDERER="$(sed -n 's/^[[:space:]]*OpenGL renderer string: //p' <<<"$GLX_OUTPUT" | head -n 1)"
            if [[ -z "$RENDERER" ]]; then
                warn "glxinfo ran but did not report an OpenGL renderer"
                printf '    %s\n' "$GLX_OUTPUT" | head -n 3
            else
                printf '  INFO: OpenGL renderer: %s\n' "$RENDERER"
                if grep -qiE 'llvmpipe|softpipe|software rasterizer' <<<"$RENDERER"; then
                    warn "Software rendering detected; GPU acceleration is not verified"
                else
                    pass "OpenGL renderer reported; hardware acceleration is not proven"
                fi
            fi
        else
            warn "glxinfo is installed but the renderer query failed"
            printf '    %s\n' "$GLX_OUTPUT" | head -n 3
        fi
    else
        skip "OpenGL renderer query: no display configured"
    fi
else
    skip "glxinfo unavailable; OpenGL renderer was not checked"
fi

optional_check "NVIDIA utility available" command -v nvidia-smi
optional_check "ccache utility available" command -v ccache

section "7. Git and Setup Tooling"

if git -C "$ROOT" rev-parse --show-toplevel >/dev/null 2>&1; then
    pass "Workspace is a Git repository"
    if GIT_STATUS="$(git -C "$ROOT" status --short 2>&1)"; then
        if [[ -n "$GIT_STATUS" ]]; then
            printf '  INFO: Git worktree has changes:\n'
            printf '    %s\n' "$GIT_STATUS"
        else
            pass "Git worktree is clean"
        fi
    else
        warn "Could not report Git worktree status"
        printf '    %s\n' "$GIT_STATUS" | head -n 3
    fi
else
    fail "Workspace Git metadata unavailable"
fi

section "8. Dev Container Configuration"

check "Active Dockerfile exists" \
    test -r "$ROOT/.devcontainer/Dockerfile"

check "Active Dev Container config exists" \
    test -r "$ROOT/.devcontainer/devcontainer.json"

if command -v devcontainer >/dev/null 2>&1; then
    pass "Dev Container CLI available"
else
    skip "Dev Container CLI unavailable; configuration resolution not checked"
fi

if git -C "$ROOT" diff --check; then
    pass "Git diff has no whitespace errors"
else
    fail "Git diff contains whitespace errors"
fi

summary
exit $?
