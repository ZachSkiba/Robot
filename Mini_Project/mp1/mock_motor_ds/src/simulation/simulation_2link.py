import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import re
from mock_motor import MockMotor

# ============================================================
# 📂 PATH SETUP
# ============================================================
script_dir = os.path.dirname(os.path.abspath(__file__))
BASE_LOG_DIR = os.path.normpath(os.path.join(script_dir, "..", "..", "logs"))

existing_runs = [
    f.name for f in os.scandir(BASE_LOG_DIR) 
    if f.is_dir() and f.name.startswith("arm_run")
]
if existing_runs:
    run_numbers = [int(re.search(r"arm_run_?(\d+)", r).group(1)) for r in existing_runs if re.search(r"arm_run_?(\d+)", r)]
    next_run = max(run_numbers) + 1 if run_numbers else 1
else:
    next_run = 1

RUN_LOG_DIR = os.path.join(BASE_LOG_DIR, f"arm_run_{next_run}")
os.makedirs(RUN_LOG_DIR, exist_ok=True)
print(f"\n📂 Logging Digital Twin (Smooth Motion) to: {RUN_LOG_DIR}\n")

# ============================================================
# ⚙️ HARDWARE CONFIG (TEENSY 4.1 + NEMA 17 PRO SPECS)
# ============================================================
L1 = 15.0  # cm
L2 = 15.0  # cm

HZ = 1000
DT = 1.0 / HZ 

# Joint-space limits (per motor)
MAX_SPEED_DEG = 1080.0  # deg/s per joint
MAX_ACCEL_DEG = 4000.0  # deg/s^2 per joint

# Default "home" position (like real robots)
# This is where the robot starts before every path
# Using a central position within typical workspace (most paths are x=5-28, y=0-18)
# This position: J1 ≈ 33.7°, J2 ≈ 0° (safe, centered configuration)
HOME_POSITION_CARTESIAN = (25.0, 8.0)  # (25, 8) cm - central workspace position

# ============================================================
# 🧠 KINEMATICS ENGINE
# ============================================================
def forward_kinematics(theta1, theta2):
    x = L1 * np.cos(theta1) + L2 * np.cos(theta1 + theta2)
    y = L1 * np.sin(theta1) + L2 * np.sin(theta1 + theta2)
    return x, y

def inverse_kinematics(x, y):
    dist = np.sqrt(x**2 + y**2)
    if dist > (L1 + L2) or dist == 0: 
        return None, None 
    cos_theta2 = (x**2 + y**2 - L1**2 - L2**2) / (2 * L1 * L2)
    cos_theta2 = np.clip(cos_theta2, -1.0, 1.0)
    theta2 = np.arccos(cos_theta2) 
    theta1 = np.arctan2(y, x) - np.arctan2(L2 * np.sin(theta2), L1 + L2 * np.cos(theta2))
    return theta1, theta2

# ============================================================
# 🎨 PATH DEFINITIONS (EASILY SWAPPABLE)
# ============================================================

def path_straight_line(num_points=100):
    """Simple horizontal line"""
    x = np.linspace(5.0, 28.0, num_points)
    y = np.zeros_like(x)
    return x, y

def path_diagonal(num_points=100):
    """Diagonal line"""
    x = np.linspace(5.0, 25.0, num_points)
    y = np.linspace(0.0, 15.0, num_points)
    return x, y

def path_circle(num_points=200):
    """Circular path"""
    center_x, center_y = 15.0, 10.0
    radius = 8.0
    theta = np.linspace(0, 2*np.pi, num_points)
    x = center_x + radius * np.cos(theta)
    y = center_y + radius * np.sin(theta)
    return x, y

def path_square(num_points=200):
    """Square path"""
    points_per_side = num_points // 4
    
    # Bottom edge
    x1 = np.linspace(10.0, 20.0, points_per_side)
    y1 = np.full_like(x1, 5.0)
    
    # Right edge
    x2 = np.full(points_per_side, 20.0)
    y2 = np.linspace(5.0, 15.0, points_per_side)
    
    # Top edge
    x3 = np.linspace(20.0, 10.0, points_per_side)
    y3 = np.full_like(x3, 15.0)
    
    # Left edge
    x4 = np.full(points_per_side, 10.0)
    y4 = np.linspace(15.0, 5.0, points_per_side)
    
    x = np.concatenate([x1, x2, x3, x4])
    y = np.concatenate([y1, y2, y3, y4])
    return x, y

def path_zigzag(num_points=150):
    """Zigzag pattern"""
    num_zigs = 5
    x = np.linspace(8.0, 25.0, num_points)
    y = 8.0 + 6.0 * np.sin(num_zigs * 2 * np.pi * (x - x[0]) / (x[-1] - x[0]))
    return x, y

