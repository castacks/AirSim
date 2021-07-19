#!/usr/bin/env python

# This script is check how to get the mavros msg from the px4

import sys
import rospy
import airsim
from rospkg import RosPack
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Pose
from nav_msgs.msg import Odometry
from gazebo_msgs.msg import ModelStates

package = RosPack()
package_path = package.get_path('airsim_ros_pkgs')

class Gazebo_Pose:

    def __init__(self, ip=''):

        # Instatiate instance of the airsim
        print(airsim.__file__)
        # print(airsim.MultirotorClient.__file__)

        self.client = airsim.MultirotorClient(ip = ip)
        self.client.confirmConnection()
        # self.client.enableApiControl(True)
        # Instantiate instance of the subscriber
        # rospy.init_node('test_mavros')
        self.FCU_sub = rospy.Subscriber('/gazebo/model_states', ModelStates, self.FCU_callback)
        # for p in sys.path:
        #     print(p)

        self.pose_info = "Initialising"
	rospy.spin()
	return

    def FCU_callback(self, msg):
        self.pose_info = msg.pose[2]
        # print ("Pose of the vehicle: ", self.pose_info)

        # Values of position and orientation in the gazebo environment
        #print("orientation_gazebo = ", self.pose_info.orientation)
        #print("position_gazebo = ", self.pose_info.position)
        #print("=================")
        # print("x_val pose ", self.pose_info.position.x)
        # print(testAPI)
        # print "=================="

        # Gazebo values of orientation x,y,x,w
        gazebo_ori_x = self.pose_info.orientation.x
        gazebo_ori_y = self.pose_info.orientation.y
        gazebo_ori_z = self.pose_info.orientation.z
        gazebo_ori_w = self.pose_info.orientation.w        

        # Gazebo values of position x,y,z
        gazebo_pos_x = self.pose_info.position.x
        gazebo_pos_y = self.pose_info.position.y
        gazebo_pos_z = self.pose_info.position.z


        # Get current pose of the airsim in order to manipulate it
        airsim_pose = self.client.simGetVehiclePose()

        # Set values of gazebo pose to airsim pose
        airsim_pose.orientation.x_val = gazebo_ori_x
        airsim_pose.orientation.y_val = -gazebo_ori_y
        airsim_pose.orientation.z_val = -gazebo_ori_z
        airsim_pose.orientation.w_val = gazebo_ori_w        

        # Gazebo values of position x,y,z
        airsim_pose.position.x_val = gazebo_pos_x
        airsim_pose.position.y_val = -gazebo_pos_y
        airsim_pose.position.z_val = -(gazebo_pos_z)

        # print("airsim_pos ", airsim_pose)

        #print(airsim_pose)
        #print("====================")
        #print(airsim_pose.position.x_val)
        #print("-----0-0-0-0-0-0-0--")
        self.client.simSetVehiclePose(airsim_pose, True)
        # self.client.moveToPositionAsync(gazebo_pos_x, gazebo_pos_y, -gazebo_pos_z, 1).join()
        #print(self.pose_info.orientation)
        # Also while it gets the value of pose it can just update the vehilce pose in airsim
        #airsim_pose = self.client.simGetVehiclePose()
        #print("=================")
        #print(airsim_pose.orientation.x_val)
        #self.client.simSetVehiclePose(msg.pose, True)

def main(args):
    try:
	rospy.init_node("gazebo_pose_node")
	client_ip = rospy.get_param('~client_ip', '')
	sm = Gazebo_Pose(client_ip)
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == '__main__':
    main(sys.argv)


