# DEMONSTRATION ONLY: ROS clock-domain timestamp, not automatically a safe time source.
# Production interface requires generated IDs, clocks, authenticated sender and safety analysis.
builtin_interfaces/Time sensor_stamp
uint32 sequence
uint8 mode
float32 requested_deceleration_mps2
float32 confidence
bool valid
