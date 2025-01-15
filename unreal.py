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
