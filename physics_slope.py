import numpy as np
import sapien
import transforms3d

scene = sapien.Scene()
scene.set_timestep(1 / 100.0)

scene.set_ambient_light([0.5, 0.5, 0.5])
scene.add_directional_light([0, 1, -1], [0.5, 0.5, 0.5])
scene.add_ground(altitude=0)

# A fixed, slanted surface
slope_builder = scene.create_actor_builder()
slope_builder.add_box_collision(half_size=[1.5, 1.5, 0.1])
slope_builder.add_box_visual(
    half_size=[1.5, 1.5, 0.1],
    material=sapien.render.RenderMaterial(base_color=[0.3, 0.5, 0.8, 1.0]),
)

slope = slope_builder.build_kinematic(name="slope")
slope.set_pose(
    sapien.Pose(
        p=[0, 0, 0.5],
        q=transforms3d.euler.euler2quat(0, np.deg2rad(20), 0),
    )
)

# A dynamic sphere that falls and rolls/slides
ball_builder = scene.create_actor_builder()
ball_builder.add_sphere_collision(radius=0.15)
ball_builder.add_sphere_visual(
    radius=0.15,
    material=sapien.render.RenderMaterial(base_color=[1.0, 0.4, 0.1, 1.0]),
)

ball = ball_builder.build(name="ball")
ball.set_pose(sapien.Pose(p=[0, 0, 1.2]))

viewer = scene.create_viewer()
viewer.set_camera_xyz(x=-3, y=-3, z=2)
viewer.set_camera_rpy(r=0, p=-0.45, y=0.75)

while not viewer.closed:
    scene.step()
    scene.update_render()
    viewer.render()