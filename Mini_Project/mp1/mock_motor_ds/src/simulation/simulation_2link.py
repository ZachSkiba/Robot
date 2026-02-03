import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import re
from mock_motor import MockMotor
import inspect

# ============================================================
# 📂 PATH SETUP
# ============================================================
script_dir = os.path.dirname(os.path.abspath(__file__))
BASE_LOG_DIR = os.path.normpath(os.path.join(script_dir, "..", "..", "logs"))

existing_runs = [
    f.name for f in os.scandir(BASE_LOG_DIR) 
    if f.is_dir() and f.name.startswith("arm_run_3d")
]
if existing_runs:
    run_numbers = [int(re.search(r"arm_run_3d_?(\d+)", r).group(1)) for r in existing_runs if re.search(r"arm_run_3d_?(\d+)", r)]
    next_run = max(run_numbers) + 1 if run_numbers else 1
else:
    next_run = 1

RUN_LOG_DIR = os.path.join(BASE_LOG_DIR, f"arm_run_3d_{next_run}")
os.makedirs(RUN_LOG_DIR, exist_ok=True)
print(f"\n📂 Logging 3D Digital Twin to: {RUN_LOG_DIR}\n")

# ============================================================
# ⚙️ HARDWARE CONFIG (RESEARCH EDITION)
# ============================================================
# Robot Geometry
L_BASE = 10.0   # cm (Height of the base pivot above the table - NEMA 23 stack is tall)
L1 = 20.0       # cm (Shoulder to Elbow)
L2 = 20.0       # cm (Elbow to Wrist)
MAX_REACH = L1 + L2 - 0.1

# Simulation Timing
HZ = 1000
DT = 1.0 / HZ 

# 🏗️ DYNAMICS CONSTANTS (MASS & GRAVITY)
G = 9.81  # m/s^2

# Link 1 (Shoulder) lifts: Link 1 Structure + Elbow Motor
M_LINK1 = 0.4          # kg (Aluminum Tube + Brackets)
M_ELBOW_MOTOR = 0.5    # kg (NEMA 17 + Planetary Gearbox)

# Link 2 (Elbow) lifts: Link 2 Structure + Wrist/Gripper Assembly
M_LINK2 = 0.3          # kg (Tube)
M_WRIST_ASSEMBLY = 0.6 # kg (Wrist P + Wrist R + Gripper - Heavy!)

# Default Home (Safe, centered position in 3D space)
# X=20, Y=0, Z=20 (Centered in front of robot, mid-height)
HOME_POSITION_CARTESIAN = (20.0, 0.0, 20.0) 

# ============================================================
# 🧠 PHYSICS ENGINE (KINEMATICS + DYNAMICS)
# ============================================================
def forward_kinematics(theta_base, theta_shoulder, theta_elbow):
    """Computes (x, y, z) from (base, shoulder, elbow) angles in radians."""
    r = L1 * np.cos(theta_shoulder) + L2 * np.cos(theta_shoulder + theta_elbow)
    z_arm = L1 * np.sin(theta_shoulder) + L2 * np.sin(theta_shoulder + theta_elbow)
    
    z = z_arm + L_BASE
    x = r * np.cos(theta_base)
    y = r * np.sin(theta_base)
    return x, y, z

# Global variable to track the previous base angle
last_base_angle_rad = 0.0

def inverse_kinematics(x, y, z):
    """Computes (base, shoulder, elbow) angles from (x, y, z)."""
    global last_base_angle_rad

    # 1. Base Angle (Theta 0) with unwrap logic
    current_base = np.arctan2(y, x)
    diff = current_base - last_base_angle_rad
    while diff > np.pi: diff -= 2 * np.pi
    while diff < -np.pi: diff += 2 * np.pi
    theta_base = last_base_angle_rad + diff
    last_base_angle_rad = theta_base 

    # 2. Convert to Planar Problem (r, z)
    r_target = np.sqrt(x**2 + y**2)
    z_target = z - L_BASE
    
    # Check reach
    dist = np.sqrt(r_target**2 + z_target**2)
    if dist > (L1 + L2) or dist == 0: 
        return None, None, None 
        
    # 3. Solve Planar IK (Shoulder, Elbow)
    cos_theta2 = (r_target**2 + z_target**2 - L1**2 - L2**2) / (2 * L1 * L2)
    cos_theta2 = np.clip(cos_theta2, -1.0, 1.0)
    theta_elbow = np.arccos(cos_theta2) 
    
    k1 = L1 + L2 * np.cos(theta_elbow)
    k2 = L2 * np.sin(theta_elbow)
    theta_shoulder = np.arctan2(z_target, r_target) - np.arctan2(k2, k1)
    
    return theta_base, theta_shoulder, theta_elbow

