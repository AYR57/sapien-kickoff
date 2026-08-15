import numpy as np
import sapien

scene = sapien.Scene()
scene.set_timestep(1 / 100.0)

scene.add_ground(altitude=0)

builder = scene.create_actor_builder()

builder.add_convex_collision_from_file(
    filename="assets/banana/collision_meshes/collision.obj"
)

builder.add_visual_from_file(
    filename="assets/banana/visual_meshes/visual.glb"
)

banana = builder.build(name="banana")
banana.set_pose(sapien.Pose(p=[0, 0, 1]))

scene.set_ambient_light([0.5, 0.5, 0.5])
scene.add_directional_light([0, 1, -1], [0.5, 0.5, 0.5])

viewer = scene.create_viewer()
viewer.set_camera_xyz(x=-3, y=0, z=2)
viewer.set_camera_rpy(r=0, p=-np.arctan2(2, 3), y=0)

while not viewer.closed:
    scene.step()
    scene.update_render()
    viewer.render()