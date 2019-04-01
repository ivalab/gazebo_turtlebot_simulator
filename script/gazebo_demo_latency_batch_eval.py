# This script is to run all the experiments in one program

import os
import subprocess
import time
import signal

# SeqNameList = ['loop'];
# SeqLengList = [40];
SeqNameList = ['loop', 'long', 'square', 'zigzag', 'infinite', 'two_circle'];
SeqLengList = [40, 50, 105, 125, 245, 200];

# low IMU
IMU_Type = 'mpu6000';
# high IMU
# IMU_Type = 'ADIS16448';

Fwd_Vel_List = [0.5, 1.0, 1.5] # [0.5, 1.0]; # [0.5, 0.75, 1.0]; # 
Vis_Latency_List = [0, 0.03] # [0.06, 0.1]; # [0, 0.01, 0.03, 0.06, 0.1]; # [0.15, 0.2, 0.3]; # 

Num_Repeating = 5 # 50 # 10 # 

SleepTime = 3 # 5 # 
# Duration = 30 # 60

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

for li, vl in enumerate(Vis_Latency_List):

    Experiment_prefix = 'Latency_' + str(Vis_Latency_List[li])

    for vn, fv in enumerate(Fwd_Vel_List):
        for sn, sname in enumerate(SeqNameList):

            SeqName = SeqNameList[sn]
            Result_root = '/mnt/DATA/tmp/debug/' + SeqName + '/' + IMU_Type + '/ideal/'
            # Result_root = '/mnt/DATA/tmp/ClosedNav_gt/' + SeqName + '/' + IMU_Type + '/ideal/'
            # Result_root = '/mnt/DATA/tmp/ClosedNav/demo_v3/' + IMU_Type + '/'
            Experiment_dir = Result_root + Experiment_prefix + '_Vel' + str(fv)
            cmd_mkdir = 'mkdir -p ' + Experiment_dir
            subprocess.call(cmd_mkdir, shell=True)

            for iteration in range(0, Num_Repeating):
                
                print bcolors.ALERT + "====================================================================" + bcolors.ENDC
                print bcolors.ALERT + "Round: " + str(iteration + 1) + "; Seq: " + SeqName + "; Vel: " + str(fv)

                path_track_logging = Experiment_dir + '/round' + str(iteration + 1)
                path_type = SeqName
                velocity_fwd = str(fv)
                duration = float(SeqLengList[sn]) / float(fv) + SleepTime

                # cmd_mkdir = 'mkdir -p ' + path_track_logging
                # subprocess.call(cmd_mkdir, shell=True)
                # cmd_mkdir = 'mkdir -p ' + path_map_logging
                # subprocess.call(cmd_mkdir, shell=True)

                cmd_reset  = str("python reset_turtlebot_pose.py && rostopic pub -1 /mobile_base/commands/reset_odometry std_msgs/Empty '{}'") 
                # cmd_reset = str('rosservice call /gazebo/reset_simulation "{}"')
                # cmd_slam   = str('rosrun delayed_odometry odometry_delayer' \
                #     + ' _delay:=' + str(Vis_Latency_List[li]) \
                #     + ' _rate:=' + str(30))
                cmd_slam   = str('roslaunch delayed_odometry demo_delay.launch' \
                    + ' delay:=' + str(Vis_Latency_List[li]) \
                    + ' rate:=30')
                cmd_esti   = str('roslaunch msf_updates gazebo_msf_demo.launch' \
                    + ' imu_type:=' + IMU_Type + ' ' \
                    + ' topic_slam_pose:=delayed_pose ' \
                    + ' link_slam_base:=base_footprint' )
                # cmd_esti   = str('rosrun odometry_converter odom_converter ' \
                #     + ' pose_topic:=odom' \
                #     + ' odom_topic:=visual/odom ' \
                #     + ' pose_link:=base_footprint ' \
                #     + ' cam_link:=base_footprint' )
                cmd_ctrl   = str('roslaunch ../launch/gazebo_controller_logging.launch path_data_logging:=' + path_track_logging \
                    + ' path_type:=' + path_type \
                    + ' velocity_fwd:=' + velocity_fwd \
                    + ' duration:=' + str(duration) )
                cmd_trig   = str("rostopic pub -1 /mobile_base/events/button kobuki_msgs/ButtonEvent '{button: 0, state: 0}' ") 

                print bcolors.WARNING + "cmd_reset: \n" + cmd_reset + bcolors.ENDC
                print bcolors.WARNING + "cmd_slam: \n"  + cmd_slam  + bcolors.ENDC
                print bcolors.WARNING + "cmd_esti: \n"  + cmd_esti  + bcolors.ENDC
                print bcolors.WARNING + "cmd_ctrl: \n"  + cmd_ctrl  + bcolors.ENDC
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

                print bcolors.OKGREEN + "Launching Controller" + bcolors.ENDC
                subprocess.Popen(cmd_ctrl, shell=True)
                
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
                subprocess.call('rosnode kill odometry_delayer', shell=True)
                # subprocess.call('rosnode kill Stereo', shell=True)
                # subprocess.call('rosnode kill visual_slam', shell=True)
                # subprocess.call('pkill Stereo', shell=True)
                # time.sleep(SleepTime)
                subprocess.call('rosnode kill msf_pose_sensor', shell=True)
                subprocess.call('rosnode kill odom_converter', shell=True)
                subprocess.call('rosnode kill visual_robot_publisher', shell=True)
                subprocess.call('rosnode kill turtlebot_controller', shell=True)
                subprocess.call('rosnode kill turtlebot_trajectory_testing', shell=True)
                subprocess.call('rosnode kill odom_reset', shell=True)
                subprocess.call('pkill rostopic', shell=True)
                