def calculate_gravity_torques(theta_shoulder, theta_elbow):
    """
    Calculates the torque (Nm) required to hold the arm against gravity.
    Angles in Radians. 0 rad = Horizontal. Positive = Up.
    """
    # Lengths in Meters for Torque Calculation
    l1_m = L1 / 100.0
    l2_m = L2 / 100.0
    
    # Global angle of forearm relative to horizon
    global_angle_elbow = theta_shoulder + theta_elbow
    
    # --- 1. Forces on ELBOW Joint (J3) ---
    # Lift Link 2 (assumed COM at 1/2 length) + Wrist/Payload (at full length)
    torque_elbow = (
        (M_LINK2 * G * (l2_m/2) * np.cos(global_angle_elbow)) + 
        (M_WRIST_ASSEMBLY * G * l2_m * np.cos(global_angle_elbow))
    )
    
    # --- 2. Forces on SHOULDER Joint (J2) ---
    # Lift Link 1 (COM at 1/2) + Elbow Motor (at L1) + The whole Forearm load
    
    # Torque from Link 1 Mass
    t_link1 = M_LINK1 * G * (l1_m/2) * np.cos(theta_shoulder)
    
    # Torque from Elbow Motor Mass (Point mass at end of L1)
    t_elbow_motor = M_ELBOW_MOTOR * G * l1_m * np.cos(theta_shoulder)
    
    # Torque from Forearm Mass (Link 2 + Wrist) acting on Shoulder lever arm
    # Horizontal distance from shoulder pivot
    dist_link2_com = l1_m * np.cos(theta_shoulder) + (l2_m/2) * np.cos(global_angle_elbow)
    dist_wrist_com = l1_m * np.cos(theta_shoulder) + l2_m * np.cos(global_angle_elbow)
    
    t_link2_on_shoulder = M_LINK2 * G * dist_link2_com
    t_wrist_on_shoulder = M_WRIST_ASSEMBLY * G * dist_wrist_com
    
    torque_shoulder = t_link1 + t_elbow_motor + t_link2_on_shoulder + t_wrist_on_shoulder
    
    return torque_shoulder, torque_elbow

# ============================================================
# 🎨 3D PATH DEFINITIONS
# ============================================================

def path_360_spin(num_points=400):
    """Rotates the arm in a full 360 degree circle at fixed reach"""
    theta = np.linspace(0, 2 * np.pi, num_points)
    radius = 20.0 # Increased for larger arm
    z_height = 20.0
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    z = np.full_like(x, z_height)
    return x, y, z

def path_pick_and_place(num_points=300):
    """Simulates picking up an object and moving it"""
    waypoints = [
        (25, 10, 10), # Hover
        (25, 10, 2),  # DOWN (Grab)
        (25, 10, 10), # UP (Lift)
        (25, -10, 10),# MOVE
        (25, -10, 2), # DOWN (Place)
        (25, -10, 10) # UP (Retract)
    ]
    x, y, z = [], [], []
    points_per_leg = num_points // (len(waypoints) - 1)
    for i in range(len(waypoints)-1):
        p1, p2 = waypoints[i], waypoints[i+1]
        x.extend(np.linspace(p1[0], p2[0], points_per_leg))
        y.extend(np.linspace(p1[1], p2[1], points_per_leg))
        z.extend(np.linspace(p1[2], p2[2], points_per_leg))
    return np.array(x), np.array(y), np.array(z)

def path_drawing_circle(num_points=200):
    """Draws a circle on a 'whiteboard' at Z=10cm"""
    center_x, center_y = 25.0, 0.0
    radius = 8.0
    z_height = 10.0
    theta = np.linspace(0, 2*np.pi, num_points)
    x = center_x + radius * np.cos(theta)
    y = center_y + radius * np.sin(theta)
    z = np.full_like(x, z_height)
    return x, y, z

