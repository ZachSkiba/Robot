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
print(f"\n📂 Logging Digital Twin (Pro Specs) to: {RUN_LOG_DIR}\n")

# ============================================================
# ⚙️ HARDWARE CONFIG (TEENSY 4.1 + NEMA 17 PRO SPECS)
# ============================================================
L1 = 15.0  # cm
L2 = 15.0  # cm

# TEENSY 4.1 SPECS
# We run the PID loop at 1kHz (1000 times per second)
HZ = 1000
DT = 1.0 / HZ 

# NEMA 17 "REALISTIC LOADED" SPECS
# Unloaded max is ~2000 deg/s. 
# Loaded arm max is safer at ~1080 deg/s (3 rev/sec).
MAX_SPEED_DEG = 1080.0  
MAX_ACCEL_DEG = 4000.0 # High torque accel

# ============================================================
# 🧠 KINEMATICS ENGINE
# ============================================================
def forward_kinematics(theta1, theta2):
    x = L1 * np.cos(theta1) + L2 * np.cos(theta1 + theta2)
    y = L1 * np.sin(theta1) + L2 * np.sin(theta1 + theta2)
    return x, y

def inverse_kinematics(x, y):
    dist = np.sqrt(x**2 + y**2)
    if dist > (L1 + L2) or dist == 0: return None, None 
    cos_theta2 = (x**2 + y**2 - L1**2 - L2**2) / (2 * L1 * L2)
    cos_theta2 = np.clip(cos_theta2, -1.0, 1.0)
    theta2 = np.arccos(cos_theta2) 
    theta1 = np.arctan2(y, x) - np.arctan2(L2 * np.sin(theta2), L1 + L2 * np.cos(theta2))
    return theta1, theta2

def generate_line_trajectory(start_xy, end_xy, speed, dt):
    start_pos = np.array(start_xy)
    end_pos = np.array(end_xy)
    dist = np.linalg.norm(end_pos - start_pos)
    
    duration = dist / speed
    steps = int(duration / dt)
    
    time_points = np.linspace(0, duration, steps)
    path_x = np.linspace(start_pos[0], end_pos[0], steps)
    path_y = np.linspace(start_pos[1], end_pos[1], steps)
    
    return time_points, path_x, path_y, duration

# ============================================================
# ▶️ SIMULATION RUNNER
# ============================================================
def run_digital_twin_simulation():
    # 1. Init Virtual Hardware (Pro Specs)
    motor1 = MockMotor(max_velocity=MAX_SPEED_DEG, max_accel=MAX_ACCEL_DEG)
    motor2 = MockMotor(max_velocity=MAX_SPEED_DEG, max_accel=MAX_ACCEL_DEG)

    # 2. Define Mission (Faster!)
    start_pos = (5.0, 0.0)
    end_pos   = (28.0, 0.0)
    move_speed = 20.0 # cm/s
    
    times, target_xs, target_ys, total_time = generate_line_trajectory(start_pos, end_pos, move_speed, DT)
    
    print(f"⏱️  Trajectory Calculated: {total_time:.2f} seconds ({len(times)} frames @ {HZ}Hz)")
    print(f"🦾 Starting High-Performance Digital Twin...")

    log_data = []
    
    prev_t1, prev_t2 = inverse_kinematics(start_pos[0], start_pos[1])
    motor1.actual_pos = np.degrees(prev_t1)
    motor2.actual_pos = np.degrees(prev_t2)

    command_id = 1 

    for i in range(len(times)):
        t_x, t_y = target_xs[i], target_ys[i]
        
        target_rad1, target_rad2 = inverse_kinematics(t_x, t_y)
        if target_rad1 is None: continue

        cmd_deg1 = np.degrees(target_rad1)
        cmd_deg2 = np.degrees(target_rad2)
        
        vel_cmd1 = (cmd_deg1 - np.degrees(prev_t1)) / DT
        vel_cmd2 = (cmd_deg2 - np.degrees(prev_t2)) / DT
        
        actual_deg1 = motor1.update(cmd_deg1, vel_cmd1, DT)
        actual_deg2 = motor2.update(cmd_deg2, vel_cmd2, DT)

        actual_rad1 = np.radians(actual_deg1)
        actual_rad2 = np.radians(actual_deg2)
        real_x, real_y = forward_kinematics(actual_rad1, actual_rad2)
        
        # Log at 1000 Hz (This creates big files, just like real life!)
        log_data.append({
            "timestamp_ms": int(times[i] * 1000),
            "command_id": command_id,
            "target_x": round(t_x, 3), 
            "target_y": round(t_y, 3),
            "real_x": round(real_x, 3), 
            "real_y": round(real_y, 3),
            "error": round(np.sqrt((t_x-real_x)**2 + (t_y-real_y)**2), 3),
            "motor1_pos": round(actual_deg1, 2), 
            "motor2_pos": round(actual_deg2, 2),
            "velocity": round(vel_cmd1, 2),
            "pwm_effort": 127,
            "hz": HZ # Log the Hz so Dashboard knows
        })
        
        prev_t1, prev_t2 = target_rad1, target_rad2

    filename = os.path.join(RUN_LOG_DIR, "arm_2link_log.csv")
    df = pd.DataFrame(log_data)
    df.to_csv(filename, index=False)
    print(f"✅ Pro-Spec Data saved to {filename}")

if __name__ == "__main__":
    run_digital_twin_simulation()