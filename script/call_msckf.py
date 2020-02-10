# This script is to run svo in seperate terminal

import os
import subprocess
import time
import signal
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        prog = 'call_msckf.py',
        description='Call MSCKF at a seperate terminal.')
    parser.add_argument('-f', type=int, help='number of features in MSCKF', 
        default = None, metavar = "num_feature")
    parser.add_argument('-i', type=str, help='Type of IMU used', 
        default = None, metavar = "imu_type")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    # print args

    # e.g. msckf_vio_gazebo_lmk120_mpu6000.launch
    cmd_source  = str('cd ~/catkin_ws && source ~/catkin_ws/devel/setup.bash')
    cmd_slam    = str('roslaunch msckf_vio ' + 'msckf_vio_gazebo_lmk' + str(args.f) + '_' + args.i + '.launch')
    # print cmd_source
    # print cmd_slam

    cmd_full = cmd_source + ' && ' + cmd_slam
    print cmd_full

    subprocess.call('bash -lic ' + '"' + cmd_full + '"', shell=True)

