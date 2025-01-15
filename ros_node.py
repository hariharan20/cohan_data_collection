import rospy
from geometry_msgs.msg import Twist
import math
import socket


class ros_node:
    def __init__(self , initial_x=0.0 , initial_y=0.0 , initial_theta=0.0  ):
        self.host = '127.0.0.1'
        self.sender_port = 5000
        self.ros_sender_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        self.ros_sender_socket.connect((self.host , self.sender_port))
        self.x = initial_x
        self.y = initial_y
        self.theta = initial_theta
        self.dt = 0.1
        rospy.Subscriber('/cmd_vel' , Twist , self.vel_cb)


    def vel_cb(self , data):
        delta_x = data.linear.x * (math.cos(self.theta) - data.linear.y * math.sin(self.theta)) *self.dt
        delta_y = data.linear.y * (math.sin(self.theta) - data.linear.y * math.cos(self.theta)) *self.dt
        delta_theta = data.angular.z *self.dt
        data.linear.x = data.linear.x + delta_x
        self.x = self.x + delta_x
        self.y = self.y + delta_y
        self.theta = self.theta + delta_theta
        pose_data = [self.x , self.y , self.theta]
        self.ros_sender_socket.send(pose_data.encode('utf-8'))
    
    
    

if __name__ == "__main__":
    rospy.init_node('vel_sub')
    obj = ros_node()
    rospy.spin()
    obj.ros_sender_socket.close()
