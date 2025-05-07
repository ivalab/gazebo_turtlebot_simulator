#!/bin/bash

# This script is to run dsol in a separate terminal.

# Source ros workspace.
cd ~/turtlebot_ws
source ~/turtlebot_ws/devel/setup.bash

# Launch dsol.
echo "Launching RTABMap."
roslaunch rtabmap_odom gazebo_trajectory_tracking.launch output_prefix:=$1