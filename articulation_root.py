import sapien

scene = sapien.Scene()
scene.set_timestep(1 / 100.0)

scene.set_ambient_light([0.5, 0.5, 0.5])
scene.add_directional_light([0, 1, -1], [0.5, 0.5, 0.5])
scene.add_ground(altitude=0)

builder = scene.create_articulation_builder()

root_builder = builder.create_link_builder()
root_builder.set_name("root")

root_builder.add_box_collision(
    half_size=[0.4, 0.4, 0.2]
)

root_builder.add_box_visual(
    half_size=[0.4, 0.4, 0.2],
    material=sapien.render.RenderMaterial(
        base_color=[0.2, 0.5, 1.0, 1.0]
    ),
)

articulation = builder.build(fix_root_link=True)
articulation.set_pose(sapien.Pose(p=[0, 0, 0.2]))

viewer = scene.create_viewer()
viewer.set_camera_xyz(x=-3, y=-3, z=2)
viewer.set_camera_rpy(r=0, p=-0.45, y=0.75)

while not viewer.closed:
    scene.step()
    scene.update_render()
    viewer.render()