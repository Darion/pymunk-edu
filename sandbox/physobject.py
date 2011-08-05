import pyglet, pymunk
from draw import *

class PhysObject():
    def __init__(self):
        pass
    def draw(self):
        pass
    def add_to_space(self, space):
        if self.static == False:
            space.add(self.shape, self.body)
        else:
            space.add_static(self.shape)
    def _draw_label(self, point, text):
        label = pyglet.text.Label(text,
              font_name='Monospace',
              font_size=8,
              x=point.x, y=point.y,
              anchor_x='left', anchor_y='center',
              color=(0,255,0,200))
        label.draw()
    def debug_info(self):
        info = ''
        info += 'velocity: %s\n' % self.body.velocity
        info += 'angle: %s\n' % self.body.angle
        info += 'angular_velocity: %s\n' % self.body.angular_velocity
        info += 'mass: %s\n' % self.body.mass
        info += 'moment: %s\n' % self.body.moment
        info += 'rotation_vector: %s\n' % self.body.rotation_vector
        return info

class Polygonal(PhysObject):
    def __init__(self, points, static=False):
        self.points = points
        self.static = static
        self.body = self._body()
        self.shape = self._shape(self.body)
    def _body(self):
        if self.static == False:
            mass = 20
            # saint random!
            radius = 20
            #inertia = pymunk.moment_for_box(mass, 0, radius)
            inertia = pymunk.moment_for_poly(mass, self.points)
            body = pymunk.Body(mass, inertia)
        else:
            body = pymunk.Body(pymunk.inf, pymunk.inf)
        return body
    def _shape(self, body):
        shape = pymunk.Poly(body, self.points)
        return shape
    def draw(self):
        ns = []
        for point in self.points:
            ns.append(point.x)
            ns.append(point.y)
        pyglet.gl.glColor4f(0.7,0.7,0.7,1.0)
        pyglet.graphics.draw(len(self.points), pyglet.gl.GL_POLYGON, ('v2f', ns))
        pyglet.gl.glColor4f(1.0,0.0,0.0,1.0)
        pyglet.graphics.draw(len(self.points), pyglet.gl.GL_POINTS, ('v2f', ns))
    def draw_label(self, text):
        self._draw_label(self.points[0], text)
    def update(self):
        self.points = self.shape.get_points()

class Segment(PhysObject):
    """Pymunk Segment Analog"""
    def __init__(self, a, b, static=False):
        self.a, self.b, self.static = a, b, static
        self.radius = 5
        self.body = self._body()
        self.shape = self._shape(self.body)
    def _body(self):
        if self.static == False:
            mass = 20
            inertia = pymunk.moment_for_segment(mass, self.a, self.b)
            body = pymunk.Body(mass, inertia)
        else:
            body = pymunk.Body(pymunk.inf, pymunk.inf)
        return body
    def _shape(self, body):
        shape = pymunk.Segment(body, self.a, self.b, self.radius)
        return shape
    def draw(self):
        PygletDraw.line(self.a, self.b)
    def draw_label(self, text):
        self._draw_label(self.a, text)
    def update(self):
        #self.a, self.b = self.shape.a, self.shape.b
        pass
    def debug_info(self):
        #info = super(self.__class__, self).debug_info()
        info = PhysObject.debug_info(self)
        info += 'a: %s\n' % self.shape.a
        info += 'b: %s\n' % self.shape.b
        return info
