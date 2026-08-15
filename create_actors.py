import numpy as np
import sapien

scene = sapien.Scene()
scene.add_ground(altitude=0)

builder = scene.create_actor_builder()
builder.add_box_collision(half_size=[0.3, 0.3, 0.3])
builder.add_box_visual(
    half_size=[0.3, 0.3, 0.3],
    material=[0.2, 0.7, 1.0],
)

box = builder.build(name="blue_box")
box.set_pose(sapien.Pose(p=[0, 0, 0.3]))

scene.set_ambient_light([0.5, 0.5, 0.5])
scene.add_directional_light([0, 1, -1], [0.5, 0.5, 0.5])

viewer = scene.create_viewer()
viewer.set_camera_xyz(x=-4, y=0, z=2)
viewer.set_camera_rpy(r=0, p=-np.arctan2(2, 4), y=0)

while not viewer.closed:
    scene.update_render()
    viewer.render()