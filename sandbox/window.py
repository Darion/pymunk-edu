import pyglet
from pyglet.window import key
from pyglet.window import mouse
import pymunk
from pymunk import Vec2d
from draw import PygletDraw

class Window(pyglet.window.Window):
    objects = []
    drawline = None
    def __init__(self, *args, **kwargs):
        pyglet.window.Window.__init__(self, *args, **kwargs)
        self.init_physics()
        self.init_handlers()

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
            self.draw()
            pyglet.clock.tick()
            self.flip()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.drawline != None:
            self.drawline.add_point(Vec2d(x, y))
            if button == mouse.LEFT:
                pass
            elif button == mouse.RIGHT:
                self.objects.append(Polygonal(self.drawline.points))
                self.drawline = None
        else:
            self.drawline = DrawLines()
            self.drawline.add_point(Vec2d(x, y))


    def on_mouse_motion(self, x, y, dx, dy):
        if self.drawline != None:
            self.drawline.set_float_point(Vec2d(x, y))

    def update(self):
        pass
    def draw(self):
        if self.drawline != None:
            self.drawline.draw()
        for o in self.objects:
            o.draw()

class PhysObject():
    def __init__(self):
        pass
    def draw(self):
        pass

class Polygonal(PhysObject):
    def __init__(self, points):
        self.points = points
    def draw(self):
        ns = []
        for point in self.points:
            ns.append(point.x)
            ns.append(point.y)
        pyglet.graphics.draw(len(self.points), pyglet.gl.GL_POLYGON, ('v2f', ns))

class DrawLines():
    points = []
    float_point = Vec2d(0,0)
    def __init__(self):
        self.points = []
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