def path_drawing_square(num_points=200):
    """Draws a square at Z=10cm"""
    z_height = 10.0
    points_per_side = num_points // 4
    c1 = (20, 8); c2 = (30, 8); c3 = (30, -8); c4 = (20, -8)
    x = np.concatenate([
        np.linspace(c1[0], c2[0], points_per_side),
        np.linspace(c2[0], c3[0], points_per_side),
        np.linspace(c3[0], c4[0], points_per_side),
        np.linspace(c4[0], c1[0], points_per_side)
    ])
    y = np.concatenate([
        np.linspace(c1[1], c2[1], points_per_side),
        np.linspace(c2[1], c3[1], points_per_side),
        np.linspace(c3[1], c4[1], points_per_side),
        np.linspace(c4[1], c1[1], points_per_side)
    ])
    z = np.full_like(x, z_height)
    return x, y, z

def path_3d_spiral(num_points=300):
    """Spiral going UP in 3D space"""
    t = np.linspace(0, 4*np.pi, num_points)
    radius = 10.0
    x = 20.0 + radius * np.cos(t)
    y = radius * np.sin(t)
    z = np.linspace(5.0, 30.0, num_points) 
    return x, y, z

def path_letter_s_3d(num_points=200):
    """S-Curve drawn on a slanted surface"""
    t = np.linspace(0, 2*np.pi, num_points)
    x_flat = 25.0 + 5.0 * np.sin(t)
    y_flat = 5.0 * np.sin(2*t)
    x = x_flat
    y = y_flat
    z = 10.0 + (x_flat * 0.2) 
    return x, y, z

def path_heart_3d(num_points=250):
    """Heart drawn in the air at Z=15"""
    t = np.linspace(0, 2*np.pi, num_points)
    heart_x = 16 * np.sin(t)**3
    heart_y = 13*np.cos(t) - 5*np.cos(2*t) - 2*np.cos(3*t) - np.cos(4*t)
    scale = 0.4
    x = 25.0 + heart_x * scale
    y = 0.0 + heart_y * scale
    z = np.full_like(x, 15.0)
    return x, y, z

def path_drawing_cube(num_points=300):
    """Draws a 3D wireframe cube"""
    center_x, center_y, center_z = 25.0, 0.0, 12.0
    size = 10.0
    half = size / 2.0
    # Bottom Face
    b1 = (center_x - half, center_y - half, center_z - half)
    b2 = (center_x + half, center_y - half, center_z - half)
    b3 = (center_x + half, center_y + half, center_z - half)
    b4 = (center_x - half, center_y + half, center_z - half)
    # Top Face
    t1 = (center_x - half, center_y - half, center_z + half)
    t2 = (center_x + half, center_y - half, center_z + half)
    t3 = (center_x + half, center_y + half, center_z + half)
    t4 = (center_x - half, center_y + half, center_z + half)
    waypoints = [b1, b2, b3, b4, b1, t1, t2, t3, t4, t1]
    x, y, z = [], [], []
    points_per_leg = num_points // (len(waypoints) - 1)
    for i in range(len(waypoints)-1):
        p1, p2 = waypoints[i], waypoints[i+1]
        x.extend(np.linspace(p1[0], p2[0], points_per_leg))
        y.extend(np.linspace(p1[1], p2[1], points_per_leg))
        z.extend(np.linspace(p1[2], p2[2], points_per_leg))
    return np.array(x), np.array(y), np.array(z)

