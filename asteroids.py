# -*- encoding: utf-8 -*-

import pyglet, random
from pyglet.window import key
import pymunk
from pymunk import Vec2d


class PymunkShape():
    """
    Общие геометрические фигуры Pymunk
    """
    @staticmethod
    def square(body, side):
        """
        :param side: Длина стороны
        """
        shape = pymunk.Poly(body,
            [
              (0, 0),
              (side, 0),
              (side, side),
              (0, side)
            ]
        )
        return shape

class PygletDraw():
    """
    Отрисовка примитивов в Pyglet
    """
    @staticmethod
    def square(coords):
        """
        Четырехугольник
        :param coords: Четыре точки - координаты (Vec2d)
        """
        pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
            ('v2i', (
                int(round(coords[0].x)), int(round(coords[0].y)),
                int(round(coords[1].x)), int(round(coords[1].y)),
                int(round(coords[2].x)), int(round(coords[2].y)),
                int(round(coords[3].x)), int(round(coords[3].y)),
                ))
        )
    @staticmethod
    def line(p1, p2):
        """
        Прямая линия
        :param p1: Первый конец линии
        :param p2: Второй конец линии
        """
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                             ('v2i', (int(p1.x), int(p1.y), int(p2.x), int(p2.y)))
                             )


class SpaceShip():
    def __init__(self, space):
        mass = 5;
        radius = 24
        inertia = pymunk.moment_for_box(mass, 0, radius)
        body = pymunk.Body(mass, inertia)
        x = random.randint(20,600)
        y = random.randint(20,400)
        body.position = x, y
        shape = PymunkShape.square(body, radius)
        space.add(body, shape)
        self.shape = shape
        self.body = body
    def draw_box(self, box):
        coords = box.get_points()
        pyglet.gl.glColor4f(1.0, 0.0, 0.0, 0.0)
        PygletDraw.square(coords)
    def draw(self):
        self.draw_box(self.shape)


class Window(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        pyglet.window.Window.__init__(self, *args, **kwargs)
        self.init_physics()
        self.init_handlers()
        self.asteroids = []
        for n in range(1, 80):
            self.add_asteroid()
        self.lines = self.add_borders()
        self.ship = SpaceShip(self.space)

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

    def add_asteroid(self):
        asteroid = self.add_box()
        self.asteroids.append(asteroid)

    def add_box(self, mass=1):
        radius = 24
        inertia = pymunk.moment_for_box(mass, 0, radius)
        body = pymunk.Body(mass, inertia)
        x = random.randint(20,600)
        y = random.randint(20,400)
        body.position = x, y
        shape = PymunkShape.square(body, radius)
        self.space.add(body, shape)
        return shape

    def draw_box(self, box):
        coords = box.get_points()
        r = random.random()
        g = random.random()
        pyglet.gl.glColor4f(r, g, 1.0, 1.0)
        PygletDraw.square(coords)

    def update(self):
        speed = 90;
        if self.keys[key.UP]:
            self.ship.body.apply_impulse((0,speed))
        elif self.keys[key.RIGHT]:
            self.ship.body.apply_impulse((speed,0))
        elif self.keys[key.DOWN]:
            self.ship.body.apply_impulse((0,-speed))
        elif self.keys[key.LEFT]:
            self.ship.body.apply_impulse((-speed,0))

    def add_borders(self):
        body = pymunk.Body(pymunk.inf, pymunk.inf)
        body.position = (50,50)
        width = 550.0
        height = 400.0
        l1 = pymunk.Segment(body, (0.0, 0.0), (0.0, height), 5.0)
        l2 = pymunk.Segment(body, (0.0, height), (width, height), 5.0)
        l3 = pymunk.Segment(body, (width, height), (width, 0.0), 5.0)
        l4 = pymunk.Segment(body, (width, 0), (0.0, 0.0), 5.0)
        self.space.add_static(l1, l2, l3, l4)
        return l1,l2,l3,l4


    def draw_lines(self, lines):
        for line in lines:
            body = line.body
            pv1 = body.position + line.a.rotated(body.angle)
            pv2 = body.position + line.b.rotated(body.angle)
            p1 = to_pyglet(pv1)
            p2 = to_pyglet(pv2)
            pyglet.gl.glColor4f(0.0,1.0,1.0,1.0)
            PygletDraw.line(p1, p2)

    def draw(self):
        for asteroid in self.asteroids:
            self.draw_box(asteroid)
        self.draw_lines(self.lines)
        self.ship.draw()

def to_pyglet(p):
    return Vec2d(round_to_int(p.x), round_to_int(p.y))

def round_to_int(f):
    return int(round(f))

if __name__ == "__main__":
    window = Window()
    window.main_loop()
