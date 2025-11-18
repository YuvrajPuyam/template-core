#!/bin/bash
set -e

source /environment.sh

# initialize launch file
dt-launchfile-init

# YOUR CODE BELOW THIS LINE
# ----------------------------------------------------------------------------

echo "[launcher] DT_REPO_PATH=${DT_REPO_PATH}"
echo "[launcher] VEHICLE_NAME=${VEHICLE_NAME:-not set}"
echo "[launcher] ROS_MASTER_URI=${ROS_MASTER_URI:-not set}"

# NOTE: dt-launchfile-init already sets things up so that relative paths like
# 'packages/my_package/my_script.py' are resolved from the repo root.
# So we do NOT change directories here.

HARNESS_SCRIPT="packages/my_package/my_script.py"
LAUNCH_FILE="launch/lane_following_with_tl_supervisor.launch"

# Local dev vs Duckiebot heuristic
if [ -z "${VEHICLE_NAME:-}" ] || [ "${VEHICLE_NAME}" = "Ubuntu" ]; then
    echo "[launcher] Local dev environment detected (no real Duckiebot)."
    echo "[launcher] Running harness: ${HARNESS_SCRIPT}"
    dt-exec python3 "${HARNESS_SCRIPT}"
else
    echo "[launcher] Duckiebot environment detected."
    echo "[launcher] (Future) would launch: ${LAUNCH_FILE}"
    # For now, since you don't have ROS/robot wired yet, still run the harness.
    # When ready, replace this line with the roslaunch call.
    dt-exec python3 "${HARNESS_SCRIPT}"
    # Later:
    # dt-exec roslaunch "${LAUNCH_FILE}" veh:="${VEHICLE_NAME}"
fi

# ----------------------------------------------------------------------------
# YOUR CODE ABOVE THIS LINE

# wait for app to end
dt-launchfile-join
