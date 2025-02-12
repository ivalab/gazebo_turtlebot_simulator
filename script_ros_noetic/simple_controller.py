#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@file simple_controller.py
@author Yanwei Du (yanwei.du@gatech.edu)
@date 02-12-2025
@version 1.0
@license Copyright (c) 2025
@desc None
"""


#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import math
import cmath
import numpy as np


class SimpleController:
    def __init__(self, x=0.0, y=0.0, theta=0.0):
        # Initialize the ROS node
        rospy.init_node("simple_controller", anonymous=True)

        # Goal position (x, y, z, theta)
        self.goal_x = x
        self.goal_y = y
        self.goal_theta = theta  # in radians

        # Tolerance for reaching the goal
        self.position_tolerance = 0.1
        self.angle_tolerance = np.deg2rad(5.0)

        # Maximum velocities
        self.max_linear_velocity = 0.25  # m/s
        self.max_angular_velocity = 0.5  # rad/s
        self.k_drive_x = 1.0
        self.k_drive_y = 1.0
        self.k_turn = 1.0

        # Current robot position and orientation
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_theta = 0.0
        self.odom_update = False
        self.angle_tracking_only = True

        # Publisher for velocity commands
        self.cmd_vel_pub = rospy.Publisher("/cmd_vel_mux/input/navi", Twist, queue_size=10)

        # Subscriber for odometry
        self.odom_sub = rospy.Subscriber("/odom", Odometry, self.odom_callback)

    def odom_callback(self, msg):
        self.odom_update = True
        # Update current position and orientation
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y
        # Convert quaternion to Euler angle (yaw)
        orientation = msg.pose.pose.orientation
        siny_cosp = 2 * (orientation.w * orientation.z + orientation.x * orientation.y)
        cosy_cosp = 1 - 2 * (orientation.y * orientation.y + orientation.z * orientation.z)
        self.current_theta = math.atan2(siny_cosp, cosy_cosp)

    def distance_to_goal(self):
        # Calculate Euclidean distance to the goal
        return math.sqrt((self.goal_x - self.current_x) ** 2 + (self.goal_y - self.current_y) ** 2)

    def angle_to_position(self):
        # Calculate the angle to the goal
        delta_x = self.goal_x - self.current_x
        delta_y = self.goal_y - self.current_y
        angle_to_position = math.atan2(delta_y, delta_x) - self.current_theta

        # Normalize the angle to the range [-pi, pi]
        angle_to_position = math.atan2(math.sin(angle_to_position), math.cos(angle_to_position))

        return angle_to_position

    def orientation_to_goal(self):
        # Calculate the difference between the current orientation and the goal orientation
        angle_to_orientation = self.goal_theta - self.current_theta

        # Normalize the angle to the range [-pi, pi]
        angle_to_orientation = math.atan2(math.sin(angle_to_orientation), math.cos(angle_to_orientation))

        return angle_to_orientation

    def get_complex_matrix(self, x, y, quat_w, quat_z):
        # Create a complex number from the quaternion components
        phase = complex(quat_w, quat_z)
        phase = phase * phase  # Square the complex number

        # Create a 2x2 complex matrix
        g = np.zeros((2, 2), dtype=complex)

        # Fill the matrix with the appropriate values
        g[0, 1] = x
        g[1, 0] = 0
        g[1, 1] = 1

        g.imag[0, 1] = y
        g.imag[1, 0] = 0
        g.imag[1, 1] = 0

        # Set the (0,0) element to the squared phase
        g[0, 0] = phase

        return g

    def get_control_law(self):

        cur_x = self.current_x
        cur_y = self.current_y
        cur_theta = self.current_theta

        des_x = self.goal_x
        des_y = self.goal_y
        des_theta = self.goal_theta

        delta_x = des_x - cur_x
        delta_y = des_y - cur_y
        delta_theta = math.atan2(delta_y, delta_x)

        if self.angle_tracking_only:
            print("trackgin only angle")
            if abs(self.angle_to_position()) > self.angle_tolerance:
                des_x = cur_x
                des_y = cur_y
                des_theta = delta_theta
            else:
                self.angle_tracking_only = False
        elif self.distance_to_goal() > self.position_tolerance:
            print("trackgin distacne and angle")
            des_theta = delta_theta
        else:
            des_x = cur_x
            des_y = cur_y

        g_cur = self.get_complex_matrix(cur_x, cur_y, np.cos(cur_theta / 2.0), np.sin(cur_theta / 2.0))
        g_des = self.get_complex_matrix(des_x, des_y, np.cos(des_theta / 2.0), np.sin(des_theta / 2.0))
        g_err = np.linalg.inv(g_cur) @ g_des

        # Extract errors from g_error
        theta_err = cmath.phase(g_err[(0, 0)])  # Argument (angle) of the complex number at (0,0)
        x_err = g_err[(0, 1)].real  # Real part of the complex number at (0,1)
        y_err = g_err[(0, 1)].imag  # Imaginary part of the complex number at (0,1)

        # Feedback control signals
        v_ang_fb = theta_err * self.k_turn
        # v_lin_fb = x_err * self.k_drive_x + y_err * self.k_drive_y
        v_lin_fb = self.k_drive_x * math.sqrt(x_err * x_err + y_err * y_err)
        # print(v_lin_fb, v_ang_fb)

        v_lin_fb = min(self.max_linear_velocity, v_lin_fb)
        v_ang_fb = min(self.max_angular_velocity, v_ang_fb)
        v_ang_fb = max(-self.max_angular_velocity, v_ang_fb)

        return v_lin_fb, v_ang_fb

    def run(self):
        rate = rospy.Rate(10)  # 10 Hz

        while not rospy.is_shutdown():
            # Calculate distance and angles
            if not self.odom_update:
                rate.sleep()
                continue
            distance = self.distance_to_goal()
            angle = self.orientation_to_goal()

            # Check if the goal is reached
            if distance < self.position_tolerance and abs(angle) < self.angle_tolerance:
                rospy.loginfo("Goal reached! Shutting down.")
                self.stop_robot()
                rospy.signal_shutdown("Goal reached")
                break

            # Create a Twist message for velocity commands
            vx, wz = self.get_control_law()
            cmd_vel = Twist()
            cmd_vel.linear.x = vx
            cmd_vel.angular.z = wz

            # Publish the velocity command
            self.cmd_vel_pub.publish(cmd_vel)

            rate.sleep()

    def stop_robot(self):
        # Stop the robot by publishing zero velocities
        rate = rospy.Rate(10.0)
        count = 0
        while count < 10:
            cmd_vel = Twist()
            cmd_vel.linear.x = 0.0
            cmd_vel.angular.z = 0.0
            self.cmd_vel_pub.publish(cmd_vel)
            count += 1
            rate.sleep()


if __name__ == "__main__":
    try:
        x = 0
        y = 0
        theta = 0
        controller = SimpleController(x, y, theta)
        controller.run()
    except rospy.ROSInterruptException:
        pass
