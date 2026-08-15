import sapien

scene = sapien.Scene()
scene.set_timestep(1 / 100.0)

scene.set_ambient_light([0.5, 0.5, 0.5])
scene.add_directional_light([0, 1, -1], [0.5, 0.5, 0.5])
scene.add_ground(altitude=0)

builder = scene.create_actor_builder()

builder.add_box_collision(
    half_size=[0.2, 0.2, 0.2]
)

builder.add_box_visual(
    half_size=[0.2, 0.2, 0.2],
    material=sapien.render.RenderMaterial(
        base_color=[0.2, 0.9, 0.3, 1.0]
    ),
)

box = builder.build(name="damped_box")
box.set_pose(sapien.Pose(p=[0, 0, 0.25]))

rigid_body = box.find_component_by_type(
    sapien.physx.PhysxRigidDynamicComponent
)

rigid_body.linear_damping = 0.8
rigid_body.angular_damping = 0.8

rigid_body.linear_velocity = [3.0, 0.0, 0.0]
rigid_body.angular_velocity = [0.0, 0.0, 8.0]

viewer = scene.create_viewer()
viewer.set_camera_xyz(x=-4, y=-4, z=3)
viewer.set_camera_rpy(r=0, p=-0.5, y=0.75)

while not viewer.closed:
    scene.step()
    scene.update_render()
    viewer.render()