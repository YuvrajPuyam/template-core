#!/usr/bin/env python3
"""
traffic_light_supervisor_node.py

Skeleton of a ROS node that will:
- Subscribe to lane follower commands (CarCmd)
- Subscribe to object-dt detections
- Use detection_logic.should_stop_for_red() to decide whether to stop
- Publish final CarCmd to the car_cmd_switch / wheels

Right now:
- If ROS is not available, it just prints a stub message and exits.
- ROS integration code is stubbed and marked with TODOs.
"""

import os
import time

# Local logic (same folder)
from detection_logic import Detection, should_stop_for_red

# Try to import ROS stuff, but don't hard-fail if not present
try:
    import rospy
    from duckietown_msgs.msg import CarCmd
    ROS_AVAILABLE = True
except ImportError as e:
    rospy = None
    CarCmd = None
    ROS_AVAILABLE = False
    _ros_import_error = e


class TrafficLightSupervisorNode:
    def __init__(self, lane_cmd_topic, final_cmd_topic, objdet_topic):
        """
        lane_cmd_topic: topic where lane follower publishes CarCmd
        final_cmd_topic: topic where we publish final CarCmd
        objdet_topic: topic where object-dt publishes detections
        """
        self.lane_cmd_topic = lane_cmd_topic
        self.final_cmd_topic = final_cmd_topic
        self.objdet_topic = objdet_topic

        self.last_lane_cmd = CarCmd() if ROS_AVAILABLE else None
        self.current_detections = []

        if ROS_AVAILABLE:
            rospy.loginfo(f"[tls] Subscribing to lane commands: {lane_cmd_topic}")
            rospy.loginfo(f"[tls] Subscribing to objdet detections: {objdet_topic}")
            rospy.loginfo(f"[tls] Publishing final commands to: {final_cmd_topic}")

            self.sub_lane = rospy.Subscriber(
                lane_cmd_topic, CarCmd, self._lane_cmd_cb, queue_size=1
            )

            # NOTE: The exact message type and fields for object-dt detections
            # will depend on the object-dt stack configuration.
            # For now, we assume a placeholder message with a .detections[] field.
            # We'll adjust once we see the real msg via `rostopic echo`.
            from std_msgs.msg import String  # placeholder just to compile

            self.sub_objdet = rospy.Subscriber(
                objdet_topic, String, self._objdet_cb_placeholder, queue_size=1
            )

            self.pub_final = rospy.Publisher(
                final_cmd_topic, CarCmd, queue_size=1
            )

    # ----------------- Callbacks -----------------

    def _lane_cmd_cb(self, msg: CarCmd):
        """Store the latest lane follower CarCmd."""
        self.last_lane_cmd = msg

    def _objdet_cb_placeholder(self, msg):
        """
        Placeholder objdet callback.

        Currently assumes we receive a String that encodes detections in
        some simple way; in practice, object-dt will have a richer message.

        TODO:
        - Replace this with the real message type from the object-dt stack.
        - Parse msg into a list[Detection].
        """
        # For now, just clear detections (pretend nothing is red)
        self.current_detections = []

    # ----------------- Main loop -----------------

    def run(self, rate_hz: float = 10.0):
        """
        Main loop:
        - Check detections via should_stop_for_red()
        - Either publish a stop command or pass-through lane command
        """
        if not ROS_AVAILABLE:
            print("[tls] ROS is not available; nothing to run.")
            return

        rate = rospy.Rate(rate_hz)
        rospy.loginfo(f"[tls] TrafficLightSupervisorNode running at {rate_hz} Hz")

        while not rospy.is_shutdown():
            stop = should_stop_for_red(self.current_detections)

            cmd_out = CarCmd()
            if stop:
                # Override with stop
                cmd_out.v = 0.0
                cmd_out.omega = 0.0
            else:
                # Pass through last lane follower command
                cmd_out.v = getattr(self.last_lane_cmd, "v", 0.0)
                cmd_out.omega = getattr(self.last_lane_cmd, "omega", 0.0)

            self.pub_final.publish(cmd_out)
            rate.sleep()


def main():
    if not ROS_AVAILABLE:
        print("[tls] ROS is not available in this environment.")
        print("      Import error was:", _ros_import_error)
        print("      This is expected on your laptop / non-ROS setup.")
        print("      Once you are in a Duckietown ROS container with duckietown_msgs,")
        print("      this node will become active.\n")
        return

    vehicle_name = os.environ.get("VEHICLE_NAME", "duckiebot")
    lane_cmd_topic = f"/{vehicle_name}/lane_controller_node/car_cmd"
    final_cmd_topic = f"/{vehicle_name}/car_cmd_switch_node/cmd"
    objdet_topic = f"/{vehicle_name}/object_detection/detections"  # TODO: confirm

    rospy.init_node("traffic_light_supervisor_node")
    node = TrafficLightSupervisorNode(
        lane_cmd_topic=lane_cmd_topic,
        final_cmd_topic=final_cmd_topic,
        objdet_topic=objdet_topic,
    )
    node.run()


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
traffic_light_supervisor_node.py

