#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@file h_test.py
@author Yanwei Du (yanwei.du@gatech.edu)
@date 02-06-2025
@version 1.0
@license Copyright (c) 2025
@desc None
"""

# H-TEST
# The script aims to launch slam methods for the hessian conditioning testings.

import os
import subprocess
import time
import signal
from dataclasses import dataclass
from pathlib import Path

from slam_methods import (
    DsolNode,
)


SCRIPT_DIR = Path(__file__).parent.parent.resolve()
PKG_DIR = SCRIPT_DIR.parent.resolve()
PKG_DIR_STR = str(PKG_DIR)


@dataclass
class SeqMetaData:
    name: str
    length: float


SEQUENCES = [
    SeqMetaData("loop", 40),
    SeqMetaData("long", 50),
    SeqMetaData("square", 105),
    SeqMetaData("zigzag", 125),
    SeqMetaData("two_circle", 200),
    SeqMetaData("infinite", 245),
]

IMUS = ["mpu6000"]  # , "ADIS16448"]  # (low + high)

# desired forward velocity (m/s)
VELS = [0.5]  # , 1.0, 1.5]  #

# repeat times for simulation
ROUNDS = 1  # 50 # 10 #

# initialization period for eth_msf
SLEEP_TIME = 3  # 5 #
# Duration = 30 # 60

# NOTE adjust the path according to your catkin workspace !!!
RESULT_ROOT = "/mnt/DATA/experiments/msf/h_test/"
METHODS = ["dsol"]
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


imu_name = IMUS[0]
vel = VELS[0]
vel_str = str(vel)

for method_name in METHODS:
    method_dir = Path(RESULT_ROOT) / method_name
    for seq in SEQUENCES:
        seq_dir = method_dir / seq.name
        seq_dir.mkdir(exist_ok=True, parents=True)
        for round_idx in range(1, ROUNDS + 1):

            print(bcolors.ALERT + "====================================================================" + bcolors.ENDC)
            print(bcolors.ALERT + "Round: " + str(round_idx) + "; Seq: " + seq.name)
            path_track_logging = str(seq_dir / f"round{round_idx}")
            duration = float(seq.length) / vel + SLEEP_TIME

            # slam node
            slam_node = None
            if "dsol" == method_name:
                slam_node = DsolNode({"path_track_logging": path_track_logging})

            cmd_reset = str(
                "python reset_turtlebot_pose.py && rostopic pub -1 /mobile_base/commands/reset_odometry std_msgs/Empty '{}'"
            )
            # cmd_reset = str('rosservice call /gazebo/reset_simulation "{}"')
            cmd_gt_slam = str("roslaunch delayed_odometry demo_delay.launch" + " delay:=0.0" + " rate:=30")
            cmd_esti = str(
                "roslaunch msf_updates gazebo_msf_demo.launch"
                + " imu_type:="
                + imu_name
                + " "
                + " topic_slam_pose:=delayed_pose "
                + " link_slam_base:=base_footprint"
            )
            cmd_ctrl = str(
                f"roslaunch {PKG_DIR_STR}/launch/gazebo_controller.launch" + " compensate_planning_time:=" + "true"
            )
            cmd_plan = str(
                f"roslaunch {PKG_DIR_STR}/launch/gazebo_offline_planning.launch"
                + " path_type:="
                + seq.name
                + " velocity_fwd:="
                + vel_str
                + " duration:="
                + str(duration)
            )
            cmd_log = str(
                f"roslaunch {PKG_DIR_STR}/launch/gazebo_logging.launch path_data_logging:=" + path_track_logging
            )
            cmd_trig = str(
                "rostopic pub -1 /mobile_base/events/button kobuki_msgs/ButtonEvent '{button: 0, state: 0}' "
            )

            print(bcolors.WARNING + "cmd_reset: \n" + cmd_reset + bcolors.ENDC)
            print(bcolors.WARNING + "cmd_slam: \n" + cmd_gt_slam + bcolors.ENDC)
            print(bcolors.WARNING + "cmd_esti: \n" + cmd_esti + bcolors.ENDC)
            print(bcolors.WARNING + "cmd_ctrl: \n" + cmd_ctrl + bcolors.ENDC)
            print(bcolors.WARNING + "cmd_plan: \n" + cmd_plan + bcolors.ENDC)
            print(bcolors.WARNING + "cmd_log: \n" + cmd_log + bcolors.ENDC)
            print(bcolors.WARNING + "cmd_trig: \n" + cmd_trig + bcolors.ENDC)

            print(bcolors.OKGREEN + "Reset simulation" + bcolors.ENDC)
            subprocess.Popen(cmd_reset, shell=True)

            print(bcolors.OKGREEN + "Sleeping for a few secs to reset gazebo" + bcolors.ENDC)
            time.sleep(SLEEP_TIME)
            # time.sleep(60)

            # Launch slam
            if slam_node is None:
                print("Wrong SLAM Node")
                exit(-1)
            slam_node.start()
            time.sleep(SLEEP_TIME)

            print(bcolors.OKGREEN + "Launching GT SLAM" + bcolors.ENDC)
            subprocess.Popen(cmd_gt_slam, shell=True)
            time.sleep(SLEEP_TIME)  # wait SLAM to initialize

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
            time.sleep(SLEEP_TIME * 3)

            Duration = duration + SLEEP_TIME
            print(bcolors.OKGREEN + "Start simulation with " + str(Duration) + " secs" + bcolors.ENDC)
            # proc_trig = subprocess.call(cmd_trig, shell=True)
            subprocess.Popen(cmd_trig, shell=True)

            time.sleep(Duration)

            print(bcolors.OKGREEN + "Finish simulation, kill the process" + bcolors.ENDC)
            subprocess.call("rosnode kill data_logging", shell=True)
            time.sleep(SLEEP_TIME)
            slam_node.stop()
            subprocess.call("rosnode kill odometry_delayer", shell=True)
            # time.sleep(SleepTime)
            subprocess.call("rosnode kill msf_pose_sensor", shell=True)
            subprocess.call("rosnode kill odom_converter", shell=True)
            subprocess.call("rosnode kill visual_robot_publisher", shell=True)
            subprocess.call("rosnode kill turtlebot_controller", shell=True)
            subprocess.call("rosnode kill turtlebot_trajectory_testing", shell=True)
            subprocess.call("rosnode kill odom_reset", shell=True)
            subprocess.call("pkill rostopic", shell=True)
            subprocess.call("pkill -f trajectory_controller_node", shell=True)
