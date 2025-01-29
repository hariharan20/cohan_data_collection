from multiverse_client_py import MultiverseClient, MultiverseMetaData
import rospy
from geometry_msgs.msg import Pose
import math
from scipy.spatial.transform import Rotation
class MyConnector(MultiverseClient):
    def __init__(self, port: str, multiverse_meta_data: MultiverseMetaData) -> None:
        super().__init__(port, multiverse_meta_data)

    def loginfo(self, message: str) -> None:
        print(f"INFO: {message}")

    def logwarn(self, message: str) -> None:
        print(f"WARN: {message}")

    def _run(self) -> None:
        self.loginfo("Start running the client.")
        self._connect_and_start()

    def send_and_receive_meta_data(self) -> None:
        self.loginfo("Sending request meta data: " + str(self.request_meta_data))
        self._communicate(True)
        self.loginfo("Received response meta data: " + str(self.response_meta_data))
        # print(self.response_meta_data)

    def send_and_receive_data(self) -> None:
        self.loginfo("Sending data: " + str(self.send_data))
        self._communicate(False)
        self.loginfo("Received data: " + str(self.receive_data))
        

class ros_publiser:
    def __init__(self , connector ):
        self.connector = connector
        self.human_pose_msg = Pose()
        self.pub = rospy.Publisher('human_pose_from_unreal'  , Pose , queue_size = 10)
        print('initialization complete')
        
    def unreal_sub(self):

        self.connector.request_meta_data["send"] = {}
        self.connector.request_meta_data["receive"] = {}
        self.connector.request_meta_data["receive"]["PlayerPawn"] = [
        "position",
        "quaternion"
        ]
        self.connector.send_and_receive_meta_data()

        sim_time = self.connector.sim_time # The current simulation time
        self.connector.send_data = [sim_time]
        # self.connector.send_and_receive_data()
        human_pose = self.connector.send_and_receive_data()
        print(human_pose)
        self.human_pose_msg.position.x = human_pose[1]
        self.human_pose_msg.position.x = human_pose[1]
        self.human_pose_msg.position.x = human_pose[1]
        self.human_pose_msg.position.x = human_pose[1]
        self.human_pose_msg.position.x = human_pose[1]
        self.human_pose_msg.position.x = human_pose[1]
        self.human_pose_msg.position.x = human_pose[1]
        self.pub.publish(self.human_pose_msg)    

if __name__ == "__main__":
    multiverse_meta_data = MultiverseMetaData(
        world_name="world",
        simulation_name="my_simulation",
        length_unit="m",
        angle_unit="rad",
        mass_unit="kg",
        time_unit="s",
        handedness="rhs",
    )
    my_connector = MyConnector(port="5000",
                               multiverse_meta_data=multiverse_meta_data)
    my_connector.run()

    # my_connector.request_meta_data["send"] = {}
    # my_connector.request_meta_data["send"]["PlayerPawn"] = [
    #     "position",
    #     "quaternion"
    # ]
    # my_connector.send_and_receive_meta_data()

    # sim_time = my_connector.sim_time # The current simulation time
    # my_object_pos = [1.0, 2.0, 3.0]
    # my_object_quat = [0.0, 0.0, 0.0, 1.0]

    # my_connector.send_data = [sim_time] #+ my_object_pos + my_object_quat # The send_data to the correct order
    # my_connector.send_and_receive_data()

    # Change the request meta data to receive the position and quaternion of my_object

    my_connector.request_meta_data["send"] = {}
    # my_connector.request_meta_data["send"] = {}
    my_connector.request_meta_data["send"]["PR2"] = [
        "position",
        "quaternion"
    ]
    my_connector.send_and_receive_meta_data()
    sim_time = my_connector.sim_time # The current simulation time
    my_object_pos = [1.0, 2.0, 3.0]
    my_object_quat = [0.0, 0.0, 0.0, 1.0]

    my_connector.send_data = [sim_time] + my_object_pos + my_object_quat
    my_connector.send_and_receive_data()
    my_connector.request_meta_data["send"] = {}
    my_connector.request_meta_data["receive"] = {}
    my_connector.request_meta_data["receive"]["PlayerPawn"] = [
        "position",
        "quaternion"
    ]
    
    my_connector.send_and_receive_meta_data()
    while True : 
        sim_time = my_connector.sim_time
        my_connector.send_data = [sim_time]
        my_connector.send_and_receive_data()

    # my_connector.request_meta_data["receive"][""] = [""]
    # my_connector.send_and_receive_meta_data()

    # sim_time = my_connector.sim_time # The current simulation time
    # my_connector.send_data = [sim_time]
    # my_connector.send_and_receive_data()

    my_connector.stop()