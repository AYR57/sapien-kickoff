import numpy as np
import sapien
from transforms3d.euler import euler2quat

scene = sapien.Scene()
scene.set_timestep(1 / 100.0)

scene.set_ambient_light([0.5, 0.5, 0.5])
scene.add_directional_light([0, 1, -1], [0.5, 0.5, 0.5])
scene.add_ground(altitude=0)

builder = scene.create_articulation_builder()

base = builder.create_link_builder()
base.set_name("base")

base.add_box_collision(half_size=[0.5, 0.5, 0.2])
base.add_box_visual(
    half_size=[0.5, 0.5, 0.2],
    material=sapien.render.RenderMaterial(
        base_color=[0.2, 0.5, 1.0, 1.0]
    ),
)

arm = builder.create_link_builder(base)
arm.set_name("arm")
arm.set_joint_name("arm_hinge")

arm.add_box_collision(
    half_size=[0.8, 0.12, 0.12],
    density=500.0,
)

arm.add_box_visual(
    half_size=[0.8, 0.12, 0.12],
    material=sapien.render.RenderMaterial(
        base_color=[1.0, 0.45, 0.1, 1.0]
    ),
)

arm.set_joint_properties(
    "revolute",
    limits=[[-np.pi / 2, np.pi / 2]],
    pose_in_parent=sapien.Pose(
        p=[0, 0, 0.2],
        q=euler2quat(0, -np.pi / 2, 0),
    ),
    pose_in_child=sapien.Pose(
        p=[-0.8, 0, 0],
        q=euler2quat(0, -np.pi / 2, 0),
    ),
)

articulation = builder.build(fix_root_link=True)
articulation.set_pose(sapien.Pose(p=[0, 0, 0.2]))

# Configure the single hinge joint's drive.
joint = articulation.get_active_joints()[0]
joint.set_drive_properties(stiffness=200.0, damping=20.0)
joint.set_drive_target(np.pi / 4)

viewer = scene.create_viewer()
viewer.set_camera_xyz(x=-3, y=-3, z=2.5)
viewer.set_camera_rpy(r=0, p=-0.5, y=0.75)

while not viewer.closed:
    scene.step()
    scene.update_render()
    viewer.render()