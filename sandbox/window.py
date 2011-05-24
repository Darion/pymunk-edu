import pyglet
from pyglet.window import key
import pymunk
from pymunk import Vec2d
from draw import PygletDraw

class Window(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        pyglet.window.Window.__init__(self, *args, **kwargs)
        self.init_physics()
        self.init_handlers()
        self.drawline = DrawLines()

    def init_physics(self):
        pymunk.init_pymunk()
        self.space = pymunk.Space()
        self.space.gravity = (0.0, 0.0)

    def init_handlers(self):
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)

    def main_loop(self):
        while not self.has_exit:
            self.dispatch_events()
            self.clear()
            self.update()
            self.space.step(1/50.0)
            print len(self.drawline.points)
            self.draw()
            pyglet.clock.tick()
            self.flip()

    def on_mouse_press(self, x, y, button, modifiers):
        self.drawline.add_point(Vec2d(x, y))

    def on_mouse_motion(self, x, y, dx, dy):
        self.drawline.set_float_point(Vec2d(x, y))

    def update(self):
        pass
    def draw(self):
        self.drawline.draw()

class DrawLines():
    points = []
    float_point = []
    def __init__(self):
        pass
    def add_point(self, point):
        self.points.append(point)
    def set_float_point(self, point):
        self.float_point = point
    def finish(self):
        pass
    def draw(self):
        if len(self.points) > 1:
            last = self.points[0]
            for n in range(1, len(self.points)):
                current = self.points[n]
                PygletDraw.line(last, current)
                last = current
            PygletDraw.line(last, self.float_point)


class Widget():
    def __init__(self):
        pass