# ============================================================
# 🔧 3D TRAJECTORY GENERATOR (Smooth Motion)
# ============================================================
def generate_smooth_joint_trajectory_3d(path_x, path_y, path_z, cartesian_speed, dt):
    """Generates 3-Motor Trajectories with Corner Detection."""
    
    # 1. Analyze Geometry for Corners
    dx = np.diff(path_x)
    dy = np.diff(path_y)
    dz = np.diff(path_z)
    headings = np.vstack((dx, dy, dz)).T
    norms = np.linalg.norm(headings, axis=1)
    
    with np.errstate(divide='ignore', invalid='ignore'):
        headings_norm = headings / norms[:, np.newaxis]
    headings_norm[np.isnan(headings_norm)] = 0

    dot_products = np.sum(headings_norm[:-1] * headings_norm[1:], axis=1)
    dot_products = np.clip(dot_products, -1.0, 1.0)
    angles = np.arccos(dot_products)
    
    corner_threshold_rad = np.deg2rad(45.0)
    sharp_turn_indices = np.where(angles > corner_threshold_rad)[0] + 1
    segment_indices = [0] + list(sharp_turn_indices) + [len(path_x) - 1]

    # 2. Generate Profile per Segment
    all_time = []
    j_cmds = [[], [], []]
    j_vels = [[], [], []]
    
    current_time_offset = 0.0
    ACCEL_CARTESIAN = 50.0 
    last_joints = [0.0, 0.0, 0.0]

    for i in range(len(segment_indices) - 1):
        start_idx = segment_indices[i]
        end_idx = segment_indices[i+1] + 1
        
        sx = path_x[start_idx:end_idx]
        sy = path_y[start_idx:end_idx]
        sz = path_z[start_idx:end_idx]
        
        sdx = np.diff(sx); sdy = np.diff(sy); sdz = np.diff(sz)
        sdists = np.sqrt(sdx**2 + sdy**2 + sdz**2)
        scum_dist = np.concatenate(([0], np.cumsum(sdists)))
        total_dist = scum_dist[-1]
        
        if total_dist < 0.001: continue

        t_accel = cartesian_speed / ACCEL_CARTESIAN
        d_accel = 0.5 * ACCEL_CARTESIAN * t_accel**2
        
        if total_dist < 2 * d_accel:
            d_accel = total_dist / 2.0
            t_accel = np.sqrt(2 * d_accel / ACCEL_CARTESIAN)
            t_cruise = 0.0
        else:
            d_cruise = total_dist - 2 * d_accel
            t_cruise = d_cruise / cartesian_speed
            
        total_seg_time = t_accel * 2 + t_cruise
        num_steps = int(np.ceil(total_seg_time / dt))
        seg_times = np.linspace(0, total_seg_time, num_steps)
        
        dist_at_t = np.zeros_like(seg_times)
        for k, t in enumerate(seg_times):
            if t <= t_accel:
                dist_at_t[k] = 0.5 * ACCEL_CARTESIAN * t**2
            elif t <= (t_accel + t_cruise):
                dist_at_t[k] = d_accel + cartesian_speed * (t - t_accel)
            else:
                t_d = t - t_accel - t_cruise
                dist_at_t[k] = (d_accel + t_cruise*cartesian_speed) + (cartesian_speed*t_d) - (0.5*ACCEL_CARTESIAN*t_d**2)
        
        dist_at_t = np.clip(dist_at_t, 0, total_dist)
        
        ix = np.interp(dist_at_t, scum_dist, sx)
        iy = np.interp(dist_at_t, scum_dist, sy)
        iz = np.interp(dist_at_t, scum_dist, sz)
        
        seg_joints = [[], [], []]
        for x, y, z in zip(ix, iy, iz):
            angs = inverse_kinematics(x, y, z)
            if angs[0] is None:
                for m in range(3): seg_joints[m].append(last_joints[m])
            else:
                deg_angs = [np.degrees(a) for a in angs]
                for m in range(3): seg_joints[m].append(deg_angs[m])
                last_joints = deg_angs
                
        for m in range(3):
            pos_arr = np.array(seg_joints[m])
            vel_arr = np.gradient(pos_arr, dt)
            j_cmds[m].extend(pos_arr)
            j_vels[m].extend(vel_arr)
            
        all_time.extend(seg_times + current_time_offset)
        current_time_offset += total_seg_time

    return (np.array(all_time), 
            np.array(j_cmds[0]), np.array(j_vels[0]), 
            np.array(j_cmds[1]), np.array(j_vels[1]), 
            np.array(j_cmds[2]), np.array(j_vels[2]))

