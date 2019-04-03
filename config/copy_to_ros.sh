export CONFIG_SRC=/home/yipuzhao/catkin_ws/src/gazebo_turtlebot_simulator/config

sudo cp ${CONFIG_SRC}/kobuki_ADIS_16448* 	/opt/ros/kinetic/share/kobuki_description/urdf
sudo cp ${CONFIG_SRC}/kobuki_mpu_6000* 	/opt/ros/kinetic/share/kobuki_description/urdf
#
sudo cp ${CONFIG_SRC}/kobuki_hexagons_* 			/opt/ros/kinetic/share/turtlebot_description/robots
sudo cp ${CONFIG_SRC}/fisheye_stereo.urdf.xacro 	/opt/ros/kinetic/share/turtlebot_description/urdf/sensors
#
sudo cp ${CONFIG_SRC}/turtlebot_gazebo_fisheye_stereo.urdf.xacro 		/opt/ros/kinetic/share/turtlebot_description/urdf
sudo cp ${CONFIG_SRC}/turtlebot_properties_fisheye_stereo.urdf.xacro 	/opt/ros/kinetic/share/turtlebot_description/urdf
sudo cp ${CONFIG_SRC}/turtlebot_properties.urdf.xacro 					/opt/ros/kinetic/share/turtlebot_description/urdf
sudo cp ${CONFIG_SRC}/turtlebot_gazebo.urdf.xacro 						/opt/ros/kinetic/share/turtlebot_description/urdf
