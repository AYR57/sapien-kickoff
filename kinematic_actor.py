import math
import sapien

scene = sapien.Scene()
scene.set_timestep(1 / 100.0)

scene.set_ambient_light([0.5, 0.5, 0.5])
scene.add_directional_light([0, 1, -1], [0.5, 0.5, 0.5])
scene.add_ground(altitude=0)

# A red cube controlled directly by this script.
builder = scene.create_actor_builder()
builder.add_box_collision(half_size=[0.3, 0.3, 0.3])
builder.add_box_visual(
    half_size=[0.3, 0.3, 0.3],
    material=sapien.render.RenderMaterial(base_color=[1.0, 0.2, 0.2, 1.0]),
)

cube = builder.build_kinematic(name="moving_cube")

viewer = scene.create_viewer()
viewer.set_camera_xyz(x=-3, y=-3, z=2)
viewer.set_camera_rpy(r=0, p=-0.45, y=0.75)

time = 0.0

while not viewer.closed:
    x = math.sin(time) * 1.2
    cube.set_pose(sapien.Pose(p=[x, 0, 1.2]))

    scene.step()
    scene.update_render()
    viewer.render()

    time += scene.get_timestep()