#!/bin/bash

# This script is to run msckf in a separate terminal.

# Source ros workspace.
cd ~/svo_ws
source ~/svo_ws/devel/setup.bash

# Launch msckf with arguments $(num_feature) $(imu_type).
LAUNCH_FILE='msckf_vio_gazebo_lmk'$1'_'$2'.launch output_prefix:='$3
echo $LAUNCH_FILE
roslaunch msckf_vio $LAUNCH_FILE