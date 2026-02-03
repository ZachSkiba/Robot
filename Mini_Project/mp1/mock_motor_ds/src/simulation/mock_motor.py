import pandas as pd
import numpy as np
import os
import re

# ============================================================
# ⚙️ MOTOR SPECS (Global Constants - Safe to Import)
# ============================================================

# Step / Resolution
MOTOR_STEP_ANGLE = 1.8
MICROSTEPS = 32         # Updated to 32 (Standard for smooth motion with DM556T)
EFFECTIVE_STEP = MOTOR_STEP_ANGLE / MICROSTEPS  # 0.05625 deg/step

# NEMA 23 / 17 Physical Limits (At the Motor Shaft, before Gears)
MOTOR_MAX_VELOCITY_SHAFT = 3600.0  # deg/s (600 RPM - typical torque drop-off point)
MOTOR_MAX_ACCEL_SHAFT = 6000.0     # deg/s^2

# Encoder Simulation
ENCODER_RES = 0.088
ENCODER_NOISE = 0.05

# ============================================================
# 🔧 MOTOR MODEL (CLASS)
# ============================================================

class MockMotor:
    def __init__(self, name="Generic", gear_ratio=1.0, max_torque_nm=3.0, 
                 max_velocity=None, max_accel=None):
        """
        Universal MockMotor.
        
        Args:
            name (str): ID for logging (e.g. "Shoulder")
            gear_ratio (float): Input rotations per 1 output rotation (e.g. 20.0)
            max_torque_nm (float): Holding torque of the RAW MOTOR (not gearbox output)
            max_velocity (float): Optional override for legacy tests
            max_accel (float): Optional override for legacy tests
        """
        self.name = name
        self.gear_ratio = gear_ratio
        
        # Physics Limits (Calculated at the JOINT output)
        # If legacy values are provided, use them; otherwise calculate from Gear Ratio
        if max_velocity:
            self.max_velocity = max_velocity
        else:
            self.max_velocity = MOTOR_MAX_VELOCITY_SHAFT / gear_ratio

        if max_accel:
            self.max_accel = max_accel
        else:
            self.max_accel = MOTOR_MAX_ACCEL_SHAFT / gear_ratio

        # Torque: Output = Motor * Ratio * Efficiency (approx 0.85 for planetary)
        self.max_torque_output = max_torque_nm * gear_ratio * 0.85

        # State
        self.actual_pos = 0.0
        self.current_velocity = 0.0
        self.failed = False
        self.fail_reason = ""

    def update(self, target_pos, target_velocity, dt, external_load_torque=0.0):
        """
        Updates motor physics state.
        
        Args:
            target_pos (float): Where we want to be
            target_velocity (float): Feed-forward velocity (from profile)
            dt (float): Time step in seconds
            external_load_torque (float): Gravity/Dynamic load in Nm (New Feature)
        
        Returns:
            float: Simulated Encoder Reading (with noise)
        """
        # 1. Failure Check (The "Gravity Killer")
        if self.failed:
            return self.actual_pos

        if abs(external_load_torque) > self.max_torque_output:
            self.failed = True
            self.fail_reason = f"STALL: Load {external_load_torque:.2f}Nm > Max {self.max_torque_output:.2f}Nm"
            print(f"🚨 {self.name} CRITICAL FAILURE: {self.fail_reason}")
            # We don't return here immediately so we can return the last known position below

        # 2. Distance Calculation
        dist_to_go = target_pos - self.actual_pos

        # 3. Velocity Logic (P-Control + Profile Feed-Forward)
        # We limit the speed based on the Motor's Physical Max (considering gears)
        desired_vel = np.sign(dist_to_go) * min(abs(target_velocity), abs(dist_to_go/dt), self.max_velocity)

        # 4. Acceleration Logic (Inertia)
        vel_diff = desired_vel - self.current_velocity
        max_vel_change = self.max_accel * dt
        
        if abs(vel_diff) > max_vel_change:
            self.current_velocity += max_vel_change * np.sign(vel_diff)
        else:
            self.current_velocity = desired_vel

        # 5. Hard Clamp to Max Velocity
        self.current_velocity = np.clip(self.current_velocity, -self.max_velocity, self.max_velocity)

        # 6. Update Position
        if not self.failed:
            self.actual_pos += self.current_velocity * dt

        # 7. Encoder Simulation (Quantization + Noise)
        # We simulate the steps, then the encoder reading that steps
        physical_pos = round(self.actual_pos / EFFECTIVE_STEP) * EFFECTIVE_STEP
        sensor_reading = round(physical_pos / ENCODER_RES) * ENCODER_RES
        sensor_reading += np.random.normal(0, ENCODER_NOISE)

        return sensor_reading

