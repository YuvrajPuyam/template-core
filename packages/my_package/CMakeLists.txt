cmake_minimum_required(VERSION 2.8.3)
project(my_package)

## Find catkin and required components
find_package(catkin REQUIRED COMPONENTS
  rospy
  duckietown_msgs
  std_msgs
)

## Declare the catkin package
catkin_package()

## Install Python nodes
## (traffic_light_supervisor_node.py lives in this same directory)
catkin_install_python(PROGRAMS
  traffic_light_supervisor_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
