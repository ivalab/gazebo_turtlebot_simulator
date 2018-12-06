# This script is to run svo in seperate terminal

import os
import subprocess
import time
import signal
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        prog = 'call_svo.py',
        description='Call SVO at a seperate terminal.')
    parser.add_argument('-f', type=int, help='number of features in SVO', 
        default = None, metavar = "num_feature")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    # print args

    cmd_install = str('cd ~/svo_install_ws && source /opt/ros/kinetic/setup.bash && source ~/svo_install_ws/install/setup.bash')
    cmd_source  = str('cd ~/svo_install_overlay_ws && source ~/svo_install_overlay_ws/devel/setup.bash')
    cmd_slam    = str('LD_PRELOAD=~/svo_install_ws/install/lib/libgflags.so.2.2.1 roslaunch svo_ros ' + 'gazebo_stereo_imu_lmk' + str(args.f) + '.launch')
    # print cmd_install
    # print cmd_source
    # print cmd_slam

    cmd_full = cmd_install + ' && ' + cmd_source + ' && ' + cmd_slam
    print cmd_full

    subprocess.call('bash -lic ' + '"' + cmd_full + '"', shell=True)

