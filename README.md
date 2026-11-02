# ROS 2 safety-awareness reference snippets (research demonstration)

**NOT FOR VEHICLE ACTUATION, NOT FUNCTIONALLY SAFE, NOT CERTIFIED, NO ASIL CLAIM.**

The `safety_guard_demo` example illustrates only software validity screening of a ROS 2 feature proposal. It is **not** an independent monitor, safe brake controller or a complete implementation of the architecture in the paper. Never route guard acceptance directly to an actuator.

## What is provided
- `adas_safety_interfaces/msg/*.msg`: typed candidate ROS 2 IDL. ROSIDL package metadata is included for testing, subject to interface review.
- `safety_guard_demo/safety_guard_demo/guard_logic.py`: testable, ROS-independent monitoring logic.
- `safety_guard_demo/safety_guard_demo/guard_node.py`: illustrative rclpy subscription/status publisher using the custom interface. An ament_python package is included for local colcon builds; not a production implementation.
- `safety_guard_demo/tests/test_guard_logic.py`: 6 deterministic pytest scenarios; requires only pytest and Python.

## Run local tests
```bash
cd code/safety_guard_demo
PYTHONPATH=. python -m pytest -q tests
```

## Production gaps
- Safe, synchronized timebase including jump detection and capture-to-consumption age. ROS wall time alone is NOT sufficient.
- Sequence wrap/reset strategy and replay-resistant authenticated transport.
- Hazard-specific FTTI, arbitration, fault reaction and mode-dependent behavior.
- Proven partitioning/FFI, safety software lifecycle and deployment configuration, fault coverage, hardware diagnostics.
- Formal safety requirement verification, HIL/vehicle testing, SOTIF scenarios, cybersecurity engineering and tools/OS qualification arguments.
- Demonstration uses Python, heap allocations and callbacks and therefore is **not a hard real-time or ASIL codebase**.

# Origin / scope
Original explanatory sample code written for the conference package, inspired by requirements synthesis from cited research (not copied from the uploaded papers).

## Example ROS 2 build on a machine with ROS 2 installed
```bash
mkdir -p ~/adas_demo_ws/src
cp -r adas_safety_interfaces safety_guard_demo ~/adas_demo_ws/src/
cd ~/adas_demo_ws
source /opt/ros/$ROS_DISTRO/setup.bash
colcon build --symlink-install
source install/setup.bash
ros2 run safety_guard_demo guard_demo
```
Defaults to clock-untrusted, so all proposals will be rejected. This is intentional. Only in a fully controlled simulation may you set `clock_trusted_for_demo:=true` for experiments. No actuator node is present.
