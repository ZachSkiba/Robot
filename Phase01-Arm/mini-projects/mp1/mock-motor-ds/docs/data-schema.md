# Data Logging Contract

All logs (virtual or real) must follow this CSV format.

| Column | Type | Description |
| :--- | :--- | :--- |
| `timestamp_ms` | int | Time in milliseconds since start |
| `command_id` | int | ID of the current move command |
| `target_pos` | float | Desired position (degrees) |
| `current_pos` | float | Actual position read by encoder (degrees) |
| `velocity` | float | Velocity (degrees/sec) |
| `pwm_effort` | int | Simulated motor power (0-255) |
| `error` | float | `target_pos` - `current_pos` |
