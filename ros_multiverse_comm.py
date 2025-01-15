import rospy
import json
from geometry_msgs.msg import Pose
import socket

class ros_comm():
    def __init__(self):
        self.ip = '127.0.0.1'
        self.server_port = '9000'
        self.client_port = '8000'
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip , self.server_port))
        self.position = [0.0 , 0.0 , 0.0]
        self.quaternion = [0.0 , 0.0 , 0.0 , 1]
        self.msg_dict = {'world':{'PR2':{'position': self.position, 'quaternion':self.quaternion}}}
        rospy.Subscriber('/pr2_pose' , Pose , self.pose_cb)
    def pose_cb(self , pose):
        self.msg_dict['position'] = [pose.position.x , pose.position.y , pose.position.z]
        self.msg_dict['quaternion'] = [pose.orientation.x , pose.orientation.y , pose.orientation.z , pose.orientation.w]
        json_string = json.dump(self.msg_dict)
        encoded_string = str.encode(json_string)
        self.sock.send(encoded_string)
        data = self.sock.recv(1024)
    

if __name__=="__main__":
    rospy.init_node('tcp_comm_node')
    obj = ros_comm()
    rospy.spin()