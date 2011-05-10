import pyglet, random
from pyglet.window import key
import pymunk
from pymunk import Vec2d

class Window(pyglet.window.Window):
  def __init__(self, *args, **kwargs):
    pyglet.window.Window.__init__(self, *args, **kwargs)
    self.keys = key.KeyStateHandler()
    self.push_handlers(self.keys)
    pymunk.init_pymunk()
    self.space = pymunk.Space()
    self.space.gravity = (0.0, -800.0)
    self.lines = add_static_L(self.space)
    self.boxes = []
  def main_loop(self):
    while not self.has_exit:
      self.dispatch_events()
      self.clear()
      self.update()
      self.draw()
      pyglet.clock.tick()
      self.flip()
  def update(self):
    if self.keys[key.UP]:
        box = add_box(self.space)
        self.boxes.append(box)
    self.space.step(1/50.0)
  def draw(self):
      for box in self.boxes:
          draw_box(self.screen, box)
      draw_lines(self.screen, self.lines)

def add_box(space):
    mass = 1
    radius = 24
    inertia = pymunk.moment_for_box(mass, 0, radius) # 1
    body = pymunk.Body(mass, inertia) # 2
    x = random.randint(220,380)
    body.position = x, 420 # 3
    shape = pymunk.Poly(body,
                        [
                          (0, 0),
                          (radius, 0),
                          (radius, radius),
                          (0, radius)
                        ]
                      )
    space.add(body, shape) # 5
    return shape

def draw_box(screen, box):
    coords = box.get_points()
    pyglet.gl.glColor4f(1.0,1,0,1.0)
    pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
        ('v2i', (
            int(round(coords[0].x)), int(round(coords[0].y)),
            int(round(coords[1].x)), int(round(coords[1].y)),
            int(round(coords[2].x)), int(round(coords[2].y)),
            int(round(coords[3].x)), int(round(coords[3].y)),
            ))
    )

def add_static_L(space):
    # static body with infinite mass and inertia
    body = pymunk.Body(pymunk.inf, pymunk.inf)
    body.position = (300,300)
    # line shapes
    l1 = pymunk.Segment(body, (-250, -100), (255.0, 0.0), 5.0)
    l2 = pymunk.Segment(body, (-250.0, 0), (150.0, 200.0), 5.0)

    # add static objects to space
    # static objects calculates faster
    space.add_static(l1, l2)
    return l1,l2

def draw_lines(screen, lines):
    for line in lines:
        body = line.body
        pv1 = body.position + line.a.rotated(body.angle) # 1
        pv2 = body.position + line.b.rotated(body.angle)
        p1 = to_pyglet(pv1) # 2
        p2 = to_pyglet(pv2)
        print "%s - %s" % (pv1, pv2)
        pyglet.gl.glColor4f(1.0,0,0,1.0)
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
            ('v2i', (int(p1.x), int(p1.y), int(p2.x), int(p2.y)))
        )

def to_pyglet(p):
    return Vec2d(round_to_int(p.x), round_to_int(p.y))

def round_to_int(f):
    return int(round(f))


if __name__ == '__main__':
  window = Window()
  window.main_loop()
