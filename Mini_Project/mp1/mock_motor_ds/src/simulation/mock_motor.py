import pandas as pd
import numpy as np
import os
import re

# ============================================================
# ⚙️ MOTOR SPECS (Global Constants - Safe to Import)
# ============================================================

# Step / Resolution
MOTOR_STEP_ANGLE = 1.8
MICROSTEPS = 32         
EFFECTIVE_STEP = MOTOR_STEP_ANGLE / MICROSTEPS  # 0.05625 deg/step

# NEMA 23 / 17 Physical Limits (At the Motor Shaft, before Gears)
MOTOR_MAX_VELOCITY_SHAFT = 3600.0  # deg/s (600 RPM)
MOTOR_MAX_ACCEL_SHAFT = 6000.0     # deg/s^2

# Encoder Simulation
ENCODER_RES = 0.088
ENCODER_NOISE = 0.05

# ============================================================
# 🔧 MOTOR MODEL (CLASS - Now with FRICTION)
# ============================================================

class MockMotor:
    def __init__(self, name="Generic", gear_ratio=1.0, max_torque_nm=3.0, 
                 max_velocity=None, max_accel=None):
        """
        Universal MockMotor with Internal Friction & Efficiency.
        """
        self.name = name
        self.gear_ratio = gear_ratio
        
        # 1. Physics Limits (Calculated at the JOINT output)
        if max_velocity:
            self.max_velocity = max_velocity
        else:
            self.max_velocity = MOTOR_MAX_VELOCITY_SHAFT / gear_ratio

        if max_accel:
            self.max_accel = max_accel
        else:
            self.max_accel = MOTOR_MAX_ACCEL_SHAFT / gear_ratio

        # 2. Torque Limits & Efficiency
        # Real planetary gears lose ~15% power to heat/noise
        self.efficiency = 0.85 
        
        # We calculate the max output torque considering this loss immediately
        self.max_torque_output = max_torque_nm * gear_ratio * self.efficiency

        # 3. Friction Constants (The "Gunk" Factors)
        # Stiction: Force needed just to START moving (static friction)
        self.stiction_nm = 0.2 * gear_ratio  # Scales with gears
        # Viscous: Drag that increases with speed (like moving through honey)
        self.viscous_coeff = 0.002 * gear_ratio 

        # State
        self.actual_pos = 0.0
        self.current_velocity = 0.0
        self.failed = False
        self.fail_reason = ""
        self.last_torque_usage = 0.0  # For logging

    def update(self, target_pos, target_velocity, dt, external_load_torque=0.0):
        """
        Updates motor physics with Friction calculations.
        """
        # 1. Failure Check (The "Gravity Killer")
        if self.failed:
            return self.actual_pos

        # --- NEW: FRICTION PHYSICS ------------------------------------------
        # Direction opposes movement
        direction = np.sign(self.current_velocity) 
        if direction == 0: direction = np.sign(target_velocity) # Start-up logic

        # A. Friction Calculation
        # Stiction (Constant drag) + Viscous (Speed dependent drag)
        friction_torque = (self.stiction_nm * direction) + \
                          (self.viscous_coeff * self.current_velocity)
        
        # B. Total Required Torque
        # Motor must overcome: External Load (Gravity) + Internal Friction
        # And we divide by efficiency because the motor works harder than the output shows
        total_required_torque = (external_load_torque + friction_torque) / self.efficiency
        
        # Save for analysis
        self.last_torque_usage = total_required_torque 
        # --------------------------------------------------------------------

        # 2. STALL CHECK (Now uses the REAL total load)
        if abs(total_required_torque) > self.max_torque_output:
            self.failed = True
            self.fail_reason = (f"STALL: Req {abs(total_required_torque):.2f}Nm "
                                f"> Max {self.max_torque_output:.2f}Nm "
                                f"(Load: {external_load_torque:.2f} + Fric: {friction_torque:.2f})")
            print(f"🚨 {self.name} CRITICAL FAILURE: {self.fail_reason}")
            
            # REALISM UPGRADE: When a stepper stalls, it doesn't just hold position.
            # If gravity is strong, it slips backward.
            slip_speed = -np.sign(external_load_torque) * 20.0 * dt
            self.actual_pos += slip_speed
            return self.actual_pos

        # 3. Distance Calculation
        dist_to_go = target_pos - self.actual_pos

        # 4. Velocity Logic (P-Control + Profile Feed-Forward)
        desired_vel = np.sign(dist_to_go) * min(abs(target_velocity), abs(dist_to_go/dt), self.max_velocity)

        # 5. Acceleration Logic (Inertia)
        vel_diff = desired_vel - self.current_velocity
        max_vel_change = self.max_accel * dt
        
        if abs(vel_diff) > max_vel_change:
            self.current_velocity += max_vel_change * np.sign(vel_diff)
        else:
            self.current_velocity = desired_vel

        # 6. Hard Clamp to Max Velocity
        self.current_velocity = np.clip(self.current_velocity, -self.max_velocity, self.max_velocity)

        # 7. Update Position
        self.actual_pos += self.current_velocity * dt

        # 8. Encoder Simulation
        physical_pos = round(self.actual_pos / EFFECTIVE_STEP) * EFFECTIVE_STEP
        sensor_reading = round(physical_pos / ENCODER_RES) * ENCODER_RES
        sensor_reading += np.random.normal(0, ENCODER_NOISE)

        return sensor_reading

# ============================================================
# ▶️ TRAPEZOIDAL PROFILE GENERATOR (Unchanged)
# ============================================================

def generate_trapezoidal_profile(target_pos, commanded_speed, dt):
    """Generates a trapezoidal velocity profile to reach target_pos."""
    max_vel = commanded_speed
    accel_time = max_vel / MOTOR_MAX_ACCEL_SHAFT 
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

        print(f"   Testing NEMA 23 Motor Model (With Friction)...")

        for speed in SPEEDS:
            # Note: We now use gear_ratio=20.0 to see the effect of multiplied friction
            motor = MockMotor(name="ShoulderJoint", gear_ratio=20.0, max_torque_nm=3.0)
            
            time_points, target_positions, target_velocities = generate_trapezoidal_profile(TARGET_POS, speed, dt)

            hold_steps = int(HOLD_TIME / dt)
            time_points = np.concatenate([time_points, time_points[-1] + np.arange(1, hold_steps+1)*dt])
            target_positions = np.concatenate([target_positions, np.full(hold_steps, TARGET_POS)])
            target_velocities = np.concatenate([target_velocities, np.zeros(hold_steps)])

            data_log = []

            for t, target_pos, target_vel in zip(time_points, target_positions, target_velocities):
                # We simulate a "Gravity Wave" load to see if it stalls
                # Load oscillates between -50 Nm and +50 Nm
                simulated_gravity_load = 50.0 * np.sin(t * 2.0) 
                
                actual = motor.update(target_pos, target_vel, dt, external_load_torque=simulated_gravity_load)
                
                data_log.append({
                    "timestamp_ms": int(t*1000),
                    "target_pos": round(target_pos, 3),
                    "actual_pos": round(actual, 3),
                    "error": round(target_pos-actual, 3),
                    "velocity_cmd": speed,
                    "torque_load": round(simulated_gravity_load, 2),
                    "torque_total_req": round(motor.last_torque_usage, 2), # LOGGING TOTAL LOAD
                    "hz": HZ
                })

            filename = get_next_filename()
            pd.DataFrame(data_log).to_csv(filename, index=False)
            print(f"✅ Data saved to: {filename}, time-to-target={time_points[len(time_points)-hold_steps-1]:.3f} s")

    # Actually Run it
    run_simulation()