def enforce_max_reach(x_arr, y_arr, z_arr):
    """Clamps points outside reach."""
    z_shifted = z_arr - L_BASE
    dist = np.sqrt(x_arr**2 + y_arr**2 + z_shifted**2)
    mask = dist > MAX_REACH
    if np.any(mask):
        print(f"⚠️  WARNING: {np.sum(mask)} points exceeded max reach. Clamping.")
        scale = MAX_REACH / dist[mask]
        x_arr[mask] *= scale
        y_arr[mask] *= scale
        z_shifted[mask] *= scale
        z_arr[mask] = z_shifted[mask] + L_BASE
    return x_arr, y_arr, z_arr

# ============================================================
# ▶️ SIMULATION RUNNER (DYNAMICS ENABLED)
# ============================================================

def run_digital_twin_simulation(path_function, cartesian_speed=15.0, path_resolution=200):
    
    global last_base_angle_rad
    last_base_angle_rad = 0.0

    print(f"🎨 3D Path: {path_function.__name__}")
    print(f"🏃 Speed: {cartesian_speed} cm/s")
    
    # 1. Initialize Motors with RESEARCH GRADE specs
    # Base: NEMA 23 (3.0Nm) + 10:1 Gearbox
    motor_base = MockMotor("Base", gear_ratio=10.0, max_torque_nm=3.0)
    
    # Shoulder: NEMA 23 (3.0Nm) + 20:1 Gearbox
    motor_shoulder = MockMotor("Shoulder", gear_ratio=20.0, max_torque_nm=3.0)
    
    # Elbow: NEMA 17 (0.5Nm) + 25:1 Gearbox
    motor_elbow = MockMotor("Elbow", gear_ratio=25.0, max_torque_nm=0.5)
    
    motors = [motor_base, motor_shoulder, motor_elbow]
    
    # Set Home Position
    home_angs = inverse_kinematics(*HOME_POSITION_CARTESIAN)
    if home_angs[0] is None:
        print("❌ Home position unreachable!")
        return

    for i, m in enumerate(motors):
        m.actual_pos = np.degrees(home_angs[i])
        
    print(f"🏠 Home: {HOME_POSITION_CARTESIAN} cm")
    
    # 2. Generate Path
    path_x, path_y, path_z = path_function(num_points=path_resolution)
    
    # 3. Add Approach Path
    start_xyz = (path_x[0], path_y[0], path_z[0])
    num_approach = 50
    full_x = np.concatenate([np.linspace(HOME_POSITION_CARTESIAN[0], start_xyz[0], num_approach), path_x])
    full_y = np.concatenate([np.linspace(HOME_POSITION_CARTESIAN[1], start_xyz[1], num_approach), path_y])
    full_z = np.concatenate([np.linspace(HOME_POSITION_CARTESIAN[2], start_xyz[2], num_approach), path_z])
    
    full_x, full_y, full_z = enforce_max_reach(full_x, full_y, full_z)

    # 4. Generate Smooth Trajectory
    (times, 
     j0_p, j0_v, 
     j1_p, j1_v, 
     j2_p, j2_v) = generate_smooth_joint_trajectory_3d(full_x, full_y, full_z, cartesian_speed, DT)
    
    print(f"⏱️  Duration: {times[-1]:.2f}s ({len(times)} steps)")
    
    # 5. Execute Loop with DYNAMICS
    log_data = []
    
    for i in range(len(times)):
        targets = [j0_p[i], j1_p[i], j2_p[i]]
        vel_cmds = [j0_v[i], j1_v[i], j2_v[i]]
        
        # --- A. Calculate Gravity Load ---
        # We need the CURRENT motor positions (radians) to calculate the leverage
        rad_sh = np.radians(motor_shoulder.actual_pos)
        rad_el = np.radians(motor_elbow.actual_pos)
        
        torque_s, torque_e = calculate_gravity_torques(rad_sh, rad_el)
        
        # --- B. Update Motors with Load ---
        # Base motor rotates around vertical axis -> Gravity torque is ~0 (just friction/inertia)
        pos_base = motor_base.update(targets[0], vel_cmds[0], DT, external_load_torque=0.0)
        
        # Shoulder and Elbow fight gravity
        pos_sh = motor_shoulder.update(targets[1], vel_cmds[1], DT, external_load_torque=torque_s)
        pos_el = motor_elbow.update(targets[2], vel_cmds[2], DT, external_load_torque=torque_e)
        
        real_degs = [pos_base, pos_sh, pos_el]

        # --- C. Failure Check ---
        if motor_shoulder.failed or motor_elbow.failed:
            print(f"💥 CRITICAL HARDWARE FAILURE at t={times[i]:.2f}s")
            print(f"   Shoulder Status: {'FAILED' if motor_shoulder.failed else 'OK'} ({motor_shoulder.fail_reason})")
            print(f"   Elbow Status:    {'FAILED' if motor_elbow.failed else 'OK'} ({motor_elbow.fail_reason})")
            break
            
        # --- D. Logging ---
        real_rads = [np.radians(d) for d in real_degs]
        rx, ry, rz = forward_kinematics(*real_rads)
        tx, ty, tz = forward_kinematics(*[np.radians(t) for t in targets])
        error = np.sqrt((tx-rx)**2 + (ty-ry)**2 + (tz-rz)**2)
        
        log_data.append({
            "timestamp_ms": int(times[i] * 1000),
            "target_x": round(tx, 3), "target_y": round(ty, 3), "target_z": round(tz, 3),
            "real_x": round(rx, 3), "real_y": round(ry, 3), "real_z": round(rz, 3),
            "error": round(error, 4),
            "base_deg": round(real_degs[0], 2),
            "shoulder_deg": round(real_degs[1], 2),
            "elbow_deg": round(real_degs[2], 2),
            "torque_shoulder": round(torque_s, 2),
            "torque_elbow": round(torque_e, 2),
            "limit_shoulder": round(motor_shoulder.max_torque_output, 2),
            "limit_elbow": round(motor_elbow.max_torque_output, 2)
        })
        
    # Save Log
    filename = os.path.join(RUN_LOG_DIR, "arm_dynamics_log.csv")
    pd.DataFrame(log_data).to_csv(filename, index=False)
    print(f"✅ Data saved to: {filename}")
    
    # Quick Stats
    if log_data:
        errs = [d['error'] for d in log_data]
        torques_s = [d['torque_shoulder'] for d in log_data]
        torques_e = [d['torque_elbow'] for d in log_data]
        print(f"   Max Error: {max(errs):.4f} cm")
        print(f"   Max Shoulder Torque: {max(torques_s):.2f} Nm (Limit: {motor_shoulder.max_torque_output:.2f})")
        print(f"   Max Elbow Torque:    {max(torques_e):.2f} Nm (Limit: {motor_elbow.max_torque_output:.2f})")

