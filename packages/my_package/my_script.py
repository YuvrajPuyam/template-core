#!/usr/bin/env python3
"""
my_script.py

Local test harness for detection_logic, simulating what the
TrafficLightSupervisorNode would do (without ROS).

We:
- Assume a lane follower wants v = 0.25, omega = 0.0
- Simulate a sequence of detection scenarios over time
- Use should_stop_for_red() to decide whether to override with STOP
"""

import time
from detection_logic import Detection, should_stop_for_red


def simulate_step(step_idx: int, detections):
    """Simulate one timestep: print detections and resulting command."""
    lane_v = 0.25
    lane_omega = 0.0

    stop = should_stop_for_red(detections)

    if stop:
        v_cmd = 0.0
        omega_cmd = 0.0
        decision = "STOP"
    else:
        v_cmd = lane_v
        omega_cmd = lane_omega
        decision = "GO"

    print(f"\n--- Step {step_idx} ---")
    print(f"Detections: {detections}")
    print(f"Decision : {decision}")
    print(f"v_cmd    : {v_cmd:.2f}")
    print(f"omega_cmd: {omega_cmd:.2f}")


def main():
    print("[core] Starting local TL supervisor simulation (no ROS).")

    timeline = [
        ("No traffic light yet", []),
        ("Green traffic light", [Detection(label="traffic_light", state="green", score=0.9)]),
        ("Red traffic light appears", [Detection(label="traffic_light", state="red", score=0.9)]),
        ("Red traffic light still there", [Detection(label="traffic_light", state="red", score=0.8)]),
        ("Red disappears", []),
    ]

    for i, (desc, dets) in enumerate(timeline):
        print(f"\nScenario: {desc}")
        simulate_step(i, dets)
        time.sleep(0.5)

    print("\n[core] Simulation finished.")


if __name__ == "__main__":
    main()
