import numpy as np
import sapien
from PIL import Image

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
    name="rgb_camera",
    width=640,
    height=480,
    fovy=np.deg2rad(45),
    near=0.1,
    far=10.0,
)

camera.set_pose(sapien.Pose(camera_pose))

scene.step()
scene.update_render()

camera.take_picture()

rgba = camera.get_picture("Color")
rgba_image = (rgba * 255).clip(0, 255).astype(np.uint8)

Image.fromarray(rgba_image).save("camera_rgb.png")

print("Saved camera_rgb.png")