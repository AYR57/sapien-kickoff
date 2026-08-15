import time
import numpy as np
import sapien

scene = sapien.Scene()
scene.set_timestep(1 / 100.0)
scene.add_ground(altitude=0)

builder = scene.create_actor_builder()
builder.add_box_collision(half_size=[0.2, 0.2, 0.2])
builder.add_box_visual(
    half_size=[0.2, 0.2, 0.2],
    material=[0.2, 0.6, 1.0],
)

box = builder.build(name="physics_box")
box.set_pose(sapien.Pose(p=[0, 0, 2]))

scene.set_ambient_light([0.5, 0.5, 0.5])
scene.add_directional_light([0, 1, -1], [0.5, 0.5, 0.5])

viewer = scene.create_viewer()
viewer.set_camera_xyz(x=-5, y=0, z=2.5)
viewer.set_camera_rpy(r=0, p=-np.arctan2(2.5, 5), y=0)

print("The box will fall in 2 seconds.")

start_time = time.time()

while not viewer.closed:
    if time.time() - start_time > 2:
        scene.step()

    scene.update_render()
    viewer.render()