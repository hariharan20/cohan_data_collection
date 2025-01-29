from multiverse_client_py import MultiverseClient, MultiverseMetaData
import rospy
from geometry_msgs.msg import Twist
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

    def send_and_receive_data(self) -> None:
        self.loginfo("Sending data: " + str(self.send_data))
        self._communicate(False)
        self.loginfo("Received data: " + str(self.receive_data))

class ros_subscriber:
    def __init__(self , connector , initial_x=0.0 , initial_y=0.0 , initial_theta=0.0  ):
        self.x = initial_x
        self.y = initial_y
        self.theta = initial_theta
        self.dt = 0.1
        self.connector = connector
        print('initialization complete')
        rospy.Subscriber('/cmd_vel' , Twist , self.vel_cb)


    def vel_cb(self , data):
        print('data received')
        delta_x = data.linear.x * (math.cos(self.theta) - data.linear.y * math.sin(self.theta)) *self.dt
        delta_y = data.linear.y * (math.sin(self.theta) - data.linear.y * math.cos(self.theta)) *self.dt
        # delta_x = data.linear.x* self.dt
        # delta_y = data.linear.y* self.dt
        delta_theta = data.angular.z *self.dt
        data.linear.x = data.linear.x + delta_x
        self.x = self.x + delta_x
        self.y = self.y + delta_y
        self.theta = self.theta + delta_theta
        self.connector.request_meta_data["send"] = {}
        self.connector.request_meta_data["send"]["PR2"] = [
            "position",
            "quaternion"
        ]
        self.connector.send_and_receive_meta_data()

        sim_time = self.connector.sim_time # The current simulation time
        my_object_pos = [self.x , self.y, 0]
        self.theta_quat = Rotation.from_euler('x' , self.theta, degrees=False).as_quat()
        my_object_quat = [self.theta_quat[0], self.theta_quat[1],self.theta_quat[2], self.theta_quat[3]]
    
        self.connector.send_data = [sim_time] + my_object_pos + my_object_quat # The send_data to the correct order
        print('sent data')
        self.connector.send_and_receive_data()
    
    
    

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
    rospy.init_node('vel_sub')
    obj = ros_subscriber(my_connector)

    rospy.spin()
    my_connector.stop()