def path_letter_s(num_points=200):
    """S-curve path"""
    t = np.linspace(0, 2*np.pi, num_points)
    x = 15.0 + 8.0 * np.sin(t)
    y = 10.0 + 8.0 * np.sin(2*t)
    return x, y

def path_via_points(num_points=150):
    """Path through specific waypoints"""
    waypoints_x = [8.0, 15.0, 22.0, 18.0, 12.0]
    waypoints_y = [5.0, 12.0, 8.0, 15.0, 10.0]
    
    # Interpolate smoothly between waypoints
    t = np.linspace(0, len(waypoints_x)-1, num_points)
    x = np.interp(t, np.arange(len(waypoints_x)), waypoints_x)
    y = np.interp(t, np.arange(len(waypoints_y)), waypoints_y)
    return x, y

def path_heart(num_points=200):
    """Heart-shaped path"""
    t = np.linspace(0, 2*np.pi, num_points)
    
    # Standard parametric heart equations
    heart_x = 16 * np.sin(t)**3
    heart_y = 13*np.cos(t) - 5*np.cos(2*t) - 2*np.cos(3*t) - np.cos(4*t)
    
    # Scale to fit workspace (robot reach = 30 cm)
    # Creates ~8cm heart centered at (15, 10)
    scale = 4.0
    center_x = 15.0
    center_y = 10.0
    
    x = center_x + scale * heart_x / 16.0
    y = center_y + scale * heart_y / 17.0
    
    return x, y

# ============================================================
# 🔧 SMOOTH JOINT TRAJECTORY GENERATOR
# ============================================================

def generate_smooth_joint_trajectory(path_x, path_y, cartesian_speed, dt,
                                     max_joint_vel, max_joint_accel):
    """
    Real-world Cartesian-based trajectory generator.

    Key idea:
    - Time is allocated in CARTESIAN space (constant end-effector speed)
    - IK is solved at each time step
    - Joint velocities are limited AFTER IK
    - Acceleration limits are enforced incrementally

    Returns:
    time_points,
    j1_positions, j1_velocities,
    j2_positions, j2_velocities
    """

    # --------------------------------------------------------
    # 1. Compute Cartesian arc-length and timing
    # --------------------------------------------------------
    dx = np.diff(path_x)
    dy = np.diff(path_y)
    segment_lengths = np.sqrt(dx**2 + dy**2)

    total_distance = np.sum(segment_lengths)
    total_time = total_distance / cartesian_speed

    cumulative_dist = np.concatenate([[0.0], np.cumsum(segment_lengths)])
    waypoint_times = cumulative_dist / cumulative_dist[-1] * total_time

    # Dense control timeline
    time_points = np.arange(0.0, total_time, dt)

    # --------------------------------------------------------
    # 2. Interpolate Cartesian position vs time
    # --------------------------------------------------------
    x_traj = np.interp(time_points, waypoint_times, path_x)
    y_traj = np.interp(time_points, waypoint_times, path_y)

    # --------------------------------------------------------
    # 3. Inverse kinematics at EACH timestep
    # --------------------------------------------------------
    j1_pos = np.zeros_like(time_points)
    j2_pos = np.zeros_like(time_points)

    for i, (x, y) in enumerate(zip(x_traj, y_traj)):
        t1, t2 = inverse_kinematics(x, y)
        if t1 is None:
            raise RuntimeError("IK failure during trajectory generation")

        j1_pos[i] = np.degrees(t1)
        j2_pos[i] = np.degrees(t2)

    # --------------------------------------------------------
    # 4. Velocity estimation (finite difference)
    # --------------------------------------------------------
    j1_vel_raw = np.gradient(j1_pos, dt)
    j2_vel_raw = np.gradient(j2_pos, dt)

    # --------------------------------------------------------
    # 5. Apply velocity limits
    # --------------------------------------------------------
    j1_vel_limited = np.clip(j1_vel_raw, -max_joint_vel, max_joint_vel)
    j2_vel_limited = np.clip(j2_vel_raw, -max_joint_vel, max_joint_vel)

    # --------------------------------------------------------
    # 6. Enforce acceleration limits (incremental)
    # --------------------------------------------------------
    j1_vel = np.zeros_like(j1_vel_limited)
    j2_vel = np.zeros_like(j2_vel_limited)

    for i in range(1, len(time_points)):
        dv1 = j1_vel_limited[i] - j1_vel[i-1]
        dv2 = j2_vel_limited[i] - j2_vel[i-1]

        max_dv = max_joint_accel * dt

        dv1 = np.clip(dv1, -max_dv, max_dv)
        dv2 = np.clip(dv2, -max_dv, max_dv)

        j1_vel[i] = j1_vel[i-1] + dv1
        j2_vel[i] = j2_vel[i-1] + dv2

    # --------------------------------------------------------
    # 7. Re-integrate position from constrained velocity
    # --------------------------------------------------------
    j1_pos_smooth = np.zeros_like(j1_pos)
    j2_pos_smooth = np.zeros_like(j2_pos)

    j1_pos_smooth[0] = j1_pos[0]
    j2_pos_smooth[0] = j2_pos[0]

    for i in range(1, len(time_points)):
        j1_pos_smooth[i] = j1_pos_smooth[i-1] + j1_vel[i] * dt
        j2_pos_smooth[i] = j2_pos_smooth[i-1] + j2_vel[i] * dt

    return (
        time_points,
        j1_pos_smooth, j1_vel,
        j2_pos_smooth, j2_vel
    )

