import socket
import unreal
actor_name = 'rollin-justin-anim'
all_actors = unreal.EditorLevelLibrary.get_all_level_actors()

for actor in all_actors:
    if actor.get_name() == actor_name:
        new_location = unreal.Vector(10.0 , 20.0 , 0.0)
        actor.set_actor_location(new_location)
        unreal.log('Actor new position set')
        break
class unreal_ros:
    def __init__(self):
        self.host = '127.0.0.1'
        self.unreal_receive_port = 5000
        self.unreal_send_port = 6000
        self.unreal_receive_sock = socket.socket(socket.AF_INET ,socket.SOCK_STREAM)
        self.unreal_receive_sock.bind(self.host , self.unreal_receive_port)
        all_actors = unreal.EditorLevelLibrary.get_all_level_actors()
        self.client_sender_socket , client_address = self.unreal_receive_sock.accept()
        for actor in all_actors:
            if actor.get_name() == actor_name: 
                self.desired_actor = actor
                break    
    def sender(self):
        client_socket , client_address = self.unreal_receive_sock.accept()
        

    def receiver(self):
        data = self.client_sender_socket.recv(1024)
        if not data: 
            break
        pose_data = data.decode('utf-8')
        new_x = pose_data[0]
        new_y = pose_data[1]
        new_theta = pose_data[2]
        self.desired_actor.set_actor_location(unreal.Vector(new_x , new_y , new_theta))
    


if __name__ == "__main__":
    obj = unreal_ros()
    while True : 
        obj.receiver()