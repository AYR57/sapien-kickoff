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

camera_position = np.array([-2.5, -2.5, 1.8])

forward = -camera_position / np.linalg.norm(camera_position)
left = np.cross([0, 0, 1], forward)
left = left / np.linalg.norm(left)
up = np.cross(forward, left)

camera_pose = np.eye(4)
camera_pose[:3, :3] = np.stack([forward, left, up], axis=1)
camera_pose[:3, 3] = camera_position

camera = scene.add_camera(
    name="point_cloud_camera",
    width=640,
    height=480,
    fovy=np.deg2rad(45),
    near=0.1,
    far=10.0,
)

camera.entity.set_pose(sapien.Pose(camera_pose))

scene.step()
scene.update_render()

camera.take_picture()

position = camera.get_picture("Position")

valid_pixels = position[..., 3] < 1
points_opengl = position[..., :3][valid_pixels]

model_matrix = camera.get_model_matrix()

points_world = (
    points_opengl @ model_matrix[:3, :3].T
    + model_matrix[:3, 3]
)

np.savetxt(
    "point_cloud.xyz",
    points_world,
    fmt="%.6f",
)

print(f"Saved {len(points_world)} 3D points to point_cloud.xyz")