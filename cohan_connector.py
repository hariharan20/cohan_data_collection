#!/usr/bin/python
import rospy
from cohan_msgs.msg import TrackedAgent , TrackedAgents , TrackedSegment ,TrackedSegmentType , AgentType
from nav_msgs.msg import Odometry
import numpy as np
from my_connector import my_connector
from multiverse_client_py import MultiverseClient , MultiverseMetaData


def euler_to_quat(theta) : 
    pass
def quat_to_euler(quat):
    pass

class cohan_mv_connector:
    def __init__(self , connector)  :
        self.agent = TrackedAgent()
        self.agent.track_id = 1 
        self.agent.name = "human1"
        self.agent_previous_pose = [0 , 0 , 0]
        self.multiverse_dt = 0.1
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
        self.tracked_agents_pub = rospy.Publisher('/tracked_agents' , TrackedAgents , queue_size=10)
        rospy.Timer(rospy.Duration(self.multiverse_dt) , self.publishAgents)

    def get_human_position(self ):
        sim_time = self.connector.sim_time
        self.connector.send_data = [sim_time]
        print(self.connector.send_and_receive_data())
        human_x = None 
        human_y = None 
        human_theta = None 
        return [human_x , human_y , human_theta]

    def publishAgents(self, _ ):
        self.agents = TrackedAgents()
        self.segment = TrackedSegment()
        self.segment.type = TrackedSegmentType.TORSO

        self.agents.header.stamp = rospy.Time.now()
        self.agents.header.frame_id = "map"
        self.agents.agents.append(self.agent) 
        human_current_pose = self.get_human_position()
        human_vel = (np.array(human_current_pose) - np.array(self.agent_previous_pose))/self.multiverse_dt
        self.agent_previous_pose = human_current_pose
        self.segment.pose.pose.position.x = human_current_pose[0]
        self.segment.pose.pose.position.y = human_current_pose[1]
        self.segment.pose.pose.orientation.z , self.segment.pose.pose.orientation.w = euler_to_quat(human_current_pose[2])
        self.segment.twist.twist.linear.x = human_vel[0]
        self.segment.twist.twist.linear.y = human_vel[1]
        self.segment.twist.twist.angular.z = human_vel[2]        
        self.agent.segments.append(self.segment)

if __name__ == "__main__"  :
    rospy.init_node('Multiverse_CoHAN_Connector_Node')
    obj = cohan_mv_connector(my_connector)    
    rospy.spin()