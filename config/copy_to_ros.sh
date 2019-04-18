export CONFIG_SRC=${CATKIN_WS}/src/gazebo_turtlebot_simulator/config
export TURTLE_TAR=/opt/ros/${ROS_DISTRO}/share/turtlebot_description
export KOBUKI_TAR=/opt/ros/${ROS_DISTRO}/share/kobuki_description
# export TURTLE_TAR=${CATKIN_WS}/src/turtlebot/turtlebot_description
# export KOBUKI_TAR=${CATKIN_WS}/src/kobuki/kobuki_description

sudo cp ${CONFIG_SRC}/kobuki_ADIS_16448* 				${KOBUKI_TAR}/urdf
sudo cp ${CONFIG_SRC}/kobuki_mpu_6000* 					${KOBUKI_TAR}/urdf
#
sudo cp ${CONFIG_SRC}/kobuki_hexagons_* 				${TURTLE_TAR}/robots
sudo cp ${CONFIG_SRC}/fisheye_stereo.urdf.xacro 			${TURTLE_TAR}/urdf/sensors
#
sudo cp ${CONFIG_SRC}/turtlebot_gazebo_fisheye_stereo.urdf.xacro 	${TURTLE_TAR}/urdf
sudo cp ${CONFIG_SRC}/turtlebot_properties_fisheye_stereo.urdf.xacro 	${TURTLE_TAR}/urdf
# back up the original ones
sudo cp ${TURTLE_TAR}/urdf/turtlebot_properties.urdf.xacro 	${TURTLE_TAR}/urdf/turtlebot_properties.urdf.xacro.bak
sudo cp ${CONFIG_SRC}/turtlebot_properties.urdf.xacro 		${TURTLE_TAR}/urdf
sudo cp ${TURTLE_TAR}/urdf/turtlebot_gazebo.urdf.xacro 		${TURTLE_TAR}/urdf/turtlebot_gazebo.urdf.xacro.bak
sudo cp ${CONFIG_SRC}/turtlebot_gazebo.urdf.xacro 			${TURTLE_TAR}/urdf
