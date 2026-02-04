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
# ⚙️ HARDWARE CONFIG (HEAVY LIFT 3D PRINTED EDITION)
# ============================================================
# Robot Geometry
L_BASE = 10.0   # cm
L1 = 20.0       # cm (Shoulder to Elbow)
L2 = 20.0       # cm (Elbow to Wrist)
MAX_REACH = L1 + L2 - 0.1

# Simulation Timing
HZ = 1000
DT = 1.0 / HZ 

# 🏗️ DYNAMICS CONSTANTS (MASS & GRAVITY)
G = 9.81  # m/s^2

# Link 1 (Shoulder)
# 3D printed walls are often heavier than thin aluminum tubes due to infill.
M_LINK1 = 0.5          # kg (3D Printed Structure + Belt/Pulleys)

# M_ELBOW_MOTOR is set to 0.0 because you moved it to the shoulder pivot.
# It no longer acts as a weight at the end of Link 1.
M_ELBOW_MOTOR = 0.0    # kg (Remote Actuation - Motor sits on Base)

# Link 2 (Elbow)
M_LINK2 = 0.4          # kg (3D Printed Tube/Structure)

# --- THE TIP MASS CALCULATION ---
# 1. Payload:          2.0 kg
# 2. Future Nema 17:   0.4 kg (Wrist Pitch)
# 3. Future Nema 11:   0.2 kg (Wrist Roll)
# 4. Future Nema 11:   0.2 kg (Gripper)
# 5. Plastic Housing:  0.2 kg
# -----------------------------
# TOTAL TIP MASS:      3.0 kg
M_WRIST_ASSEMBLY = 3.0 # kg (Huge weight for a Nema 17!)

# Default Home
HOME_POSITION_CARTESIAN = (20.0, 0.0, 20.0) 

SENSOR_BIT_DEPTH = 14  # High precision sensors

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
    """
    Computes (base, shoulder, elbow) angles.
    Includes 'Elbow Up' logic to prevent floor collisions.
    """
    global last_base_angle_rad

    # --- 1. Base Angle (Theta 0) ---
    current_base = np.arctan2(y, x)
    diff = current_base - last_base_angle_rad
    while diff > np.pi: diff -= 2 * np.pi
    while diff < -np.pi: diff += 2 * np.pi
    theta_base = last_base_angle_rad + diff
    last_base_angle_rad = theta_base 

    # --- 2. Planar Problem (r, z) ---
    r_target = np.sqrt(x**2 + y**2)
    z_target = z - L_BASE # Height relative to shoulder pivot

    # Check reach
    dist = np.sqrt(r_target**2 + z_target**2)
    if dist > (L1 + L2) or dist == 0: 
        return None, None, None 

    # --- 3. Solve Planar IK (Select Best Configuration) ---
    # Law of Cosines for the Elbow Angle magnitude
    cos_theta2 = (r_target**2 + z_target**2 - L1**2 - L2**2) / (2 * L1 * L2)
    cos_theta2 = np.clip(cos_theta2, -1.0, 1.0)
    
    # We have TWO possible elbow angles: +acos and -acos
    # One creates an "Elbow Down" pose, one is "Elbow Up"
    candidates = [np.arccos(cos_theta2), -np.arccos(cos_theta2)]
    
    best_solution = None
    max_elbow_height = -999.0

    for theta_el_cand in candidates:
        # Calculate matching shoulder angle for this elbow angle
        k1 = L1 + L2 * np.cos(theta_el_cand)
        k2 = L2 * np.sin(theta_el_cand)
        theta_sh_cand = np.arctan2(z_target, r_target) - np.arctan2(k2, k1)
        
        # Calculate where the Elbow joint is physically located in Z space
        # Z_elbow = Base_Height + L1 * sin(shoulder_angle)
        elbow_z_height = L_BASE + L1 * np.sin(theta_sh_cand)

        # We prefer the solution with the HIGHEST elbow position (Elbow Up)
        if elbow_z_height > max_elbow_height:
            max_elbow_height = elbow_z_height
            best_solution = (theta_sh_cand, theta_el_cand)

    # Safety Check: If even the "highest" solution puts the elbow underground
    if max_elbow_height < 0.0:
        # In a real robot, we would throw an error or clamp. 
        # Here we return None to indicate "Unsafe Path"
        return None, None, None

    theta_shoulder, theta_elbow = best_solution
    return theta_base, theta_shoulder, theta_elbow

