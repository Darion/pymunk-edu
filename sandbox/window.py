import pyglet
from pyglet.window import key
from pyglet.window import mouse
import pymunk
from pymunk import Vec2d
from draw import PygletDraw
from random import randint

class Window(pyglet.window.Window):
    objects = []
    widgets = []
    drawline = None
    drawmode = 1
    DRAWMODE_RIGID = 1
    DRAWMODE_STATIC = 2
    def __init__(self, *args, **kwargs):
        pyglet.window.Window.__init__(self, *args, **kwargs)
        self.init_physics()
        self.init_handlers()
        mode_widget = Widget('rigid', Vec2d(10,25))
        fps_widget = Widget('null', Vec2d(10, 10))
        command_widget = Widget('', Vec2d(10, 40))
        self.widgets.append(mode_widget)
        self.widgets.append(fps_widget)
        self.widgets.append(command_widget)
        self.set_drawmode(self.DRAWMODE_RIGID)
        self.input_active = False
        self.input_text = ''

    def set_drawmode(self, mode):
        self.drawmode = mode
        if mode == self.DRAWMODE_RIGID:
            self.widgets[0].set_text('rigid')
        elif mode == self.DRAWMODE_STATIC:
            self.widgets[0].set_text('static')
        else:
            "mode %i not defined" % mode

    def init_physics(self):
        pymunk.init_pymunk()
        self.space = pymunk.Space()
        self.space.gravity = (0.0, -50.0)

    def init_handlers(self):
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)

    def main_loop(self):
        while not self.has_exit:
            self.dispatch_events()
            self.clear()
            pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
            pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
            pyglet.gl.glEnable(pyglet.gl.GL_LINE_SMOOTH)
            pyglet.gl.glHint(pyglet.gl.GL_LINE_SMOOTH_HINT, pyglet.gl.GL_DONT_CARE)
            self.update()
            self.space.step(1/50.0)
            self.draw()
            self.widgets[1].set_text("fps: %f" % pyglet.clock.get_fps())
            pyglet.clock.tick()
            self.flip()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.drawline != None:
            self.drawline.add_point(Vec2d(x, y))
            if button == mouse.LEFT:
                pass
            elif button == mouse.RIGHT:
                if (self.drawmode == self.DRAWMODE_STATIC):
                    p = Polygonal(self.drawline.points, True)
                else:
                    p = Polygonal(self.drawline.points)
                p.add_to_space(self.space)
                self.objects.append(p)
                self.drawline = None
        else:
            self.drawline = DrawLines()
            self.drawline.add_point(Vec2d(x, y))

    def on_key_press(self, symbol, modifiers):
        if self.input_active:
            pass
        else:
            if symbol == key.R:
                self.set_drawmode(self.DRAWMODE_RIGID)
            elif symbol == key.S:
                self.set_drawmode(self.DRAWMODE_STATIC)
            elif symbol == key.Q:
                self.close()
           # elif symbol == key.COLON:
           #     self.input_start()

    def on_text(self, symbol):
        if self.input_active:
            if ord(symbol) == 13:
                # if symbol - "enter key"
                self.input_finish()
            else:
                if self.input_symbol_printable(symbol):
                    self.input_add_symbol(symbol)
        else:
            if symbol == ':':
                self.input_start()

    def on_text_motion(self, symbol):
        if self.input_active:
            if symbol == key.MOTION_BACKSPACE:
                self.input_backspace()


    def on_mouse_motion(self, x, y, dx, dy):
        if self.drawline != None:
            self.drawline.set_float_point(Vec2d(x, y))

    def update(self):
        maxg = 900
        #self.space.gravity = (randint(-maxg,maxg), randint(-maxg,maxg))
    def draw(self):
        if self.drawline != None:
            self.drawline.draw()
        for o in self.objects:
            o.update()
            o.draw()
        for w in self.widgets:
            w.draw()

    def input_start(self):
        self.input_active = True
        self.input_update_widget()

    def input_finish(self):
        self.input_text = ''
        self.widgets[2].set_text('')
        self.input_active = False

    def input_add_symbol(self, symbol):
        self.input_text += symbol
        self.input_update_widget()

    def input_backspace(self):
        print "before bs: %s" % self.input_text
        self.input_text = self.input_text[:-1]
        self.input_update_widget()
        print "after bs: %s" % self.input_text

    def input_symbol_printable(self, symbol):
        return True

    def input_update_widget(self):
        self.widgets[2].set_text(':'+self.input_text)

class PhysObject():
    def __init__(self):
        pass
    def draw(self):
        pass

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
            inertia = pymunk.moment_for_box(mass, 0, radius)
            body = pymunk.Body(mass, inertia)
        else:
            body = pymunk.Body(pymunk.inf, pymunk.inf)
        return body
    def _shape(self, body):
        shape = pymunk.Poly(body, self.points)
        return shape
    def add_to_space(self, space):
        if self.static == False:
            self.body.mass = pymunk.inf
            self.body.inertia = pymunk.inf
            space.add(self.shape, self.body)
        else:
            space.add_static(self.shape)
    def draw(self):
        ns = []
        for point in self.points:
            ns.append(point.x)
            ns.append(point.y)
        pyglet.gl.glColor4f(1.0,1.0,1.0,1.0)
        pyglet.graphics.draw(len(self.points), pyglet.gl.GL_POLYGON, ('v2f', ns))
        pyglet.gl.glColor4f(1.0,0.0,0.0,1.0)
        pyglet.graphics.draw(len(self.points), pyglet.gl.GL_POINTS, ('v2f', ns))
    def update(self):
        self.points = self.shape.get_points()

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
    def __init__(self, text='', position=Vec2d(10,10)):
        self.position = position
        self.text = text
        self.label = pyglet.text.Label(self.text,
              font_name='Monospace',
              font_size=8,
              x=self.position.x, y=self.position.y,
              anchor_x='left', anchor_y='center')
    def set_text(self, text):
        self.label.text = text
    def draw(self):
        pyglet.gl.glColor4f(0.0,1.0,1.0,0.8)
        self.label.draw()
