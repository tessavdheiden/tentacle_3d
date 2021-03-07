from pyglet.window import key
import imageio

from gym.envs.classic_control.rendering import *


from tentacle import Tentacle
from rendering_3d import *


if __name__ == '__main__':
    frames = []
    target = [0, 0, 0]
    viewer = Viewer3D(500, 500)
    viewer.set_bounds(-.5, .5, -.5, .5)
    dot = Point3D()
    dt = Transform3D()
    dot.add_attr(dt)
    viewer.add_geom(dot)

    axes = make_axes()
    for ax in axes:
        viewer.add_geom(ax)

    base = np.array([0, 0, 0])
    t = Tentacle(*base)
    for segment in t.segments:
        viewer.add_geom(segment)

    open_viewer = True

    @viewer.window.event
    def on_key_press(s,m):
        global target, open_viewer
        dx, dy, dz = 0, 0, 0
        if s == key.LEFT:
            dx = -.1
        elif s == key.RIGHT:
            dx = .1
        elif s == key.UP:
            dy = .1
        elif s == key.DOWN:
            dy = -.1
        elif s == key.D:
            dz = -.1
        elif s == key.S:
            dz = .1
        elif s == key.ESCAPE:
            open_viewer = False
        target = [target[0] + dx, target[1] + dy, target[2] + dz]
        dt.set_translation(target[0], target[1], target[2])

    while open_viewer:
        print(f"({target[0]:.2f}, {target[1]:.2f}, {target[2]:.2f})")
        target_ = target
        for segment in reversed(t.segments):
            segment.follow(*target_)
            target_ = segment.start
        target_ = base
        for segment in t.segments:
            segment.set_start(target_)
            target_ = segment.end
        frames.append(viewer.render(return_rgb_array=True))
        imageio.mimsave('video.gif', frames, fps=30)