def calculate_gravity_torques(theta_shoulder, theta_elbow):
    """
    Calculates the torque (Nm) required to hold the arm against gravity.
    UPDATED: Elbow motor is now at the shoulder pivot (Remote Actuation).
    """
    # Lengths in Meters
    l1_m = L1 / 100.0
    l2_m = L2 / 100.0
    
    # Global angle of forearm relative to horizon
    global_angle_elbow = theta_shoulder + theta_elbow
    
    # --- 1. Forces on ELBOW Joint (Unchanged) ---
    # The belt transfers torque, so the load calculation at the elbow joint is the same.
    torque_elbow = (
        (M_LINK2 * G * (l2_m/2) * np.cos(global_angle_elbow)) + 
        (M_WRIST_ASSEMBLY * G * l2_m * np.cos(global_angle_elbow))
    )
    
    # --- 2. Forces on SHOULDER Joint (MAJOR CHANGE) ---
    # PREVIOUSLY: We added (M_ELBOW_MOTOR * G * l1_m...)
    # NOW: The motor is at the pivot (distance = 0), so it adds NO torque load.
    
    # Torque from Link 1 Mass (The aluminum tube itself)
    t_link1 = M_LINK1 * G * (l1_m/2) * np.cos(theta_shoulder)
    
    # Torque from Link 2 + Wrist acting on Shoulder lever arm
    dist_link2_com = l1_m * np.cos(theta_shoulder) + (l2_m/2) * np.cos(global_angle_elbow)
    dist_wrist_com = l1_m * np.cos(theta_shoulder) + l2_m * np.cos(global_angle_elbow)
    
    t_link2_on_shoulder = M_LINK2 * G * dist_link2_com
    t_wrist_on_shoulder = M_WRIST_ASSEMBLY * G * dist_wrist_com
    
    # REMOVED: t_elbow_motor (It is now 0 torque impact)
    torque_shoulder = t_link1 + t_link2_on_shoulder + t_wrist_on_shoulder
    
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

def path_random_micro_movements(num_points=500):
    """Tiny 2mm movements + jitter to test resolution limits."""
    # Center position
    cx, cy, cz = 25.0, 0.0, 15.0
    
    # 1. Create a very slow, tiny spiral (Radius = 0.2 cm)
    # This is small enough that 12-bit sensors will struggle to track it smoothly
    t = np.linspace(0, 6*np.pi, num_points)
    radius = 0.2 
    
    base_x = cx + radius * np.cos(t)
    base_y = cy + radius * np.sin(t)
    base_z = cz + np.linspace(0, 0.5, num_points) # Rise 0.5cm

    # 2. Add random "micro-jitter" (0.02 cm)
    # This tests if the sensor can detect sub-millimeter vibration
    np.random.seed(42) # Fixed seed so 12-bit vs 14-bit runs are identical
    noise = 0.02
    
    x = base_x + np.random.uniform(-noise, noise, num_points)
    y = base_y + np.random.uniform(-noise, noise, num_points)
    z = base_z + np.random.uniform(-noise, noise, num_points)
    
    return x, y, z

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

def enforce_constraints(x_arr, y_arr, z_arr):
    """
    1. Clamps points outside max reach.
    2. Clamps points below the ground (Z < 0).
    """
    # --- Floor Constraint ---
    # Ensure the end-effector never touches the table
    # We add a 0.5cm safety buffer
    min_z = 0.5 
    mask_floor = z_arr < min_z
    if np.any(mask_floor):
        print(f"⚠️  WARNING: {np.sum(mask_floor)} points were underground. Clamping to Z={min_z}.")
        z_arr[mask_floor] = min_z

    # --- Reach Constraint ---
    z_shifted = z_arr - L_BASE
    dist = np.sqrt(x_arr**2 + y_arr**2 + z_shifted**2)
    mask_reach = dist > MAX_REACH
    
    if np.any(mask_reach):
        print(f"⚠️  WARNING: {np.sum(mask_reach)} points exceeded max reach. Clamping.")
        scale = MAX_REACH / dist[mask_reach]
        x_arr[mask_reach] *= scale
        y_arr[mask_reach] *= scale
        z_shifted[mask_reach] *= scale
        z_arr[mask_reach] = z_shifted[mask_reach] + L_BASE
        
    return x_arr, y_arr, z_arr

