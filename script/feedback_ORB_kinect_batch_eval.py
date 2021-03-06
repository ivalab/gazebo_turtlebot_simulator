# This script is to run all the experiments in one program

import os
import subprocess
import time
import signal

# SeqNameList = ['line', 'turn', 'loop', 'long'];
# SeqLengList = [17, 20, 40, 50];
SeqNameList = ['loop', 'long'];
SeqLengList = [40, 50];

Fwd_Vel_List = [0.5, 1.0]; # [0.5, 0.75, 1.0]; # 
# Number_GF_List = [600, 1200]; # 
Number_GF_List = [80, 120, 160];

Num_Repeating = 10 # 3 # 5 # 50 # 

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


for ri, num_gf in enumerate(Number_GF_List):

    Experiment_prefix = 'ObsNumber_' + str(int(num_gf))

    for vn, fv in enumerate(Fwd_Vel_List):
        for sn, sname in enumerate(SeqNameList):

            SeqName = SeqNameList[sn]


            # NOTE adjust the path according to your working environment !!!
            Result_root = '/mnt/DATA/tmp/ClosedNav/debug/' 
            # Result_root = '/mnt/DATA/tmp/ClosedNav_new/RGBD/' + SeqName + '/low_imu/ORB/'
            
            Experiment_dir = Result_root + Experiment_prefix + '_Vel' + str(fv)
            cmd_mkdir = 'mkdir -p ' + Experiment_dir
            subprocess.call(cmd_mkdir, shell=True)

            for iteration in range(0, Num_Repeating):
                
                print bcolors.ALERT + "====================================================================" + bcolors.ENDC
                print bcolors.ALERT + "Round: " + str(iteration + 1) + "; Seq: " + SeqName + "; Vel: " + str(fv)

                path_data_logging = Experiment_dir + '/round' + str(iteration + 1)
                num_all_feature = str(num_gf*2)
                num_good_feature = str(num_gf*3)
                path_type = SeqName
                velocity_fwd = str(fv)
                duration = float(SeqLengList[sn]) / float(fv)

                cmd_reset  = str('rosservice call /gazebo/reset_simulation') 
                cmd_esti   = str('roslaunch msf_updates gazebo_ORB_kinect.launch' \
                    + ' num_all_feature:=' + num_all_feature \
                    + ' num_good_feature:=' + num_good_feature \
                    + ' path_data_logging:=' + path_data_logging)
                cmd_ctrl   = str('roslaunch ../launch/gazebo_controller.launch')
                cmd_plan   = str('roslaunch ../launch/gazebo_offline_planning.launch' \
                    + ' path_type:=' + path_type \
                    + ' velocity_fwd:=' + velocity_fwd \
                    + ' duration:=' + str(duration) )
                cmd_log   = str('roslaunch ../launch/gazebo_logging.launch path_data_logging:=' + path_track_logging )
                cmd_trig   = str("rostopic pub /mobile_base/events/button kobuki_msgs/ButtonEvent '{button: 0, state: 0}' ") 

                print bcolors.WARNING + "cmd_reset: \n" + cmd_reset + bcolors.ENDC
                print bcolors.WARNING + "cmd_esti: \n"  + cmd_esti  + bcolors.ENDC
                print bcolors.WARNING + "cmd_ctrl: \n"  + cmd_ctrl  + bcolors.ENDC
                print bcolors.WARNING + "cmd_plan: \n"  + cmd_plan  + bcolors.ENDC
                print bcolors.WARNING + "cmd_log: \n"   + cmd_log  + bcolors.ENDC
                print bcolors.WARNING + "cmd_trig: \n"  + cmd_trig  + bcolors.ENDC

                print bcolors.OKGREEN + "Reset simulation" + bcolors.ENDC
                proc_rst = subprocess.Popen(cmd_reset, shell=True)

                print bcolors.OKGREEN + "Sleeping for a few secs to reset gazebo" + bcolors.ENDC
                time.sleep(SleepTime)

                print bcolors.OKGREEN + "Launching State Estimator" + bcolors.ENDC
                proc_esti = subprocess.Popen(cmd_esti, shell=True)

                print bcolors.OKGREEN + "Sleeping for a few secs to stabilize msf" + bcolors.ENDC
                time.sleep(SleepTime)

                print bcolors.OKGREEN + "Launching Controller" + bcolors.ENDC
                subprocess.Popen(cmd_ctrl, shell=True)

                print bcolors.OKGREEN + "Launching Planner" + bcolors.ENDC
                subprocess.Popen(cmd_plan, shell=True)

                print bcolors.OKGREEN + "Launching Logger" + bcolors.ENDC
                subprocess.Popen(cmd_log, shell=True)

                time.sleep(SleepTime)
                
                Duration = duration + SleepTime
                print bcolors.OKGREEN + "Start simulation with " + str(Duration) + " secs" + bcolors.ENDC
                # proc_trig = subprocess.call(cmd_trig, shell=True)
                proc_trig = subprocess.Popen(cmd_trig, shell=True)

                time.sleep(Duration)

                print bcolors.OKGREEN + "Finish simulation, kill the process" + bcolors.ENDC
                subprocess.call('rosnode kill data_logging', shell=True)
                time.sleep(SleepTime)
                subprocess.call('rosnode kill RGBD', shell=True)
                subprocess.call('rosnode kill visual_slam', shell=True)
                subprocess.call('pkill RGBD', shell=True)
                time.sleep(SleepTime)
                subprocess.call('rosnode kill imu_downsample', shell=True)
                subprocess.call('rosnode kill msf_pose_sensor', shell=True)
                subprocess.call('rosnode kill odom_converter', shell=True)
                subprocess.call('rosnode kill visual_robot_publisher', shell=True)
                subprocess.call('rosnode kill odom_downsample', shell=True)
                subprocess.call('rosnode kill turtlebot_controller', shell=True)
                subprocess.call('rosnode kill turtlebot_trajectory_testing', shell=True)
                subprocess.call('rosnode kill odom_reset', shell=True)
                
