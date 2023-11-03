#!/bin/bash

# This script is to run dsol in a separate terminal.

# Source ros workspace.
cd ~/catkin_ws
source ~/catkin_ws/devel/setup.bash

# Launch dsol.
echo "Launching DSOL."
roslaunch dsol gazebo_DSOL_stereo.launch vis:=$1 save:=$2 cell_size:=$3 log:=100 min_log_level:=0