# ============================================================
# CALCULATE STEPPING OF ENCODER
# ============================================================

def quantize_angle(angle_deg, bit_depth):
    """Simulates the 'stepping' of a digital encoder."""
    steps = 2 ** bit_depth
    # Convert angle to a discrete "step" (0 to 4095 for 12-bit)
    step_count = round((angle_deg / 360.0) * steps)
    # Convert back to degrees
    return (step_count / steps) * 360.0


def apply_structural_deflection(real_x, real_y, real_z, torque_shoulder, torque_elbow):
    """
    Simulates the physical bending of the aluminum tubes under load.
    The heavier the load (torque), the more the arm droops.
    """
    # STIFFNESS CONSTANT: How 'floppy' is your arm?
    # 0.02 means 10Nm of torque causes 2mm of sag.
    # Cheap 3D printed arms might be 0.1 (very floppy).
    MATERIAL_STIFFNESS_K = 0.03 
    
    # Calculate total load acting to bend the arm down
    total_load_torque = abs(torque_shoulder) + abs(torque_elbow)
    
    # Hooke's Law approximation for a cantilever beam
    # The sag is always in the negative Z direction (gravity)
    sag_z = -(total_load_torque * MATERIAL_STIFFNESS_K)
    
    # The sag also slightly reduces the reach (X/Y) as it curls down, 
    # but Z is the dominant error.
    return real_x, real_y, real_z + sag_z

# ============================================================
# ▶️ SIMULATION RUNNER (DYNAMICS ENABLED)
# ============================================================

def run_digital_twin_simulation(path_function, cartesian_speed=15.0, path_resolution=200):
    
    global last_base_angle_rad
    last_base_angle_rad = 0.0

    print(f"🎨 3D Path: {path_function.__name__}")
    
    # ==========================================
    # 🔧 UPDATED MOTOR CONFIGURATION
    # ==========================================
    
    # 1. BASE: Nema 17 (Turntable)
    # 5:1 is fine here for rotation, as it doesn't fight gravity directly.
    motor_base = MockMotor("Base (Nema 17)", gear_ratio=5.0, max_torque_nm=0.45)
    
    # 2. SHOULDER: Nema 23 (The Heavy Lifter)
    # With 3kg at the tip, the shoulder sees huge leverage. 
    # Keep this at 20:1 (or even 30:1 if you have a high-ratio gearbox).
    motor_shoulder = MockMotor("Shoulder (Nema 23)", gear_ratio=20.0, max_torque_nm=1.2)
    
    # 3. ELBOW : Upgrade Elbow to Nema 23 (Same as Shoulder)
    motor_elbow = MockMotor("Elbow (Nema 23)", gear_ratio=20.0, max_torque_nm=1.2)
    
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
    
    full_x, full_y, full_z = enforce_constraints(full_x, full_y, full_z)

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
        # 1. Calculate the "Physics" (Infinite resolution float values)
        pos_base_phys = motor_base.update(targets[0], vel_cmds[0], DT, external_load_torque=0.0)
        pos_sh_phys   = motor_shoulder.update(targets[1], vel_cmds[1], DT, external_load_torque=torque_s)
        pos_el_phys   = motor_elbow.update(targets[2], vel_cmds[2], DT, external_load_torque=torque_e)
        
        # 2. Simulate the Sensor (Crunch it down to 12-bit or 14-bit)
        # This is what your code will actually "see" and log
        pos_base = quantize_angle(pos_base_phys, SENSOR_BIT_DEPTH)
        pos_sh   = quantize_angle(pos_sh_phys,   SENSOR_BIT_DEPTH)
        pos_el   = quantize_angle(pos_el_phys,   SENSOR_BIT_DEPTH)

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
        rx, ry, rz = apply_structural_deflection(rx, ry, rz, torque_s, torque_e)
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
            "torque_shoulder": round(motor_shoulder.last_torque_usage, 2),
            "torque_elbow": round(motor_elbow.last_torque_usage, 2),
            "limit_shoulder": round(motor_shoulder.max_torque_output, 2),
            "limit_elbow": round(motor_elbow.max_torque_output, 2),
            "torque_base": round(motor_base.last_torque_usage, 2),
            "limit_base": round(motor_base.max_torque_output, 2),   
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
        'path_heart_3d':       (10.0, 300),
        'path_random_micro_movements': (2.0, 500)
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