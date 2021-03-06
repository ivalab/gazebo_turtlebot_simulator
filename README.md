![](https://github.com/ivalab/demo_gif/blob/master/closedloop_demo.gif)


## Config

Assuming desktop full verison of ros-kinetic has been installed, and a catkin workspace has been created at 

	/home/XXX/catkin_ws/

Follow the instruction at `meta_ClosedLoopBench` to clone all required catkin packages in the workspace:

	https://github.com/ivalab/meta_ClosedLoopBench

Navigate to the dir of simulator package `gazebo_turtlebot_simulaton`.  Adjust the catkin workspace in __set_up_sim.sh__:

	export CATKIN_WS=/home/XXX/catkin_ws/

Then execute the auto setup script __set_up_sim.sh__ (will be asked for sudo authorization):

	./set_up_sim.sh

Build all packages:

	catkin config --cmake-args -DCMAKE_BUILD_TYPE=Release
	catkin build

## Launch Simulator

Launch the gazebo simulation:

	cd /home/XXX/catkin_ws/src/gazebo_turtlebot_simulator/launch/ 
	roslaunch ./gazebo_closeloop_turtlebot.launch


By default the gazebo GUI is off. To enable gazebo GUI during simulation, simply set arg gui in gazebo_closeloop_turtlebot.launch to true:

	<arg name="gui" default="true"/>

The IMU spec can be adjusted as well.  The two example IMU specs provided are mpu_6000 and ADIS_16448. Switch IMU spec by editing arg imu_sensor:

	<arg name="imu_sensor"  value="mpu_6000" />

Or

	<arg name="imu_sensor"  value="ADIS_16448" />

Lastly, the visual sensor can be adjusted with arg 3d_sensor:

	<arg name="3d_sensor"   value="fisheye_stereo" />

Or

	<arg name="3d_sensor"   value="kinect" />

Or

	<arg name="3d_sensor"   value="asus_xtion_pro" />

## Launch Closed-loop Evaluation

Adjust the parameters in batch evaluation script, e.g. [feedback_GFGG_stereo_batch_eval.py](https://github.com/ivalab/gazebo_turtlebot_simulator/blob/master/script/feedback_GFGG_stereo_batch_eval.py).  Detailed descriptions on each parameter are provided.

After settting the parameters, start batch evalution:

	cd /home/XXX/catkin_ws/src/gazebo_turtlebot_simulator/script 
	python feedback_GFGG_stereo_batch_eval.py

An rviz config is provided for visualization:

	rviz -d /home/XXX/catkin_ws/src/gazebo_turtlebot_simulator/closeloop_viz.rviz	

## Results Collection

The closed-loop navigation output are recorded as rosbag.  
To convert these rosbags to text files, clone the repo: 

	https://github.com/ivalab/mat_from_rosbag

Then edit and execute the batch conversion script, so that `CLOSEDLOOP_DIR` is the folder all closed-loop evaluation rosbags are saved within:
	
	./script/batch_closedloop.sh

Finally, use the closed-loop evaluation script in SLAM Evaluation repo:

	https://github.com/YipuZhao/SLAM_Evaluation

Refer to the evaluation script on how to quantify the navigation performance and latency consumption:

	closeLoop_error_TRO21.m

## Contact information

- Yipu Zhao		yipu.zhao@gatech.edu
- Justin S. Smith	jssmith@gatech.edu
- Patricio A. Vela	pvela@gatech.edu
