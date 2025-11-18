#!/usr/bin/env python3
"""
detection_logic.py

Pure-Python logic for deciding whether to stop on a red traffic light
based on object detector outputs.

This file does NOT depend on ROS, so we can unit-test it easily.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class Detection:
    """
    Minimal abstraction of an object detection.

    When we later connect to duckietown-objdet, we'll translate its
    message format into this simple Detection type.
    """
    label: str         # e.g. "traffic_light", "duckiebot", "duckie"
    state: str = ""    # e.g. "red", "yellow", "green" (if available)
    score: float = 1.0 # confidence score in [0,1], if we have it


def should_stop_for_red(detections: List[Detection]) -> bool:
    """
    Decide whether we should stop based on a list of detections.

    For now, the rule is:
      - If there is any detection with label containing "traffic_light"
        (case-insensitive),
      - AND its state is "red" (case-insensitive),
      - AND its score >= 0.5 (if score is provided),

    then we return True (stop). Otherwise, False (go).
    """
    for det in detections:
        label = (det.label or "").lower()
        state = (det.state or "").lower()
        score = det.score if det.score is not None else 1.0

        if "traffic" in label and "light" in label:
            # This is some kind of traffic light detection
            if state == "red" and score >= 0.5:
                return True

    return False


# ---------------------------------------------------------------------
# Simple self-test when run as a script
# ---------------------------------------------------------------------
def _self_test():
    print("[detection_logic] Running self-test...")

    case1 = [
        Detection(label="traffic_light", state="red", score=0.9),
    ]
    print("Case 1 (red light) -> should_stop_for_red =", should_stop_for_red(case1))

    case2 = [
        Detection(label="traffic_light", state="green", score=0.9),
    ]
    print("Case 2 (green light) -> should_stop_for_red =", should_stop_for_red(case2))

    case3 = [
        Detection(label="duckie", state="", score=0.9),
    ]
    print("Case 3 (no traffic light) -> should_stop_for_red =", should_stop_for_red(case3))

    case4 = [
        Detection(label="traffic_light", state="red", score=0.2),
    ]
    print("Case 4 (low-confidence red) -> should_stop_for_red =", should_stop_for_red(case4))

    print("[detection_logic] Self-test complete.")


if __name__ == "__main__":
    _self_test()
