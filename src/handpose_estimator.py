#!/usr/bin/env python

from easy_tcp_python2_3 import socket_utils as su
import cv2, cv_bridge
from sensor_msgs.msg import Image
import rospy
import numpy as np 



class HandPoseEstimator:

    def __init__(self):

        rospy.init_node("hand_pose_estimator")
        rospy.loginfo("Starting hand_pose_estimator.py node")
        self.cv_bridge = cv_bridge.CvBridge()

        self.sock,_ = su.initialize_server('localhost', 7776)
        rgb_sub = rospy.Subscriber('azure1/rgb/image_raw', Image, self.callback, queue_size=1, buff_size=2**24)
        self.result_pub = rospy.Publisher('/vis/hand_pose_img', Image, queue_size=1)

    def callback(self,rgb):

        rgb = self.cv_bridge.imgmsg_to_cv2(rgb,desired_encoding='bgr8')
        su.sendall_pickle(self.sock, rgb)
        rospy.loginfo_once('Sended an image to client')
        
        LHandJoint, RHandJoint = su.recvall_pickle(self.sock)
        print("LHandJoint", LHandJoint) # [21, 3] [img_x, img_y, z]
        print("RHandJoint", RHandJoint)
        hand_vis_img = su.recvall_image(self.sock) 
        rospy.loginfo_once('Received inference results from client')

        # visualization
        img_msg = self.cv_bridge.cv2_to_imgmsg(hand_vis_img, encoding='bgr8')
        self.result_pub.publish(img_msg)
        rospy.loginfo_once('Published the result as topic. Topic name : /estimation_result')


                    
if __name__ == '__main__':

    server = HandPoseEstimator()
    rospy.spin()