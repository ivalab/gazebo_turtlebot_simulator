- Fill in the proper world file for gazebo_rectangular.launch
- roslaunch gazebo_rectangular.launch
- rviz
- roslaunch turtlebot_teleop keyboard_teleop.launch --screen
- rosbag record -O subset /multisense_sl/camera/left/image_raw /multisense_sl/camera/right/image_raw /tf



export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/home/yipuzhao/catkin_ws/src/gazebo_stereo_simulator/textureModel/models
roslaunch gazebo_rectangular.launch
