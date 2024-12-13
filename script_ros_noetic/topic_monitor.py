#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@file topic_monitor.py
@author Yanwei Du (yanwei.du@gatech.edu)
@date 01-02-2024
@version 1.0
@license Copyright (c) 2024
@desc None
'''

# https://robotics.stackexchange.com/questions/93488/how-to-check-whether-the-topic-is-publishing-msg

import rospy
import threading # Needed for Timer
from geometry_msgs.msg import PoseWithCovarianceStamped

rospy.init_node("topic_monitor")

def timeout():
    print("No message received for 5 seconds")
    # Do something

def callback(msg):
    global timer
    # print("Message received")
    timer.cancel()
    timer = threading.Timer(5,timeout)
    timer.start()
    # Do Other thing

rospy.Subscriber("/ORB_SLAM/camera_pose_in_imu", PoseWithCovarianceStamped, callback) # When receiving a message, call callback()
timer = threading.Timer(5,timeout) # If 5 seconds elapse, call timeout()
timer.start()

while not rospy.is_shutdown():
    #Do something else
    rospy.sleep(1)