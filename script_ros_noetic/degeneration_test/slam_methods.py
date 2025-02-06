#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@file slam_methods.py
@author Yanwei Du (yanwei.du@gatech.edu)
@date 02-06-2025
@version 1.0
@license Copyright (c) 2025
@desc None
"""

import subprocess
import time
from abc import ABC, abstractmethod
from typing import Dict
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
PKG_DIR = Path(__file__).parent.parent.parent.resolve()


class NodeBase(ABC):
    def __init__(self, name: str, label: str, nodes: list, params: Dict):
        self._name = name
        self._label = label
        self._nodes = nodes
        self._params = params
        assert len(self._nodes) > 0
        assert self._params

    def name(self) -> str:
        return self._name

    def label(self) -> str:
        return self._label

    def nodes(self) -> list:
        return self._nodes

    def start(self) -> bool:
        cmd = self.compose_start_cmd()
        assert cmd
        print(cmd)
        subprocess.Popen(cmd, shell=True)
        return True

    def stop(self) -> bool:
        for node in self.nodes():
            subprocess.call("rosnode kill /" + node, shell=True)
            time.sleep(1)
        return True

    @abstractmethod
    def compose_start_cmd(self) -> str:
        return ""

    # @abstractmethod
    def reset(self) -> bool:
        return False


class DsolNode(NodeBase):
    """_summary_

    Args:
        NodeBase (_type_): _description_
    """

    def __init__(self, params: Dict):
        nodes = ["dsol_odom"]
        super().__init__("dsol", "DSOL", nodes, params)
        self._feature_num = 1000
        self._f2c = {600: "24", 1000: "19"}

    def compose_start_cmd(self) -> str:
        cmd = (
            f"roslaunch {PKG_DIR}/launch/gazebo_DSOL_stereo.launch"
            + " save:="
            + self._params["path_track_logging"]
            + " cell_size:="
            + self._f2c[self._feature_num]
            + " slam_pose_topic:="
            + "/ORB_SLAM/camera_pose_in_imu"
        )
        return cmd


# class GfggNode(NodeBase):
#     def __init__(self, params: Dict):
#         nodes = ["visual_slam", "Stereo"]
#         super().__init__("gfgg", "GF-GG", nodes, params)

#     def compose_start_cmd(self) -> str:
#         cmd = str(
#             "roslaunch ../launch/gazebo_GF_stereo.launch"
#             + " path_slam_config:="
#             + path_slam_config
#             + " num_good_feature:="
#             + num_good_feature
#             + " path_track_logging:="
#             + path_track_logging
#             + " path_map_logging:="
#             + path_map_logging
#             + " do_rectify:="
#             + do_rectify
#             + " do_vis:="
#             + do_vis
#         )
#         return cmd


# class SlamToolboxNode(NodeBase):
#     def __init__(self, params: Dict):
#         nodes = ["slam_toolbox"]
#         super().__init__("SlamToolbox", "SlamToolbox", nodes, params)

#     def compose_start_cmd(self) -> str:
#         return (
#             "roslaunch slam_toolbox nav_slam_test.launch mode:=mapping output_pose_topic:="
#             + self._params["et_pose_topic"]


# class Orb3Node(NodeBase):
#     def __init__(self, params: Dict):
#         nodes = ["visual_slam", "Stereo"]
#         super().__init__("ORB3", nodes, params)

#     def compose_start_cmd(self) -> str:
#         ROS_WS = os.path.join(os.environ["HOME"], "closedloop_ws")
#         TRACK_LOG_DIR = self._params["path_dir"]
#         cmd = (
#             "bash "
#             + str(SLAM_CONFIGS_PATH / "call_orb3.sh ")
#             + ROS_WS
#             + " "
#             + TRACK_LOG_DIR
#             + " "
#             + str(self._params["feature_num"])
#             + " "
#             + self._params["et_pose_topic"]
#         )
#         return cmd
