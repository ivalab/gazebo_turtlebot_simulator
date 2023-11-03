# This script is to run svo in seperate terminal

import os
import subprocess
import time
import signal
import argparse


def parse_args():
    parser = argparse.ArgumentParser(prog="call_vinsfusion.py", description="Call VINS-Fusion at a seperate terminal.")
    parser.add_argument("-f", type=int, help="number of features in VINS-Fusion", default=None, metavar="num_feature")
    parser.add_argument("-i", type=str, help="Type of IMU used", default=None, metavar="imu_type")
    parser.add_argument("-l", type=str, help="Logging director", default="/tmp", metavar="logging directory")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    # print args

    # e.g. gazebo-stereo_config_lmk240_mpu6000.yaml
    Config_Yaml = (
        "~/svo_ws/src/VINS-Fusion/config/gazebo/gazebo-stereo_config_lmk" + str(args.f) + "_" + args.i + ".yaml"
    )
    cmd_source = str("cd ~/svo_ws && source ~/svo_ws/devel/setup.bash")
    cmd_vinsrun = str(
        "rosrun vins vins_node " + Config_Yaml + " _output_prefix:=" + args.l + " _g_enable_closed_loop:=true"
    )
    cmd_looprun = str("rosrun loop_fusion loop_fusion_node " + Config_Yaml + " _output_prefix:=" + args.l)
    # print cmd_source
    # print cmd_slam

    cmd_full = cmd_source + " && " + cmd_vinsrun + " && " + cmd_looprun
    print(cmd_full)

    subprocess.call("bash -lic " + '"' + cmd_full + '"', shell=True)

