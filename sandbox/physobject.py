import pyglet, pymunk

class PhysObject():
    def __init__(self):
        pass
    def draw(self):
        pass
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
    def add_to_space(self, space):
        if self.static == False:
            space.add(self.shape, self.body)
        else:
            space.add_static(self.shape)
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
        label = pyglet.text.Label(text,
              font_name='Monospace',
              font_size=8,
              x=self.points[0].x, y=self.points[0].y,
              anchor_x='left', anchor_y='center',
              color=(0,255,0,200))
        label.draw()
    def update(self):
        self.points = self.shape.get_points()

