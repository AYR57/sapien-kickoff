import numpy as np
import sapien


def main():
    scene = sapien.Scene()
    scene.set_timestep(1 / 100.0)

    scene.add_ground(altitude=0)

    actor_builder = scene.create_actor_builder()
    actor_builder.add_box_collision(half_size=[0.5, 0.5, 0.5])
    actor_builder.add_box_visual(
        half_size=[0.5, 0.5, 0.5],
        material=[1.0, 0.0, 0.0],
    )

    box = actor_builder.build(name="box")
    box.set_pose(sapien.Pose(p=[0, 0, 0.5]))

    scene.set_ambient_light([0.5, 0.5, 0.5])
    scene.add_directional_light([0, 1, -1], [0.5, 0.5, 0.5])

    viewer = scene.create_viewer()

    viewer.set_camera_xyz(x=-4, y=0, z=2)
    viewer.set_camera_rpy(r=0, p=-np.arctan2(2, 4), y=0)
    viewer.window.set_camera_parameters(near=0.05, far=100, fovy=1)

    while not viewer.closed:
        scene.step()
        scene.update_render()
        viewer.render()


if __name__ == "__main__":
    main()