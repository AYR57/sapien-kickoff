import numpy as np
import sapien
from PIL import Image

scene = sapien.Scene()
scene.set_timestep(1 / 240)

scene.add_ground(altitude=0)

builder = scene.create_actor_builder()

builder.add_box_collision(
    half_size=[0.25, 0.25, 0.25]
)

builder.add_box_visual(
    half_size=[0.25, 0.25, 0.25],
    material=sapien.render.RenderMaterial(
        base_color=[0.1, 0.4, 0.9, 1.0]
    ),
)

cube = builder.build(name="blue_cube")
cube.set_pose(sapien.Pose([0, 0, 0.25]))

scene.add_directional_light(
    direction=[-1, -1, -1],
    color=[1, 1, 1],
    shadow=True,
)

scene.set_ambient_light([0.3, 0.3, 0.3])

camera = scene.add_camera(
    name="camera",
    width=640,
    height=480,
    fovy=np.deg2rad(60),
    near=0.1,
    far=100,
)

camera.set_entity_pose(
    sapien.Pose(
        [1.2, -1.2, 0.9],
        [0.849, 0.176, 0.326, 0.383],
    )
)

scene.update_render()
camera.take_picture()

position = camera.get_picture("Position")

depth_meters = -position[..., 2]
valid_pixels = position[..., 3] < 1

depth_mm = np.zeros(depth_meters.shape, dtype=np.uint16)
depth_mm[valid_pixels] = (
    depth_meters[valid_pixels] * 1000
).astype(np.uint16)

Image.fromarray(depth_mm).save("depth_mm.png")

preview = np.zeros(depth_meters.shape, dtype=np.uint8)

if np.any(valid_pixels):
    nearest = depth_meters[valid_pixels].min()
    farthest = depth_meters[valid_pixels].max()

    normalized = (depth_meters[valid_pixels] - nearest) / (
        farthest - nearest + 1e-8
    )

    preview[valid_pixels] = (255 * (1 - normalized)).astype(np.uint8)

Image.fromarray(preview).save("depth_preview.png")

print("Saved depth_mm.png")
print("Saved depth_preview.png")