# ============================================================
# ▶️ SIMULATION RUNNER
# ============================================================

def run_digital_twin_simulation(path_function=path_straight_line, 
                                 cartesian_speed=20.0,
                                 path_resolution=200):
    """
    Run 2-link arm simulation with smooth joint-space motion.
    
    Args:
        path_function: Function returning (x_array, y_array) waypoints
        cartesian_speed: End-effector speed in cm/s
        path_resolution: Number of waypoints in Cartesian path
    """
    
    print(f"🎨 Path: {path_function.__name__}")
    print(f"🏃 Cartesian Speed: {cartesian_speed} cm/s")
    print(f"⚙️  Control Rate: {HZ} Hz")
    
    # 1. Initialize motors at HOME position (like real robots)
    home_j1, home_j2 = inverse_kinematics(*HOME_POSITION_CARTESIAN)
    if home_j1 is None:
        print("❌ Invalid HOME position!")
        return
    
    motor1 = MockMotor(max_velocity=MAX_SPEED_DEG, max_accel=MAX_ACCEL_DEG)
    motor2 = MockMotor(max_velocity=MAX_SPEED_DEG, max_accel=MAX_ACCEL_DEG)
    
    # Set motors to home position
    motor1.actual_pos = np.degrees(home_j1)
    motor2.actual_pos = np.degrees(home_j2)
    
    home_x, home_y = HOME_POSITION_CARTESIAN
    print(f"🏠 Home Position: ({home_x:.1f}, {home_y:.1f}) cm | J1: {np.degrees(home_j1):.1f}° J2: {np.degrees(home_j2):.1f}°")
    
    # 2. Generate Cartesian path
    path_x, path_y = path_function(num_points=path_resolution)
    
    # 3. Add move-to-start segment (from HOME to first waypoint)
    start_x, start_y = path_x[0], path_y[0]
    
    # Generate straight line from home to path start
    move_to_start_points = 50
    approach_x = np.linspace(home_x, start_x, move_to_start_points)
    approach_y = np.linspace(home_y, start_y, move_to_start_points)
    
    # Prepend approach path to main path
    full_path_x = np.concatenate([approach_x, path_x])
    full_path_y = np.concatenate([approach_y, path_y])
    
    print(f"📍 Path Start: ({start_x:.1f}, {start_y:.1f}) cm")
    
    # 4. Convert to smooth joint trajectories
    (times, 
     j1_pos, j1_vel, 
     j2_pos, j2_vel) = generate_smooth_joint_trajectory(
        full_path_x, full_path_y, 
        cartesian_speed, 
        DT,
        MAX_SPEED_DEG * 0.8,  # Safety margin
        MAX_ACCEL_DEG
    )
    
    print(f"⏱️  Total Duration: {times[-1]:.2f} seconds ({len(times)} frames)")
    print(f"🦾 Executing: Home → Start → Path → End")
    
    # 5. Execute trajectory
    log_data = []
    command_id = 1
    
    for i in range(len(times)):
        # Target from smooth trajectory
        target_j1 = j1_pos[i]
        target_j2 = j2_pos[i]
        vel_cmd_j1 = j1_vel[i]
        vel_cmd_j2 = j2_vel[i]
        
        # Update motors with smooth commands
        actual_deg1 = motor1.update(target_j1, vel_cmd_j1, DT)
        actual_deg2 = motor2.update(target_j2, vel_cmd_j2, DT)
        
        # Forward kinematics for actual position
        actual_rad1 = np.radians(actual_deg1)
        actual_rad2 = np.radians(actual_deg2)
        real_x, real_y = forward_kinematics(actual_rad1, actual_rad2)
        
        # Target position in Cartesian (for error calculation)
        target_rad1 = np.radians(target_j1)
        target_rad2 = np.radians(target_j2)
        target_x, target_y = forward_kinematics(target_rad1, target_rad2)
        
        # Log data
        log_data.append({
            "timestamp_ms": int(times[i] * 1000),
            "command_id": command_id,
            "target_x": round(target_x, 3), 
            "target_y": round(target_y, 3),
            "real_x": round(real_x, 3), 
            "real_y": round(real_y, 3),
            "error": round(np.sqrt((target_x - real_x)**2 + (target_y - real_y)**2), 3),
            "motor1_pos": round(actual_deg1, 2), 
            "motor2_pos": round(actual_deg2, 2),
            "motor1_vel": round(j1_vel[i], 2),
            "motor2_vel": round(j2_vel[i], 2),
            "velocity": round(cartesian_speed, 2),
            "pwm_effort": 127,
            "hz": HZ
        })
    
    # 5. Save results
    filename = os.path.join(RUN_LOG_DIR, "arm_2link_log.csv")
    df = pd.DataFrame(log_data)
    df.to_csv(filename, index=False)
    
    max_error = df['error'].max()
    avg_error = df['error'].mean()
    
    print(f"✅ Simulation Complete")
    print(f"   Max Error: {max_error:.4f} cm")
    print(f"   Avg Error: {avg_error:.4f} cm")
    print(f"   Data saved to: {filename}")

