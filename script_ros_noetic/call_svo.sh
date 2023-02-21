#!/bin/bash

# This script is to run svo in a separate terminal.

# Source ros workspace.
cd ~/svo_ws
source ~/svo_ws/devel/setup.bash

# Launch svo with arguments $(num_feature) $(dataset) $(dir).
LAUNCH_FILE='gazebo_stereo_only.launch grid_size:='$1' dataset:='$2' trace_dir:='$3
echo $LAUNCH_FILE
roslaunch svo_ros $LAUNCH_FILE