#!/usr/bin/env python

# This script is check how to get the mavros msg from the px4

import sys
import rospy
import airsim
from rospkg import RosPack
from airsim_ros_pkgs.msg import ObjectPose, ObjectPoseArray
from geometry_msgs.msg import Pose
from gazebo_msgs.msg import ModelStates

package = RosPack()
package_path = package.get_path('airsim_ros_pkgs')

class Object_Pose:

    def __init__(self, ip=''):
        # Instatiate instance of the airsim
        # print(airsim.__file__)

        self.client = airsim.MultirotorClient(ip = ip)
        self.client.confirmConnection()
        object_regex = rospy.get_param("/object_pose/object_pose_list_regex")
        print(object_regex)
        self.object_list = self.client.simListSceneObjects(name_regex=object_regex)
        self.print_object_ids()

    def print_object_ids(self):
        count = 0
        for o in self.object_list:
            print(count, o)
            count += 1


    def get_object_pose(self, time, frame):
        object_pose_array = ModelStates()
        # object_pose_array.header.stamp = time
        # object_pose_array.header.frame_id = frame
        for o in self.object_list:
            pose = self.client.simGetObjectPose(o)
            object_pose = Pose()
            object_pose_array.name.append(o)
            object_pose.orientation.w = pose.orientation.w_val
            object_pose.orientation.x = pose.orientation.x_val
            object_pose.orientation.y = pose.orientation.y_val
            object_pose.orientation.z = pose.orientation.z_val
            object_pose.position.x = pose.position.x_val
            object_pose.position.y = pose.position.y_val
            object_pose.position.z = pose.position.z_val
            object_pose_array.pose.append(object_pose)
            # object_pose_array.objects.append(object_pose)
        return object_pose_array

def main(args):
    rospy.init_node("object_pose_node")
    client_ip = rospy.get_param('~client_ip', '')
    obj = Object_Pose(client_ip)

    object_pose_pub = rospy.Publisher('/airsim_node/sim_object_poses_array', ModelStates, queue_size=10)
    rate = rospy.Rate(10)
    time = rospy.Time()
    frame = "local_ned"
    while not rospy.is_shutdown():
        time = rospy.Time()
        frame = "local_ned"
        object_pose_pub.publish(obj.get_object_pose(time, frame))
        rate.sleep()


if __name__ == '__main__':
    main(sys.argv)