# ============================================================
# 🚀 MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    # ========================================================
    # 🎯 AUTO-DISCOVER ALL PATH FUNCTIONS
    # ========================================================
    
    # Get all path functions from global scope
    import inspect
    current_module = inspect.currentframe().f_globals
    
    # Find all functions starting with "path_"
    path_functions = [
        (name, func) for name, func in current_module.items()
        if callable(func) and name.startswith('path_') and inspect.isfunction(func)
    ]
    
    # Sort by name for consistent ordering
    path_functions.sort(key=lambda x: x[0])
    
    if not path_functions:
        print("❌ No path functions found!")
        exit(1)
    
    # Auto-select speed and resolution based on path type
    # speed (cm/s) = Cartesian end-effector speed along the path
    # resolution (waypoints) = Number of points defining the path (higher = smoother curves)
    speed_config = {
        'path_straight_line': (20.0, 100),   # Fast, simple path
        'path_diagonal': (20.0, 100),        # Fast, simple path
        'path_circle': (15.0, 200),          # Medium speed, high resolution for curves
        'path_square': (18.0, 200),          # Medium-fast, corners need resolution
        'path_zigzag': (12.0, 150),          # Slower for sharp turns
        'path_letter_s': (12.0, 200),        # Slower, complex curves need resolution
        'path_via_points': (15.0, 150),      # Medium speed, smooth interpolation
        'path_heart': (10.0, 250)            # Slow, very detailed curves
    }
    
    # Display menu
    print("\n" + "="*70)
    print("🎨 SELECT PATH TYPE")
    print("="*70)
    for i, (name, func) in enumerate(path_functions, 1):
        # Format name: path_straight_line -> Straight Line
        display_name = name.replace('path_', '').replace('_', ' ').title()
        
        # Extract docstring for description
        doc = func.__doc__ or "No description"
        doc_first_line = doc.strip().split('\n')[0]
        
        # Get speed and resolution for this path
        speed, resolution = speed_config.get(name, (15.0, 150))
        
        print(f"  {i}. {display_name:<20} - {doc_first_line}")
        print(f"     └─ {speed} cm/s, {resolution} waypoints")
    print("="*70)
    
    # Get user input
    while True:
        try:
            choice = input(f"\nEnter choice (1-{len(path_functions)}): ").strip()
            choice_idx = int(choice) - 1
            
            if 0 <= choice_idx < len(path_functions):
                selected_name, selected_func = path_functions[choice_idx]
                display_name = selected_name.replace('path_', '').replace('_', ' ').title()
                print(f"\n✅ Selected: {display_name}\n")
                break
            else:
                print(f"❌ Invalid choice. Please enter 1-{len(path_functions)}")
        except (ValueError, KeyboardInterrupt):
            print("\n❌ Invalid input. Please enter a number.")
            continue
    
    # Use configured values or defaults
    cartesian_speed, path_resolution = speed_config.get(selected_name, (15.0, 150))
    
    # Run simulation with selected path
    run_digital_twin_simulation(
        path_function=selected_func,
        cartesian_speed=cartesian_speed,
        path_resolution=path_resolution
    )