# ============================================================
# 🚀 MAIN EXECUTION (Menu System)
# ============================================================
if __name__ == "__main__":
    
    # 1. Auto-discover "path_" functions
    current_module = inspect.currentframe().f_globals
    path_functions = [
        (name, func) for name, func in current_module.items()
        if callable(func) and name.startswith('path_') and inspect.isfunction(func)
    ]
    path_functions.sort(key=lambda x: x[0])
    
    # 2. Config for paths
    speed_config = {
        'path_pick_and_place': (15.0, 300),
        'path_drawing_circle': (15.0, 200),
        'path_drawing_square': (15.0, 200),
        'path_3d_spiral':      (12.0, 300),
        'path_drawing_cube':   (12.0, 350),
        'path_360_spin':       (20.0, 400),
        'path_letter_s_3d':    (10.0, 250),
        'path_heart_3d':       (10.0, 300)
    }

    # 3. Display Menu
    print("\n" + "="*70)
    print("🤖 3D ROBOT ARM SIMULATION (RESEARCH PHYSICS ENGINE)")
    print("="*70)
    
    for i, (name, func) in enumerate(path_functions, 1):
        display = name.replace('path_', '').replace('_', ' ').title()
        speed, res = speed_config.get(name, (10.0, 200))
        doc = (func.__doc__ or "").split('\n')[0]
        print(f"  {i}. {display:<20} | {doc}")
    print("="*70)
    
    # 4. Input Loop
    while True:
        try:
            choice = int(input(f"\nSelect Path (1-{len(path_functions)}): ")) - 1
            if 0 <= choice < len(path_functions):
                sel_name, sel_func = path_functions[choice]
                speed, res = speed_config.get(sel_name, (10.0, 200))
                run_digital_twin_simulation(sel_func, speed, res)
                break
            else:
                print("❌ Invalid number.")
        except ValueError:
            print("❌ Enter a number.")