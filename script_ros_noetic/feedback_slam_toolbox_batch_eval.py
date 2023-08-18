#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@file feedback_slam_toolbox_batch_eval.py
@author Yanwei Du (yanwei.du@gatech.edu)
@date 08-17-2023
@version 1.0
@license Copyright (c) 2023
@desc None
"""


# This script is to run all the experiments in one program

import os
import subprocess
import time
import signal

SeqNameList = ["line"]
SeqLengList = [14]

# IMU (low + high)
IMUS = ["mpu6000", "ADIS16448"]
# IMUS = ['ADIS16448']

Fwd_Vel_List = [0.5, 1.0, 1.5]

# # @NOTE (yanwei) DSOL uses cell_size instead of feature number, i.e. num_gf = (im.cols / cell_size) * (im.rows / cell_size)
Number_GF_List = [1000]
GF_To_GridCell = {600: "24", 1000: "19"}

Num_Repeating = 1  # 50 # 10 #

SleepTime = 2  # 5 #
# Duration = 30 # 60

# on/off flag of DSOL visualization
do_vis = str(0)

# NOTE adjust the path according to your catkin workspace !!!
RESULT_ROOT = "/mnt/DATA/Yanwei/closedloop/2023/20.04/"
METHOD_NAME = "SLAM_TOOLBOX"
ENABLE_ROSBAG_LOGGING = False

# To add after each roslaunch command, in order to avoid the boring warning messages.
POSTFIX = ""  # 2> >(grep -v TF_REPEATED_DATA buffer_core)"

# ----------------------------------------------------------------------------------------------------------------------


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    ALERT = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


for IMU_Type in IMUS:

    for ri, num_gf in enumerate(Number_GF_List):

        # for DSOL, it is really not a feature number
        Experiment_prefix = "ObsNumber_" + str(int(num_gf))

        for vn, fv in enumerate(Fwd_Vel_List):
            for sn, sname in enumerate(SeqNameList):

                SeqName = SeqNameList[sn]

                Result_root = os.path.join(RESULT_ROOT, SeqName, IMU_Type, METHOD_NAME)

                Experiment_dir = os.path.join(Result_root, Experiment_prefix + "_Vel" + str(fv))
                if os.path.exists(Experiment_dir):
                    cmd_rmdir = "rm -r " + Experiment_dir
                    # subprocess.call(cmd_rmdir, shell=True)
                cmd_mkdir = "mkdir -p " + Experiment_dir
                subprocess.call(cmd_mkdir, shell=True)

                for iteration in range(0, Num_Repeating):

                    print(
                        bcolors.ALERT
                        + "===================================================================="
                        + bcolors.ENDC
                    )
                    print(bcolors.ALERT + "Round: " + str(iteration + 1) + "; Seq: " + SeqName + "; Vel: " + str(fv))

                    path_track_logging = Experiment_dir + "/round" + str(iteration + 1)
                    path_type = SeqName
                    velocity_fwd = str(fv)
                    duration = float(SeqLengList[sn]) / float(fv) + SleepTime

                    cmd_reset = str(
                        "python reset_turtlebot_pose.py && rostopic pub -1 /mobile_base/commands/reset_odometry std_msgs/Empty '{}'"
                    )
                    # cmd_reset = str('rosservice call /gazebo/reset_simulation "{}"')

                    # !!! Parameters order matters !!! #
                    # Order defined in .sh file. #
                    cmd_slam = str(
                        "bash call_slam_toolbox.sh"
                        + " "
                        + do_vis
                        + " "
                        + path_track_logging
                        + " "
                        + GF_To_GridCell[num_gf]
                    )

                    cmd_esti = str(
                        "roslaunch msf_updates gazebo_msf_laser.launch"
                        + " imu_type:="
                        + IMU_Type
                        + " "
                        + " topic_slam_pose:=/scanmatch/pose"
                        + " link_slam_base:=base_footprint"
                    )
                    cmd_ctrl = str(
                        "roslaunch ../launch/gazebo_controller.launch"
                        + " compensate_planning_time:="
                        + "true"
                        + POSTFIX
                    )
                    cmd_plan = str(
                        "roslaunch ../launch/gazebo_offline_planning.launch"
                        + " path_type:="
                        + path_type
                        + " velocity_fwd:="
                        + velocity_fwd
                        + " duration:="
                        + str(duration)
                        + POSTFIX
                    )
                    cmd_log = str(
                        "roslaunch ../launch/gazebo_logging.launch path_data_logging:=" + path_track_logging + POSTFIX
                    )

                    cmd_trig = str(
                        "rostopic pub -1 /mobile_base/events/button kobuki_msgs/ButtonEvent '{button: 0, state: 0}' "
                    )

                    print(bcolors.WARNING + "cmd_reset: \n" + cmd_reset + bcolors.ENDC)
                    print(bcolors.WARNING + "cmd_slam: \n" + cmd_slam + bcolors.ENDC)
                    print(bcolors.WARNING + "cmd_esti: \n" + cmd_esti + bcolors.ENDC)
                    print(bcolors.WARNING + "cmd_ctrl: \n" + cmd_ctrl + bcolors.ENDC)
                    print(bcolors.WARNING + "cmd_plan: \n" + cmd_plan + bcolors.ENDC)
                    print(bcolors.WARNING + "cmd_log: \n" + cmd_log + bcolors.ENDC)
                    print(bcolors.WARNING + "cmd_trig: \n" + cmd_trig + bcolors.ENDC)

                    print(bcolors.OKGREEN + "Reset simulation" + bcolors.ENDC)
                    subprocess.Popen(cmd_reset, shell=True)

                    print(bcolors.OKGREEN + "Sleeping for a few secs to reset gazebo" + bcolors.ENDC)
                    time.sleep(SleepTime)
                    # time.sleep(60)

                    print(bcolors.OKGREEN + "Launching SLAM" + bcolors.ENDC)
                    subprocess.Popen(cmd_slam, shell=True)
                    time.sleep(SleepTime)  # wait SLAM to initialize
                    # subprocess.Popen(cmd_delayed, shell=True)

                    print(bcolors.OKGREEN + "Launching State Estimator" + bcolors.ENDC)
                    subprocess.Popen(cmd_esti, shell=True)

                    print(bcolors.OKGREEN + "Launching Controller" + bcolors.ENDC)
                    subprocess.Popen(cmd_ctrl, shell=True)

                    print(bcolors.OKGREEN + "Launching Planner" + bcolors.ENDC)
                    subprocess.Popen(cmd_plan, shell=True)

                    if ENABLE_ROSBAG_LOGGING:
                        print(bcolors.OKGREEN + "Launching Logger" + bcolors.ENDC)
                        subprocess.Popen(cmd_log, shell=True)

                    print(bcolors.OKGREEN + "Sleeping for a few secs to stabilize msf" + bcolors.ENDC)
                    time.sleep(SleepTime * 3)

                    Duration = duration + SleepTime
                    print(bcolors.OKGREEN + "Start simulation with " + str(Duration) + " secs" + bcolors.ENDC)
                    # proc_trig = subprocess.call(cmd_trig, shell=True)
                    subprocess.Popen(cmd_trig, shell=True)

                    time.sleep(Duration)

                    print(bcolors.OKGREEN + "Finish simulation, kill the process" + bcolors.ENDC)
                    subprocess.call("rosnode kill data_logging", shell=True)
                    time.sleep(SleepTime)
                    subprocess.call("rosnode kill slam_toolbox", shell=True)
                    time.sleep(SleepTime)
                    subprocess.call("rosnode kill msf_pose_sensor", shell=True)
                    subprocess.call("rosnode kill odom_converter", shell=True)
                    subprocess.call("rosnode kill visual_robot_publisher", shell=True)
                    subprocess.call("rosnode kill turtlebot_controller", shell=True)
                    subprocess.call("rosnode kill turtlebot_trajectory_testing", shell=True)
                    subprocess.call("rosnode kill odom_reset", shell=True)
                    subprocess.call("pkill rostopic", shell=True)
                    subprocess.call("pkill -f trajectory_controller_node", shell=True)
