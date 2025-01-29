import rospy
from geometry_msgs.msg import Pose
from multiverse_client_py import MultiverseClient, MultiverseMetaData

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


if __name__ == "__main__":
    multiverse_meta_data = MultiverseMetaData(
        world_name="my_world",
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
    my_connector.stop()

    