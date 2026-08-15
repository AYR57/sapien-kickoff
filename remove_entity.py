import time
import numpy as np
import sapien

scene = sapien.Scene()
scene.add_ground(altitude=0)

builder = scene.create_actor_builder()
builder.add_box_collision(half_size=[0.3, 0.3, 0.3])
builder.add_box_visual(
    half_size=[0.3, 0.3, 0.3],
    material=[1.0, 0.4, 0.2],
)

box = builder.build(name="temporary_box")
box.set_pose(sapien.Pose(p=[0, 0, 0.3]))

scene.set_ambient_light([0.5, 0.5, 0.5])
scene.add_directional_light([0, 1, -1], [0.5, 0.5, 0.5])

viewer = scene.create_viewer()
viewer.set_camera_xyz(x=-4, y=0, z=2)
viewer.set_camera_rpy(r=0, p=-np.arctan2(2, 4), y=0)

start_time = time.time()
removed = False

while not viewer.closed:
    if not removed and time.time() - start_time >= 3:
        scene.remove_entity(box)
        print("Removed the orange box.")
        removed = True

    scene.update_render()
    viewer.render()