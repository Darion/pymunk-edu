import pyglet, random
from pyglet.window import key
import pymunk
from pymunk import Vec2d

class Window(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        pyglet.window.Window.__init__(self, *args, **kwargs)
        self.init_physics()
        self.init_handlers()
        self.asteroids = []
        for n in range(1, 80):
            self.add_asteroid()
        self.add_ship()

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
        shape = pymunk.Poly(body,
                            [
                              (0, 0),
                              (radius, 0),
                              (radius, radius),
                              (0, radius)
                            ]
                          )
        self.space.add(body, shape)
        return shape

    def add_ship(self):
        mass = 5;
        radius = 24
        inertia = pymunk.moment_for_box(mass, 0, radius)
        body = pymunk.Body(mass, inertia)
        x = random.randint(20,600)
        y = random.randint(20,400)
        body.position = x, y
        shape = pymunk.Poly(body,
                            [
                              (0, 0),
                              (radius, 0),
                              (radius, radius),
                              (0, radius)
                            ]
                          )
        self.space.add(body, shape)
        self.ship = shape
        self.ship_body = body

    def draw_box(self, box, ship=False):
        coords = box.get_points()
        r = random.random()
        g = random.random()
        if(ship):
            pyglet.gl.glColor4f(1.0, 0.0, 0.0, 0.0)
        else:
            pyglet.gl.glColor4f(r, g, 1.0, 1.0)
        pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
            ('v2i', (
                int(round(coords[0].x)), int(round(coords[0].y)),
                int(round(coords[1].x)), int(round(coords[1].y)),
                int(round(coords[2].x)), int(round(coords[2].y)),
                int(round(coords[3].x)), int(round(coords[3].y)),
                ))
        )

    def ship_body(self):
        return self.space.bodies[len(self.space.bodies)-1]

    def update(self):
        speed = 50;
        if self.keys[key.UP]:
            self.ship_body.apply_impulse((0,speed))
        elif self.keys[key.RIGHT]:
            self.ship_body.apply_impulse((speed,0))
        elif self.keys[key.DOWN]:
            self.ship_body.apply_impulse((0,-speed))
        elif self.keys[key.LEFT]:
            self.ship_body.apply_impulse((-speed,0))

    def draw(self):
        for asteroid in self.asteroids:
            self.draw_box(asteroid)
        self.draw_box(self.ship, True)

if __name__ == "__main__":
    window = Window()
    window.main_loop()
