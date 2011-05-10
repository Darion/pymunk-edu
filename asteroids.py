import pyglet, random
from pyglet.window import key
import pymunk
from pymunk import Vec2d

class Window(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        pyglet.window.Window.__init__(self, *args, **kwargs)
        self.init.physics()
        self.init_handlers()

    def init_physics(self):
        pymunk.init_pymunk()
        self.space = pymunk.Space()
        self.space.gravity = (0.0, -800.0)

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

    def update(self):
        pass

    def draw(self):
        for box in self.boxes:
            draw_box(self.screen, box)
        draw_lines(self.screen, self.lines)



