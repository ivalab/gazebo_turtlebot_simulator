## Config

Assuming desktop full verison of ros-kinetic has been installed, and a catkin workspace has been created at 

	/home/XXX/catkin_ws/

Follow the instruction at `meta_ClosedLoopBench` to clone all required catkin packages in the workspace:

	https://github.com/ivalab/meta_ClosedLoopBench

Clone all packages from pips_vslam.rosinstall in PiPS meta repo:

	https://github.gatech.edu/ivabots/meta_pips

Navigate to the dir of similator package `gazebo_turtlebot_simulaton`.  Adjust the catkin workspace in __set_up_sim.sh__:

	export CATKIN_WS=/home/XXX/catkin_ws/

Then execute the auto setup script __set_up_sim.sh__ (sudo needed):

	./set_up_sim.sh

Build all packages:

	catkin config --cmake-args -DCMAKE_BUILD_TYPE=Release
	catkin build

## Launch

Adjust the IMU config to be simulated in gazebo_closeloop_turtlebot.launch, i.e. mpu_6000 or ADIS_16448

Launch the gazebo simulation:

	cd /home/XXX/catkin_ws/src/gazebo_turtlebot_simulator/launch/ 
	roslaunch ./gazebo_closeloop_turtlebot.launch

Adjust the parameters in batch evaluation script, e.g. feedback_GF_stereo_batch_eval.py

Start batch evalution:

	cd /home/XXX/catkin_ws/src/gazebo_turtlebot_simulator/script 
	python feedback_GF_stereo_batch_eval.py

## Results Collection

The closed-loop navigation output are recorded as rosbag.  
To convert these rosbags to text files, clone the repo: 

	https://github.gatech.edu/VSLAM/mat_from_rosbag

Then edit the batch conversion script 
	
	./script/batch_closedloop.sh

And execute it

Finally, use the closed-loop evaluation script in SLAM Evaluation repo:

	https://github.gatech.edu/VSLAM/SLAM_Evaluation

Refer to the evaluation script on how to quantify the navigation performance and latency consumption:

	closeLoop_error_RAS19.m

## Contact information

- Yipu Zhao			yipu.zhao@gatech.edu
- Justin S. Smith	jssmith@gatech.edu
- Patricio A. Vela	pvela@gatech.edu