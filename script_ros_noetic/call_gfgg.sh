# Source ros workspace.
cd ~/roboslam_ws
source ~/roboslam_ws/devel/setup.bash
cd src/gf_orb_slam2
source export_env.sh

# Launch svo with arguments $(num_feature) $(dataset) $(dir).
LAUNCH_FILE='gazebo_multisense.launch good_feature_num:='$1' output_dir:='$2
echo $LAUNCH_FILE
roslaunch gf_orb_slam2 $LAUNCH_FILE