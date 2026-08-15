import numpy as np
import sapien
from PIL import Image, ImageColor

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

segmentation = camera.get_picture("Segmentation")

colors = sorted(set(ImageColor.colormap.values()))

palette = np.array(
    [ImageColor.getrgb(color) for color in colors],
    dtype=np.uint8,
)

mesh_labels = segmentation[..., 0].astype(np.uint8)
actor_labels = segmentation[..., 1].astype(np.uint8)

mesh_image = Image.fromarray(palette[mesh_labels])
actor_image = Image.fromarray(palette[actor_labels])

mesh_image.save("mesh_segmentation.png")
actor_image.save("actor_segmentation.png")

print("Saved mesh_segmentation.png")
print("Saved actor_segmentation.png")