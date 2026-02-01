import pandas as pd
import numpy as np
import os
import re

# ============================================================
# 📂 PATH SETUP
# ============================================================

script_dir = os.path.dirname(os.path.abspath(__file__))
BASE_LOG_DIR = os.path.normpath(os.path.join(script_dir, "..", "..", "logs"))

existing_runs = [
    f.name for f in os.scandir(BASE_LOG_DIR) if f.is_dir() and f.name.startswith("run")
]

if existing_runs:
    run_numbers = [int(re.search(r"run(\d+)", r).group(1)) for r in existing_runs]
    next_run = max(run_numbers) + 1
else:
    next_run = 1

RUN_LOG_DIR = os.path.join(BASE_LOG_DIR, f"run{next_run}")
os.makedirs(RUN_LOG_DIR, exist_ok=True)
print(f"\n📂 Logging simulation run to folder: {RUN_LOG_DIR}\n")

# ============================================================
# ⚙️ MOTOR SPECS
# ============================================================

MOTOR_STEP_ANGLE = 1.8
MICROSTEPS = 64
EFFECTIVE_STEP = MOTOR_STEP_ANGLE / MICROSTEPS  # ~0.028125 deg/step
MAX_ACCEL = 1000.0      # deg/s^2
MAX_VELOCITY = 1200.0    # deg/s
ENCODER_RES = 0.088
ENCODER_NOISE = 0.05
SPEED_CAP = 0.8          # % of MAX_VELOCITY

# ============================================================
# 🔧 MOTOR MODEL
# ============================================================

class MockMotor:
    def __init__(self, max_safe_vel=MAX_VELOCITY*SPEED_CAP):
        self.actual_pos = 0.0
        self.current_velocity = 0.0
        self.max_safe_vel = max_safe_vel

    def update(self, target_pos, target_vel, dt):
        # Distance to target
        dist_to_go = target_pos - self.actual_pos

        # Limit desired velocity by remaining distance
        desired_vel = np.sign(dist_to_go) * min(abs(target_vel), abs(dist_to_go/dt))

        # Limit acceleration
        vel_diff = desired_vel - self.current_velocity
        max_vel_change = MAX_ACCEL * dt
        if abs(vel_diff) > max_vel_change:
            self.current_velocity += max_vel_change * np.sign(vel_diff)
        else:
            self.current_velocity = desired_vel

        # Clip to motor's max safe velocity
        self.current_velocity = np.clip(self.current_velocity, -self.max_safe_vel, self.max_safe_vel)

        # Update position
        self.actual_pos += self.current_velocity * dt

        # Encoder quantization + noise
        physical_pos = round(self.actual_pos / EFFECTIVE_STEP) * EFFECTIVE_STEP
        sensor_reading = round(physical_pos / ENCODER_RES) * ENCODER_RES
        sensor_reading += np.random.normal(0, ENCODER_NOISE)

        return sensor_reading

# ============================================================
# ▶️ TRAPEZOIDAL PROFILE GENERATOR
# ============================================================

def generate_trapezoidal_profile(target_pos, commanded_speed, dt):
    """Generates a trapezoidal velocity profile to reach target_pos."""
    max_vel = commanded_speed
    accel_time = max_vel / MAX_ACCEL               # time to accelerate to commanded speed
    accel_dist = 0.5 * MAX_ACCEL * accel_time**2  # distance covered during acceleration

    if accel_dist * 2 > target_pos:  # Triangular profile if distance too short
        accel_time = np.sqrt(target_pos / MAX_ACCEL)
        cruise_time = 0
        cruise_dist = 0
    else:
        cruise_dist = target_pos - 2 * accel_dist
        cruise_time = cruise_dist / max_vel

    total_time = 2 * accel_time + cruise_time

    time_points = np.arange(0, total_time+dt, dt)
    vel_profile = np.zeros_like(time_points)
    pos_profile = np.zeros_like(time_points)

    for i, t in enumerate(time_points):
        if t < accel_time:
            vel = MAX_ACCEL * t
            pos = 0.5 * MAX_ACCEL * t**2
        elif t < accel_time + cruise_time:
            vel = max_vel
            pos = accel_dist + max_vel * (t - accel_time)
        else:
            t_dec = t - (accel_time + cruise_time)
            vel = max_vel - MAX_ACCEL * t_dec
            pos = accel_dist + cruise_dist + max_vel * t_dec - 0.5 * MAX_ACCEL * t_dec**2
        vel_profile[i] = vel
        pos_profile[i] = pos

    return time_points, pos_profile, vel_profile

# ============================================================
# ▶️ SIMULATION RUNNER
# ============================================================

def get_next_filename():
    files = os.listdir(RUN_LOG_DIR)
    numbers = [int(re.search(r"(\d+)", f).group(1)) for f in files if re.search(r"motor_log_(\d+)", f)]
    next_num = 1 if not numbers else max(numbers) + 1
    return os.path.join(RUN_LOG_DIR, f"motor_log_{next_num:03d}.csv")

def run_simulation():
    SPEEDS = [45, 60, 75, 90, 180, 270, 360, 720]  # commanded speeds
    HZ = 500
    dt = 1.0 / HZ
    TARGET_POS = 720
    HOLD_TIME = 2.0  # seconds to hold at 360 deg

    for speed in SPEEDS:
        motor = MockMotor(max_safe_vel=MAX_VELOCITY*SPEED_CAP)
        time_points, target_positions, target_velocities = generate_trapezoidal_profile(TARGET_POS, speed, dt)

        # Extend to hold at 360 deg
        hold_steps = int(HOLD_TIME / dt)
        time_points = np.concatenate([time_points, time_points[-1] + np.arange(1, hold_steps+1)*dt])
        target_positions = np.concatenate([target_positions, np.full(hold_steps, TARGET_POS)])
        target_velocities = np.concatenate([target_velocities, np.zeros(hold_steps)])

        data_log = []

        for t, target_pos, target_vel in zip(time_points, target_positions, target_velocities):
            actual = motor.update(target_pos, target_vel, dt)
            data_log.append({
                "timestamp_ms": int(t*1000),
                "target_pos": round(target_pos, 3),
                "actual_pos": round(actual, 3),
                "error": round(target_pos-actual, 3),
                "velocity_cmd": speed,
                "hz": HZ
            })

        filename = get_next_filename()
        pd.DataFrame(data_log).to_csv(filename, index=False)
        print(f"✅ Data saved to: {filename}, time-to-360°={time_points[len(time_points)-hold_steps-1]:.3f} s (plus {HOLD_TIME}s hold)")


if __name__ == "__main__":
    run_simulation()