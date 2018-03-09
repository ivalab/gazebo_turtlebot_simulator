#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2016 Massachusetts Institute of Technology

"""Extract images from a rosbag.
"""

import os
import argparse
import numpy as np
from matplotlib import pyplot as plt

import cv2

import rosbag
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

def main():
    """Extract a folder of images from a rosbag.
    """
    parser = argparse.ArgumentParser(description="Extract images from a ROS bag.")
    parser.add_argument("input_bag", help="Input ROS bag.")
    parser.add_argument("output_bag", help="Output ROS bag.")
    parser.add_argument("image_topic_l", help="Left image topic.")
    parser.add_argument("image_topic_r", help="Right image topic.")

    args = parser.parse_args()

    # create filter
    kernel_size = 5 # 9
    kernel = np.ones((kernel_size,kernel_size),np.float32)/(kernel_size*kernel_size)

    bag_in = rosbag.Bag(args.input_bag, "r")
    bag_out = rosbag.Bag(args.output_bag, "w")
    bridge = CvBridge()

    print "Extract images from %s on topic %s into %s" % (args.input_bag,
                                                          args.image_topic_l, args.output_bag)

    count = 0
    for topic, msg, t in bag_in.read_messages(topics=[args.image_topic_l]):

        # grab image from input rosbag
        try:
            cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
        except CvBridgeError as e:
            print(e)
        rgb_img = cv_img[...,::-1]

        # seconds = t.to_sec() #floating point
        # print seconds
        nanoseconds = t.to_nsec()
        # print nanoseconds

        # apply filter to image
        filter_img = cv2.filter2D(rgb_img,-1,kernel)
        filter_img = cv2.flip(filter_img,1)

        # write message to output bag
        try:
            msg_out = bridge.cv2_to_imgmsg(filter_img, encoding="passthrough")
        except CvBridgeError as e:
            print(e)
        msg_out.header.stamp = t
        bag_out.write(args.image_topic_l, msg_out, t)

        # # viz
        # plt.subplot(121),plt.imshow(rgb_img),plt.title('Original')
        # plt.xticks([]), plt.yticks([])
        # plt.subplot(122),plt.imshow(filter_img),plt.title('Blurred')
        # plt.xticks([]), plt.yticks([])
        # plt.show()

        # cv2.imwrite(os.path.join(args.output_dir, "%019i.png" % nanoseconds), rgb_img)
        print "Wrote image %i" % count

        count += 1


    print "Extract images from %s on topic %s into %s" % (args.input_bag,
                                                          args.image_topic_r, args.output_bag)

    count = 0
    for topic, msg, t in bag_in.read_messages(topics=[args.image_topic_r]):

        # grab image from input rosbag
        try:
            cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
        except CvBridgeError as e:
            print(e)
        rgb_img = cv_img[...,::-1]

        # seconds = t.to_sec() #floating point
        # print seconds
        nanoseconds = t.to_nsec()
        # print nanoseconds

        # apply filter to image
        filter_img = cv2.filter2D(rgb_img,-1,kernel)
        filter_img = cv2.flip(filter_img,1)

        # write message to output bag
        try:
            msg_out = bridge.cv2_to_imgmsg(filter_img, encoding="passthrough")
        except CvBridgeError as e:
            print(e)
        msg_out.header.stamp = t
        bag_out.write(args.image_topic_r, msg_out, t)

        # # viz
        # plt.subplot(121),plt.imshow(rgb_img),plt.title('Original')
        # plt.xticks([]), plt.yticks([])
        # plt.subplot(122),plt.imshow(filter_img),plt.title('Blurred')
        # plt.xticks([]), plt.yticks([])
        # plt.show()

        # cv2.imwrite(os.path.join(args.output_dir, "%019i.png" % nanoseconds), rgb_img)
        print "Wrote image %i" % count

        count += 1


    bag_in.close()

    return

if __name__ == '__main__':
    main()