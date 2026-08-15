import numpy as np
import sapien

scene = sapien.Scene()
scene.set_timestep(1 / 100.0)

scene.set_ambient_light([0.5, 0.5, 0.5])
scene.add_directional_light([0, 1, -1], [0.5, 0.5, 0.5])
scene.add_ground(altitude=0)

builder = scene.create_actor_builder()

builder.add_box_collision(half_size=[0.5, 0.5, 0.5])
builder.add_box_visual(
    half_size=[0.5, 0.5, 0.5],
    material=sapien.render.RenderMaterial(
        base_color=[0.2, 0.6, 1.0, 1.0]
    ),
)

box = builder.build_kinematic(name="box")
box.set_pose(sapien.Pose(p=[0, 0, 0.5]))

camera = scene.add_camera(
    name="scene_camera",
    width=640,
    height=480,
    fovy=1.0,
    near=0.1,
    far=10.0,
)

camera_position = np.array([2.5, -2.5, 1.8])

forward = -camera_position / np.linalg.norm(camera_position)

left = np.cross([0, 0, 1], forward)
left = left / np.linalg.norm(left)

up = np.cross(forward, left)

camera_pose = np.eye(4)
camera_pose[:3, :3] = np.stack([forward, left, up], axis=1)
camera_pose[:3, 3] = camera_position

camera.set_pose(sapien.Pose(camera_pose))

viewer = scene.create_viewer()
viewer.set_camera_xyz(x=3, y=-3, z=2)
viewer.set_camera_rpy(r=0, p=-0.4, y=2.35)

while not viewer.closed:
    scene.step()
    scene.update_render()
    viewer.render()
