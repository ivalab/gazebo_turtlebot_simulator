CATKIN_WS=/home/yanwei/closed_loop_ws
export CONFIG_SRC=${CATKIN_WS}/src/gazebo_turtlebot_simulator/config
# export TURTLE_TAR=/opt/ros/${ROS_DISTRO}/share/turtlebot_description
# export KOBUKI_TAR=/opt/ros/${ROS_DISTRO}/share/kobuki_description
export TURTLE_TAR=${CATKIN_WS}/src/turtlebot2/turtlebot/turtlebot_description
export KOBUKI_TAR=${CATKIN_WS}/src/kobuki_ros/kobuki/kobuki_description

cp ${CONFIG_SRC}/kobuki_ADIS_16448* 				${KOBUKI_TAR}/urdf
cp ${CONFIG_SRC}/kobuki_mpu_6000* 					${KOBUKI_TAR}/urdf
cp ${CONFIG_SRC}/kobuki_hexagons_* 				${TURTLE_TAR}/robots
cp ${CONFIG_SRC}/fisheye_stereo.urdf.xacro 			${TURTLE_TAR}/urdf/sensors
cp ${CONFIG_SRC}/turtlebot_gazebo_fisheye_stereo.urdf.xacro 	${TURTLE_TAR}/urdf
cp ${CONFIG_SRC}/turtlebot_properties_fisheye_stereo.urdf.xacro 	${TURTLE_TAR}/urdf
# k up the original ones
cp ${TURTLE_TAR}/urdf/turtlebot_properties.urdf.xacro 	${TURTLE_TAR}/urdf/turtlebot_properties.urdf.xacro.bak
cp ${CONFIG_SRC}/turtlebot_properties.urdf.xacro 		${TURTLE_TAR}/urdf
cp ${TURTLE_TAR}/urdf/turtlebot_gazebo.urdf.xacro 		${TURTLE_TAR}/urdf/turtlebot_gazebo.urdf.xacro.bak
cp ${CONFIG_SRC}/turtlebot_gazebo.urdf.xacro 			${TURTLE_TAR}/urdf
