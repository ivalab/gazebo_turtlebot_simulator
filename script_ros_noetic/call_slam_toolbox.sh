#!/bin/bash

# This script is to run slam_toolbox in a separate terminal.

# Source ros workspace.
cd ~/turtlebot_ws
source ~/turtlebot_ws/devel/setup.bash

# Launch dsol.
echo "Launching slam_toolbox."
roslaunch slam_toolbox gazebo_slam_toolbox.launch vis:=$1 output_pose_topic:=/scanmatch/pose output_odometry_topic:=/scanmatch/odom 2> >(grep -v TF_REPEATED_DATA buffer_core)
