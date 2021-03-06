# This script is to run all the experiments in one program

import os
import subprocess
import time
import signal

# low IMU
IMU_Type = 'mpu6000';
# high IMU
# IMU_Type = 'ADIS16448';

# TODO 
# figure out how to set target vel in depth_path_following
# spawn textured obstacles along the desired path
Fwd_Vel_List = [1.0] # [0.5, 1.0, 1.5] # [0.5, 1.0]; # [0.5, 0.75, 1.0]; # 
Number_GF_List = [120] # [60, 80, 100, 120] # [40, 60, 80, 120, 160];

Num_Repeating = 50 # 10 # 

SleepTime = 3 # 5 # 
# Duration = 30 # 60

do_rectify = str('false');
do_vis = str('false');

# path_slam_config = '/home/yipu/catkin_ws/src/ORB_Data/'
path_slam_config = '/home/yipuzhao/ros_workspace/package_dir/ORB_Data/'


#----------------------------------------------------------------------------------------------------------------------
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ALERT = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


for ri, num_gf in enumerate(Number_GF_List):

    Experiment_prefix = 'ObsNumber_' + str(int(num_gf))

    for vn, fv in enumerate(Fwd_Vel_List):
        # for sn, sname in enumerate(SeqNameList):

            # SeqName = SeqNameList[sn]
            Result_root = '/mnt/DATA/tmp/ClosedNav/debug/'
            # Result_root = '/media/yipu/1399F8643500EDCD/ClosedNav_dev/' + SeqName + '/' + IMU_Type + '/GF_pyr8_gpu/'
            # Result_root = '/mnt/DATA/tmp/ClosedNav_v4/' + SeqName + '/low_imu/GF_gpu/'
            Experiment_dir = Result_root + Experiment_prefix + '_Vel' + str(fv)
            cmd_mkdir = 'mkdir -p ' + Experiment_dir
            subprocess.call(cmd_mkdir, shell=True)

            for iteration in range(0, Num_Repeating):
                
                print bcolors.ALERT + "====================================================================" + bcolors.ENDC
                # print bcolors.ALERT + "Round: " + str(iteration + 1) + "; Seq: " + SeqName + "; Vel: " + str(fv)
                print bcolors.ALERT + "Round: " + str(iteration + 1) + "; Vel: " + str(fv)

                path_track_logging = Experiment_dir + '/round' + str(iteration + 1)
                path_map_logging = Experiment_dir + '/round' + str(iteration + 1) + '_Map'
                num_good_feature = str(num_gf*3)
                # path_type = SeqName
                velocity_fwd = str(fv)
                # duration = float(SeqLengList[sn]) / float(fv) + SleepTime
                duration = 999 # 120

                cmd_reset  = str("python reset_turtlebot_pose.py && rostopic pub -1 /mobile_base/commands/reset_odometry std_msgs/Empty '{}'") 
                # cmd_reset = str('rosservice call /gazebo/reset_simulation "{}"')
                cmd_slam   = str('roslaunch ../launch/gazebo_GFGG_stereo.launch' \
                    + ' path_slam_config:=' + path_slam_config \
                    + ' num_good_feature:=' + num_good_feature \
                    + ' path_track_logging:=' + path_track_logging \
                    + ' path_map_logging:=' + path_map_logging \
                    + ' do_rectify:=' + do_rectify \
                    + ' do_vis:=' + do_vis)
                cmd_esti   = str('roslaunch msf_updates gazebo_msf_stereo.launch' \
                    + ' imu_type:=' + IMU_Type + ' ' \
                    + ' topic_slam_pose:=/ORB_SLAM/camera_pose_in_imu ' \
                    + ' link_slam_base:=left_camera_frame' )
                cmd_stereo = str('roslaunch elas_ros elas.launch stereo:=/multisense_sl/camera')
                # controller already being called in pips
                cmd_pips  = str('roslaunch ../launch/closednav_global_follower.launch target_vel:=' + velocity_fwd)
                cmd_log   = str('roslaunch ../launch/gazebo_logging.launch path_data_logging:=' + path_track_logging )
                # set a random goal
                cmd_trig   = str("rostopic pub -1 /move_base_simple/goal geometry_msgs/PoseStamped " + \
                    "'{header: {stamp: now, frame_id: 'map'}, pose: {position: {x: -8.0, y: 9.0, z: 0.0}, orientation: {w: 1.0}}}' ") 

                print bcolors.WARNING + "cmd_reset: \n" + cmd_reset + bcolors.ENDC
                print bcolors.WARNING + "cmd_slam: \n"  + cmd_slam  + bcolors.ENDC
                print bcolors.WARNING + "cmd_esti: \n"  + cmd_esti  + bcolors.ENDC
                print bcolors.WARNING + "cmd_stereo: \n"+ cmd_stereo+ bcolors.ENDC
                print bcolors.WARNING + "cmd_pips: \n"  + cmd_pips  + bcolors.ENDC
                print bcolors.WARNING + "cmd_log: \n"   + cmd_log  + bcolors.ENDC
                print bcolors.WARNING + "cmd_trig: \n"  + cmd_trig  + bcolors.ENDC

                print bcolors.OKGREEN + "Reset simulation" + bcolors.ENDC
                subprocess.Popen(cmd_reset, shell=True)

                print bcolors.OKGREEN + "Sleeping for a few secs to reset gazebo" + bcolors.ENDC
                time.sleep(SleepTime)
                # time.sleep(60)

                print bcolors.OKGREEN + "Launching SLAM" + bcolors.ENDC
                subprocess.Popen(cmd_slam, shell=True)

                print bcolors.OKGREEN + "Launching State Estimator" + bcolors.ENDC
                subprocess.Popen(cmd_esti, shell=True)

                print bcolors.OKGREEN + "Launching Dense Stereo Matching" + bcolors.ENDC
                subprocess.Popen(cmd_stereo, shell=True)

                print bcolors.OKGREEN + "Launching PiPS" + bcolors.ENDC
                subprocess.Popen(cmd_pips, shell=True)

                print bcolors.OKGREEN + "Launching Logger" + bcolors.ENDC
                subprocess.Popen(cmd_log, shell=True)
                
                print bcolors.OKGREEN + "Sleeping for a few secs to stabilize msf" + bcolors.ENDC
                time.sleep(SleepTime * 3)
                
                Duration = duration + SleepTime
                print bcolors.OKGREEN + "Start simulation with " + str(Duration) + " secs" + bcolors.ENDC
                # proc_trig = subprocess.call(cmd_trig, shell=True)
                subprocess.Popen(cmd_trig, shell=True)

                time.sleep(Duration)

                print bcolors.OKGREEN + "Finish simulation, kill the process" + bcolors.ENDC
                subprocess.call('rosnode kill data_logging', shell=True)
                time.sleep(SleepTime)
                subprocess.call('rosnode kill Stereo', shell=True)
                subprocess.call('rosnode kill visual_slam', shell=True)
                # subprocess.call('pkill Stereo', shell=True)
                # time.sleep(SleepTime)
                subprocess.call('rosnode kill msf_pose_sensor', shell=True)
                subprocess.call('rosnode kill odom_converter', shell=True)
                subprocess.call('rosnode kill visual_robot_publisher', shell=True)
                # subprocess.call('rosnode kill turtlebot_controller', shell=True)
                subprocess.call('rosnode kill depth_global_follower', shell=True)
                subprocess.call('rosnode kill odom_reset', shell=True)
                subprocess.call('pkill rostopic', shell=True)
                subprocess.call('pkill -f trajectory_controller_node', shell=True)
                