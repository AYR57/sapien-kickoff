import numpy as np
import sapien

scene = sapien.Scene()
scene.add_ground(altitude=0)

builder = scene.create_actor_builder()

builder.add_box_collision(
    pose=sapien.Pose(p=[0, 0, 0]),
    half_size=[0.4, 0.4, 0.2],
)
builder.add_box_visual(
    pose=sapien.Pose(p=[0, 0, 0]),
    half_size=[0.4, 0.4, 0.2],
    material=[0.3, 0.7, 1.0],
)

builder.add_sphere_collision(
    pose=sapien.Pose(p=[0, 0, 0.45]),
    radius=0.2,
)
builder.add_sphere_visual(
    pose=sapien.Pose(p=[0, 0, 0.45]),
    radius=0.2,
    material=[1.0, 0.3, 0.2],
)

compound_actor = builder.build(name="box_and_sphere")
compound_actor.set_pose(sapien.Pose(p=[0, 0, 0.2]))

scene.set_ambient_light([0.5, 0.5, 0.5])
scene.add_directional_light([0, 1, -1], [0.5, 0.5, 0.5])

viewer = scene.create_viewer()
viewer.set_camera_xyz(x=-5, y=0, z=2.5)
viewer.set_camera_rpy(r=0, p=-np.arctan2(2.5, 5), y=0)

while not viewer.closed:
    scene.update_render()
    viewer.render()