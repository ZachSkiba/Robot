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
                 max_velocity=None, max_accel=None, belt_stiffness=800):
        """
        Universal MockMotor with Internal Friction & Efficiency.
        """
        self.name = name
        self.gear_ratio = gear_ratio
        self.belt_stiffness = belt_stiffness
        
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
        # UPDATED: Belts are more efficient (90%) than cheap gearboxes (85%)
        self.efficiency = 0.90 
        
        # We calculate the max output torque considering this loss immediately
        self.max_torque_output = max_torque_nm * gear_ratio * self.efficiency

        # 3. Friction Constants (The "Gunk" Factors)
        # UPDATED: Lowered stiction from 0.2 to 0.02. 
        # 0.2 was like a rusty gearbox. 0.02 is a smooth belt drive.
        self.stiction_nm = 0.02 * gear_ratio  
        
        # NEW: Increase damping by 50x-100x to simulate grease/belt losses
        # This acts as a "shock absorber" for the 3kg weight
        self.viscous_coeff = 0.01 * gear_ratio

        # --- BELT PHYSICS SETUP ---
        self.current_belt_stretch = 0.0       # Degrees
        # -------------------------------

        # State
        self.motor_angle_deg = 0.0
        self.actual_pos = 0.0
        self.current_velocity = 0.0
        self.failed = False
        self.fail_reason = ""
        self.last_torque_usage = 0.0  # For logging

    def update(self, target_pos, target_velocity, dt, external_load_torque=0.0):
        """
        Updates motor physics including Inertia, Friction, and Belt Stretch.
        Returns the TRUE physical position of the arm link.
        """
        # 1. Failure Check (Gravity Slip)
        if self.failed:
            # If stalled, gravity pulls the arm down rapidly
            slip_speed = -np.sign(external_load_torque) * 20.0 * dt
            self.actual_pos += slip_speed
            return self.actual_pos

        # ==========================================
        # A. KINEMATICS (Motion Profiling)
        # ==========================================
        # Calculate how the MOTOR SHAFT wants to move (ignoring stretch for now)
        
        # Distance to target (in motor space)
        dist_to_go = target_pos - self.motor_angle_deg
        
        # Desired Velocity: Try to match target speed, but slow down if close to target
        desired_vel = np.sign(dist_to_go) * min(abs(target_velocity), abs(dist_to_go/dt), self.max_velocity)

        # Acceleration Limit: We cannot change velocity instantly
        vel_diff = desired_vel - self.current_velocity
        max_vel_change = self.max_accel * dt
        
        actual_accel = 0.0
        if abs(vel_diff) > max_vel_change:
            actual_accel = np.sign(vel_diff) * self.max_accel
            self.current_velocity += actual_accel * dt
        else:
            actual_accel = vel_diff / dt
            self.current_velocity = desired_vel

        # Update INTERNAL MOTOR Angle (The hard steel shaft position)
        self.motor_angle_deg += self.current_velocity * dt

        # ==========================================
        # B. DYNAMICS (Torques)
        # ==========================================
        # 1. Inertial Torque (Force needed to spin the rotor)
        # We must convert degrees/s^2 to radians/s^2 for correct Newton-meters
        accel_radians = np.radians(actual_accel) 
        # 0.002 kg m^2 is a reasonable estimate for Rotor + Gearbox + Belt inertia
        torque_inertial = accel_radians * 0.002

        # 2. Friction Torque
        # Direction opposes movement
        direction = np.sign(self.current_velocity) if self.current_velocity != 0 else np.sign(desired_vel)
        torque_friction = (self.stiction_nm * direction) + \
                          (self.viscous_coeff * self.current_velocity)

        # 3. Total Required Torque
        # Load + Friction + Inertia
        # We divide by efficiency because the motor works harder than the output shows
        total_required_torque = (external_load_torque + torque_friction + torque_inertial) / self.efficiency
        
        self.last_torque_usage = total_required_torque

        # ==========================================
        # C. STALL CHECK
        # ==========================================
        if abs(total_required_torque) > self.max_torque_output:
            self.failed = True
            self.fail_reason = (f"Over Torque: {total_required_torque:.2f} Nm > {self.max_torque_output:.2f} Nm")
            print(f"🔥 {self.name} STALLED: {self.fail_reason}")
            return self.actual_pos

        # ==========================================
        # D. COMPLIANCE (Belt Stretch)
        # ==========================================
        # Hooke's Law: F = kx  =>  x = F / k
        # The motor pulls the belt, the belt stretches.
        stretch_radians = total_required_torque / self.belt_stiffness
        self.current_belt_stretch = np.degrees(stretch_radians)

        # ==========================================
        # E. REAL JOINT POSITION
        # ==========================================
        # The arm is where the motor is MINUS the stretch (lag)
        # If gravity pulls down (positive torque), the arm lags behind (negative position relative to motor)
        self.actual_pos = self.motor_angle_deg - self.current_belt_stretch

        # Return the TRUE physical position 
        # (The simulation loop handles the sensor quantization/noise)
        return self.actual_pos

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
                # Load oscillates between -15 Nm and +15 Nm
                simulated_gravity_load = 15.0 * np.sin(t * 2.0)
                
                actual = motor.update(target_pos, target_vel, dt, external_load_torque=simulated_gravity_load)
                
                data_log.append({
                    "timestamp_ms": int(t*1000),
                    "target_pos": round(target_pos, 3),
                    "sensor_pos": round(actual, 3),  
                    "real_arm_pos": round(motor.actual_pos, 3), 
                    "belt_stretch": round(motor.current_belt_stretch, 4), 
                    "error": round(target_pos - motor.actual_pos, 3),    
                    "velocity_cmd": speed,
                    "torque_load": round(simulated_gravity_load, 2),
                    "torque_total_req": round(motor.last_torque_usage, 2),
                    "hz": HZ
                })

            filename = get_next_filename()
            pd.DataFrame(data_log).to_csv(filename, index=False)
            print(f"✅ Data saved to: {filename}, time-to-target={time_points[len(time_points)-hold_steps-1]:.3f} s")

    # Actually Run it
    run_simulation()