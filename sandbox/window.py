import pyglet
from pyglet.window import key
from pyglet.window import mouse
import pymunk
from pymunk import Vec2d
from draw import PygletDraw
from cli import *

class Window(pyglet.window.Window):
    objects = []
    widgets = {}
    drawline = None
    drawmode = 1
    DRAWMODE_RIGID = 1
    DRAWMODE_STATIC = 2
    def __init__(self, *args, **kwargs):
        self.log = Log()
        pyglet.window.Window.__init__(self, *args, **kwargs)
        self.init_physics()
        self.init_handlers()
        self.log.add('init widgets')
        self.append_widget('mode', Widget('rigid', Vec2d(10,25)))
        self.append_widget('fps', Widget('null', Vec2d(10, 10)))
        self.append_widget('command', Widget('', Vec2d(10, 40)))
        self.append_widget('log', MlWidget('log', Vec2d(200, 10), 400))
        self.append_widget('object_info', MlWidget('', Vec2d(350, 450), 400))
        self.widgets['object_info'].label.anchor_y = 'top'
        self.widgets['object_info'].label.color = (0, 0, 128, 200)
        self.set_drawmode(self.DRAWMODE_RIGID)
        self.input_active = False
        self.input_text = ''
        self.paused = True
        self.step_on = False
        self.active_object = None
        # float!
        self.step_divisor = 50.0

    def append_widget(self, name, widget):
        self.widgets[name] = widget

    def set_drawmode(self, mode):
        self.drawmode = mode
        if mode == self.DRAWMODE_RIGID:
            self.widgets['mode'].set_text('rigid')
        elif mode == self.DRAWMODE_STATIC:
            self.widgets['mode'].set_text('static')
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
            if self.paused != False or self.step_on:
                self.space.step(1 / self.step_divisor)
                self.step_on = False
            self.draw()
            self.widgets['fps'].set_text("fps: %f" % pyglet.clock.get_fps())
            self.widgets['log'].set_text(self.log.tail(8))
            if self.active_object != None:
                self.widgets['object_info'].set_text(self.objects[self.active_object].debug_info())
            pyglet.clock.tick()
            self.flip()

    def pause(self):
        if self.paused:
            self.paused = False
        else:
            self.paused = True

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
            elif symbol == key.P:
                self.pause()
            elif symbol == key.T:
                self.step_on = True

    def on_text(self, symbol):
        if self.input_active:
            if ord(symbol) == 13:
                # if symbol - "enter key"
                command = Parser.parse(self.input_text)
                if command['type'] == 'set':
                    if command['params'][0] == 'gravity':
                        self.space.gravity = (0, -1 * float(command['params'][1]))
                        self.log.add('set gravity=%s' % command['params'][1])
                    elif command['params'][0] == 'step_divisor':
                        self.step_divisor = float(command['params'][1])
                        self.log.add('set step_divisor=%s' % command['params'][1])
                    elif command['params'][0] == 'active_object':
                        self.active_object = int(command['params'][1])
                        self.log.add('set active_object=%s' % command['params'][1])
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

    def draw(self):
        if self.drawline != None:
            self.drawline.draw()
        for i in range(0, len(self.objects)):
            o = self.objects[i]
            o.update()
            o.draw()
            o.draw_label(str(i))
        for w in self.widgets:
            self.widgets[w].draw()

    def input_start(self):
        self.input_active = True
        self.input_update_widget()

    def input_finish(self):
        self.input_text = ''
        self.widgets['command'].set_text('')
        self.input_active = False

    def input_add_symbol(self, symbol):
        self.input_text += symbol
        self.input_update_widget()

    def input_backspace(self):
        self.input_text = self.input_text[:-1]
        self.input_update_widget()

    def input_symbol_printable(self, symbol):
        return True

    def input_update_widget(self):
        self.widgets['command'].set_text(':'+self.input_text)

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

class MlWidget(Widget):
    def __init__(self, text='', position=Vec2d(10,10), width = 100):
        self.position = position
        self.text = text
        self.label = pyglet.text.Label(self.text,
              font_name='Monospace',
              font_size=8,
              x=self.position.x, y=self.position.y,
              anchor_x='left', anchor_y='bottom',
              width=width,
              multiline=True,
              )

class Log():
    TYPE_INFO = 0
    TYPE_WARNING = 1
    TYPE_ERROR = 2
    log = []
    def add(self, text, message_type=0):
        self.log.append([text, message_type])
    def tail(self, num):
        tail = self.log[-num:]
        return "\n".join([ line[0] for line in tail ])
