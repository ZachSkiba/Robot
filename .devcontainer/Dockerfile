# ============================================================
# 6DOF Robot Arm — ROS2 Humble + MoveIt2 Dev Container
# Production-Ready, USB & GUI Safe
# ============================================================

FROM osrf/ros:humble-desktop

SHELL ["/bin/bash", "-lc"]

ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=humble
ENV ROS_WS=/workspace
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# ------------------------------------------------------------
# 1. System Essentials & Robotics Tools
# ------------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    sudo git git-lfs curl wget build-essential cmake pkg-config \
    python3-pip python3-venv python3-colcon-common-extensions \
    python3-rosdep python3-vcstool python3-argcomplete \
    udev usbutils mesa-utils libgl1-mesa-dri libgl1-mesa-glx \
    tio teensy-loader-cli \
    ros-humble-moveit \
    ros-humble-ros2-control \
    ros-humble-ros2-controllers \
    ros-humble-xacro \
    ros-humble-joint-state-publisher-gui \
    ros-humble-ros-gz \
    ros-humble-ros-gz-bridge \
    ros-humble-tf2-tools \
    && if apt-cache show ros-humble-foxglove-bridge >/dev/null 2>&1; then \
         apt-get install -y --no-install-recommends ros-humble-foxglove-bridge; \
       else \
         echo "ros-humble-foxglove-bridge not found in apt sources; skipping"; \
       fi \
    && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------
# 2. Create non-root devuser
# ------------------------------------------------------------
ARG USERNAME=devuser
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && usermod -aG sudo,dialout $USERNAME \
    && echo "$USERNAME ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# ------------------------------------------------------------
# 3. Initialize rosdep
# ------------------------------------------------------------
RUN rosdep init 2>/dev/null || true

USER $USERNAME
RUN rosdep update || true

# ------------------------------------------------------------
# 4. ROS Sourcing Automation
# ------------------------------------------------------------
RUN echo "source /opt/ros/$ROS_DISTRO/setup.bash" >> ~/.bashrc \
    && echo "export PATH=$HOME/.local/bin:$PATH" >> ~/.bashrc \
    && echo "if [ -f /workspace/install/setup.bash ]; then source /workspace/install/setup.bash; fi" >> ~/.bashrc \
    && echo "if [ -f /workspace/Robot/install/setup.bash ]; then source /workspace/Robot/install/setup.bash; fi" >> ~/.bashrc \
    && echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" >> ~/.bashrc

# ------------------------------------------------------------
# 5. Workspace Setup
# ------------------------------------------------------------
WORKDIR /workspace
RUN mkdir -p /workspace/src /workspace/build /workspace/install /workspace/log

# ------------------------------------------------------------
# 6. Python Tools
# ------------------------------------------------------------
RUN pip3 install --upgrade pip "setuptools<80" wheel black numpy scipy matplotlib pandas pyserial jupyterlab

CMD ["/bin/bash"]
#nice