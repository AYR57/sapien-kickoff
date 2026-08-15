import sapien

scene = sapien.Scene()
scene.set_timestep(1 / 100.0)

scene.set_ambient_light([0.5, 0.5, 0.5])
scene.add_directional_light([0, 1, -1], [0.5, 0.5, 0.5])

ground_material = sapien.physx.PhysxMaterial(
    static_friction=0.8,
    dynamic_friction=0.6,
    restitution=0.1,
)
scene.add_ground(altitude=0, material=ground_material)

bouncy_material = sapien.physx.PhysxMaterial(
    static_friction=0.4,
    dynamic_friction=0.3,
    restitution=0.9,
)

dull_material = sapien.physx.PhysxMaterial(
    static_friction=0.8,
    dynamic_friction=0.7,
    restitution=0.0,
)

def add_ball(position, color, material, name):
    builder = scene.create_actor_builder()
    builder.add_sphere_collision(
        radius=0.15,
        material=material,
        density=1000.0,
    )
    builder.add_sphere_visual(
        radius=0.15,
        material=sapien.render.RenderMaterial(base_color=color),
    )
    ball = builder.build(name=name)
    ball.set_pose(sapien.Pose(p=position))
    return ball

add_ball(
    position=[-0.5, 0, 2],
    color=[1.0, 0.2, 0.2, 1.0],
    material=bouncy_material,
    name="bouncy_ball",
)

add_ball(
    position=[0.5, 0, 2],
    color=[0.2, 0.4, 1.0, 1.0],
    material=dull_material,
    name="dull_ball",
)

viewer = scene.create_viewer()
viewer.set_camera_xyz(x=-3, y=-3, z=2)
viewer.set_camera_rpy(r=0, p=-0.45, y=0.75)

while not viewer.closed:
    scene.step()
    scene.update_render()
    viewer.render()