Skeleton of a ROS node that will:
- Subscribe to lane follower commands (CarCmd)
- Subscribe to object-dt detections
- Use detection_logic.should_stop_for_red() to decide whether to stop
- Publish final CarCmd to the car_cmd_switch / wheels

Right now:
- If ROS is not available, it just prints a stub message and exits.
- ROS integration code is stubbed and marked with TODOs.
"""

import os
import time

# Local logic (same folder)
from detection_logic import Detection, should_stop_for_red

# Try to import ROS stuff, but don't hard-fail if not present
try:
    import rospy
    from duckietown_msgs.msg import CarCmd
    ROS_AVAILABLE = True
except ImportError as e:
    rospy = None
    CarCmd = None
    ROS_AVAILABLE = False
    _ros_import_error = e


class TrafficLightSupervisorNode:
    def __init__(self, lane_cmd_topic, final_cmd_topic, objdet_topic):
        """
        lane_cmd_topic: topic where lane follower publishes CarCmd
        final_cmd_topic: topic where we publish final CarCmd
        objdet_topic: topic where object-dt publishes detections
        """
        self.lane_cmd_topic = lane_cmd_topic
        self.final_cmd_topic = final_cmd_topic
        self.objdet_topic = objdet_topic

        self.last_lane_cmd = CarCmd() if ROS_AVAILABLE else None
        self.current_detections = []

        if ROS_AVAILABLE:
            rospy.loginfo(f"[tls] Subscribing to lane commands: {lane_cmd_topic}")
            rospy.loginfo(f"[tls] Subscribing to objdet detections: {objdet_topic}")
            rospy.loginfo(f"[tls] Publishing final commands to: {final_cmd_topic}")

            self.sub_lane = rospy.Subscriber(
                lane_cmd_topic, CarCmd, self._lane_cmd_cb, queue_size=1
            )

            # NOTE: The exact message type and fields for object-dt detections
            # will depend on the object-dt stack configuration.
            # For now, we assume a placeholder message with a .detections[] field.
            # We'll adjust once we see the real msg via `rostopic echo`.
            from std_msgs.msg import String  # placeholder just to compile

            self.sub_objdet = rospy.Subscriber(
                objdet_topic, String, self._objdet_cb_placeholder, queue_size=1
            )

            self.pub_final = rospy.Publisher(
                final_cmd_topic, CarCmd, queue_size=1
            )

    # ----------------- Callbacks -----------------

    def _lane_cmd_cb(self, msg: CarCmd):
        """Store the latest lane follower CarCmd."""
        self.last_lane_cmd = msg

    def _objdet_cb_placeholder(self, msg):
        """
        Placeholder objdet callback.

        Currently assumes we receive a String that encodes detections in
        some simple way; in practice, object-dt will have a richer message.

        TODO:
        - Replace this with the real message type from the object-dt stack.
        - Parse msg into a list[Detection].
        """
        # For now, just clear detections (pretend nothing is red)
        self.current_detections = []

    # ----------------- Main loop -----------------

    def run(self, rate_hz: float = 10.0):
        """
        Main loop:
        - Check detections via should_stop_for_red()
        - Either publish a stop command or pass-through lane command
        """
        if not ROS_AVAILABLE:
            print("[tls] ROS is not available; nothing to run.")
            return

        rate = rospy.Rate(rate_hz)
        rospy.loginfo(f"[tls] TrafficLightSupervisorNode running at {rate_hz} Hz")

        while not rospy.is_shutdown():
            stop = should_stop_for_red(self.current_detections)

            cmd_out = CarCmd()
            if stop:
                # Override with stop
                cmd_out.v = 0.0
                cmd_out.omega = 0.0
            else:
                # Pass through last lane follower command
                cmd_out.v = getattr(self.last_lane_cmd, "v", 0.0)
                cmd_out.omega = getattr(self.last_lane_cmd, "omega", 0.0)

            self.pub_final.publish(cmd_out)
            rate.sleep()


def main():
    if not ROS_AVAILABLE:
        print("[tls] ROS is not available in this environment.")
        print("      Import error was:", _ros_import_error)
        print("      This is expected on your laptop / non-ROS setup.")
        print("      Once you are in a Duckietown ROS container with duckietown_msgs,")
        print("      this node will become active.\n")
        return

    vehicle_name = os.environ.get("VEHICLE_NAME", "duckiebot")
    lane_cmd_topic = f"/{vehicle_name}/lane_controller_node/car_cmd"
    final_cmd_topic = f"/{vehicle_name}/car_cmd_switch_node/cmd"
    objdet_topic = f"/{vehicle_name}/object_detection/detections"  # TODO: confirm

    rospy.init_node("traffic_light_supervisor_node")
    node = TrafficLightSupervisorNode(
        lane_cmd_topic=lane_cmd_topic,
        final_cmd_topic=final_cmd_topic,
        objdet_topic=objdet_topic,
    )
    node.run()


if __name__ == "__main__":
    main()
