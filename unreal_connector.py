#!/usr/bin/python
import rospy
from nav_msgs.msg import Odometry
from my_connector_2 import my_connector_sender

class unreal_connector:
    def __init__(self , connector) :
        self.connector = connector
        self.connecotr.request_meta_data["send"] = {}
        self.connector.request_meta_data["send"]["PR2"] = [
            "position",
            "orientation"
        ]
        self.connector.send_and_receive_meta_data()
        sim_time = self.my_connector.sim_time
        self.connector.send_data = [sim_time] + [0.0 , 0.0 , 0.0] + [0.0 , 0.0 , 0.0 ,1.0]
        self.connector.send_and_receive_data()
        self.connector.request_meta_data["send"] = {}
        self.connector.request_meta_data["receive"] = {}
        self.connector.request_meta_data["receive"]["PlayerPawn"] = [
            "position",
            "quaternion"
        ]
        
        self.connector.send_and_receive_meta_data()
        rospy.Subscriber('/base_pose_ground_truth' , Odometry , self.roboCB)
    
    def roboCB(self, data:Odometry):
        obj_pos = [data.pose.pose.position.x , data.pose.pose.position.y , data.pose.pose.position.z]
        obj_quat = [data.pose.orientation.x , data.pose.orientation.y , data.pose.orientation.z , data.pose.orientation.w] 
        self.connector.send_data = [self.connector.sim_time] + obj_pos  + obj_quat
        print('sending data')
        self.connector.send_and_receive_data()


if __name__ == "__main__":
    rospy.init_node('unreal_connector_node_pr2')
    obj = unreal_connector(my_connector_sender)
    rospy.spin()