# ============================================================
# ▶️ TRAPEZOIDAL PROFILE GENERATOR (Preserved)
# ============================================================

def generate_trapezoidal_profile(target_pos, commanded_speed, dt):
    """Generates a trapezoidal velocity profile to reach target_pos."""
    max_vel = commanded_speed
    accel_time = max_vel / MOTOR_MAX_ACCEL_SHAFT # Use global default for profile generation
    accel_dist = 0.5 * MOTOR_MAX_ACCEL_SHAFT * accel_time**2  

    if accel_dist * 2 > target_pos:  # Triangular profile
        accel_time = np.sqrt(target_pos / MOTOR_MAX_ACCEL_SHAFT)
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
            vel = MOTOR_MAX_ACCEL_SHAFT * t
            pos = 0.5 * MOTOR_MAX_ACCEL_SHAFT * t**2
        elif t < accel_time + cruise_time:
            vel = max_vel
            pos = accel_dist + max_vel * (t - accel_time)
        else:
            t_dec = t - (accel_time + cruise_time)
            vel = max_vel - MOTOR_MAX_ACCEL_SHAFT * t_dec
            pos = accel_dist + cruise_dist + max_vel * t_dec - 0.5 * MOTOR_MAX_ACCEL_SHAFT * t_dec**2
        vel_profile[i] = vel
        pos_profile[i] = pos

    return time_points, pos_profile, vel_profile


# ============================================================
# 🚀 EXECUTION BLOCK (Standalone Test Runner)
# ============================================================
if __name__ == "__main__":
    
    # --- 📂 PATH SETUP ---
    script_dir = os.path.dirname(os.path.abspath(__file__))
    BASE_LOG_DIR = os.path.normpath(os.path.join(script_dir, "..", "..", "logs"))

    # Ensure logs directory exists (even if running standalone)
    if not os.path.exists(BASE_LOG_DIR):
        os.makedirs(BASE_LOG_DIR, exist_ok=True)

    existing_runs = [
        f.name for f in os.scandir(BASE_LOG_DIR) if f.is_dir() and f.name.startswith("run")
    ]

    if existing_runs:
        run_numbers = [int(re.search(r"run(\d+)", r).group(1)) for r in existing_runs if re.search(r"run(\d+)", r)]
        next_run = max(run_numbers) + 1 if run_numbers else 1
    else:
        next_run = 1

    RUN_LOG_DIR = os.path.join(BASE_LOG_DIR, f"run{next_run}")
    os.makedirs(RUN_LOG_DIR, exist_ok=True)
    print(f"\n📂 Logging Single-Motor simulation to: {RUN_LOG_DIR}\n")

    def get_next_filename():
        files = os.listdir(RUN_LOG_DIR)
        numbers = [int(re.search(r"(\d+)", f).group(1)) for f in files if re.search(r"motor_log_(\d+)", f)]
        next_num = 1 if not numbers else max(numbers) + 1
        return os.path.join(RUN_LOG_DIR, f"motor_log_{next_num:03d}.csv")

    def run_simulation():
        SPEEDS = [45, 60, 75, 90, 180, 270, 360, 720]
        HZ = 1000
        dt = 1.0 / HZ
        TARGET_POS = 720
        HOLD_TIME = 2.0

        print(f"   Testing NEMA 23 Motor Model (No Load)...")

        for speed in SPEEDS:
            # We initialize a 'Test' motor. 
            # We set gear_ratio=1.0 for this test to observe raw shaft speed behavior.
            motor = MockMotor(name="TestMotor", gear_ratio=1.0, max_torque_nm=3.0)
            
            # NOTE: We cap the command speed for the profile generator, 
            # but the motor class will also enforce its own physical limits.
            time_points, target_positions, target_velocities = generate_trapezoidal_profile(TARGET_POS, speed, dt)

            hold_steps = int(HOLD_TIME / dt)
            time_points = np.concatenate([time_points, time_points[-1] + np.arange(1, hold_steps+1)*dt])
            target_positions = np.concatenate([target_positions, np.full(hold_steps, TARGET_POS)])
            target_velocities = np.concatenate([target_velocities, np.zeros(hold_steps)])

            data_log = []

            for t, target_pos, target_vel in zip(time_points, target_positions, target_velocities):
                # We pass external_load_torque=0.0 because this is a simple bench test
                actual = motor.update(target_pos, target_vel, dt, external_load_torque=0.0)
                
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
            print(f"✅ Data saved to: {filename}, time-to-target={time_points[len(time_points)-hold_steps-1]:.3f} s")

    # Actually Run it
    run_simulation()