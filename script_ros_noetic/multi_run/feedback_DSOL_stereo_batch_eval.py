#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@file feedback_DSOL_stereo_batch_eval.py
@author Yanwei Du (duyanwei0702@gmail.com)
@date 01-26-2023
@version 1.0
@license Copyright (c) 2023
@desc None
"""

# This script is to run all the experiments in one program

import os
import subprocess
import time
import signal
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.parent.resolve()

SeqNameList = ["loop", "long", "square", "zigzag", "two_circle", "infinite"]
SeqLengList = [40, 50, 105, 125, 200, 245]

# SeqNameList.reverse()
# SeqLengList.reverse()

# SeqNameList = ["square", "two_circle", "infinite"]
# SeqLengList = [105, 200, 245]


# IMU (low + high)
IMUS = ["mpu6000", "ADIS16448"]
# IMUS = ['ADIS16448']

Fwd_Vel_List = [0.5, 1.0, 1.5]

# @NOTE (yanwei) DSOL uses cell_size instead of feature number, i.e. num_gf = (im.cols / cell_size) * (im.rows / cell_size)
Number_GF_List = [1000]
GF_To_GridCell = {600: "24", 1000: "19"}

Num_Repeating = 2  # 50 # 10 #
Num_Looping = 5  # 50 # 10 #

SleepTime = 2  # 5 #
# Duration = 30 # 60

# on/off flag of DSOL visualization
do_vis = str(0)

# NOTE adjust the path according to your catkin workspace !!!
# RESULT_ROOT = "/mnt/DATA/experiments/good_graph/closedloop/12700k/multi_run/"
RESULT_ROOT = "/local/data/roboslam/experiments/good_graph/closed_loop/xeon/multi_run"
METHOD_NAME = "DSOL"
ENABLE_ROSBAG_LOGGING = True

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
                    cmd_slam = (
                        "roslaunch ../launch/gazebo_DSOL_stereo.launch"
                        + " save:="
                        + path_track_logging
                        + " cell_size:="
                        + GF_To_GridCell[num_gf]
                        + " slam_pose_topic:="
                        + "/ORB_SLAM/camera_pose_in_imu"
                    )

                    cmd_esti = str(
                        "roslaunch msf_updates gazebo_msf_stereo.launch"
                        + " imu_type:="
                        + IMU_Type
                        + " "
                        + " topic_slam_pose:=/ORB_SLAM/camera_pose_in_imu  "
                        + " link_slam_base:=left_camera_frame"
                    )
                    cmd_ctrl = str(
                        "roslaunch ../launch/gazebo_controller.launch" + " compensate_planning_time:=" + "true"
                    )
                    cmd_plan = str(
                        "roslaunch ../launch/gazebo_offline_planning.launch"
                        + " path_type:="
                        + path_type
                        + " velocity_fwd:="
                        + velocity_fwd
                        + " duration:="
                        + str(duration)
                    )
                    cmd_log = str("roslaunch ../launch/gazebo_logging.launch path_data_logging:=" + path_track_logging)
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

                    # Duration = duration + SleepTime
                    Duration = duration * 1.5
                    print(bcolors.OKGREEN + "Start simulation with " + str(Duration) + " secs" + bcolors.ENDC)
                    # proc_trig = subprocess.call(cmd_trig, shell=True)
                    subprocess.Popen(cmd_trig, shell=True)

                    time.sleep(Duration)
                    for loop_idx in range(1, Num_Looping):
                        subprocess.call("rosnode kill turtlebot_controller", shell=True)
                        subprocess.call("rosnode kill turtlebot_trajectory_testing", shell=True)
                        time.sleep(SleepTime)

                        # Drive the robot back to start point.
                        print("Drive the robot back to start point.")
                        cmd_simple_controller = f"python {SCRIPT_DIR}/simple_controller.py"
                        print(cmd_simple_controller)
                        subprocess.call(cmd_simple_controller, shell=True)  # Wait until it is done.
                        print("Finished.")
                        time.sleep(SleepTime)

                        print(bcolors.OKGREEN + f"Start Loop {loop_idx} ... " + bcolors.ENDC)
                        print(bcolors.OKGREEN + "Launching Controller" + bcolors.ENDC)
                        subprocess.Popen(cmd_ctrl, shell=True)
                        print(bcolors.OKGREEN + "Launching Planner" + bcolors.ENDC)
                        subprocess.Popen(cmd_plan, shell=True)
                        time.sleep(SleepTime * 3)
                        subprocess.Popen(cmd_trig, shell=True)
                        time.sleep(Duration)

                    print(bcolors.OKGREEN + "Finish simulation, kill the process" + bcolors.ENDC)
                    subprocess.call("rosnode kill data_logging", shell=True)
                    time.sleep(SleepTime)
                    subprocess.call("rosnode kill dsol_odom", shell=True)
                    time.sleep(SleepTime)
                    subprocess.call("pkill dsol", shell=True)
                    subprocess.call("rosnode kill msf_pose_sensor", shell=True)
                    subprocess.call("rosnode kill odom_converter", shell=True)
                    subprocess.call("rosnode kill visual_robot_publisher", shell=True)
                    subprocess.call("rosnode kill turtlebot_controller", shell=True)
                    subprocess.call("rosnode kill turtlebot_trajectory_testing", shell=True)
                    subprocess.call("rosnode kill odom_reset", shell=True)
                    subprocess.call("pkill rostopic", shell=True)
                    subprocess.call("pkill -f trajectory_controller_node", shell=True)
