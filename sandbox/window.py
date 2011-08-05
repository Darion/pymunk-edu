# -*- encoding: utf-8 -*-
import pyglet
from pyglet.window import key
from pyglet.window import mouse
import pymunk
from pymunk import Vec2d
from draw import PygletDraw
from widget import *
from physobject import *
from utils import *
from cli import *

class Window(pyglet.window.Window):
    objects = []
    widgets = {}
    drawline = None
    drawmode = 1
    DRAWMODE_RIGID = 1
    DRAWMODE_STATIC = 2
    fig = 'polygon'
    def __init__(self, *args, **kwargs):
        self.log = Log()
        pyglet.window.Window.__init__(self, *args, **kwargs)
        self.init_physics()
        self.init_handlers()
        self.log.add('init widgets')
        self.append_widget('mode', Widget('rigid', Vec2d(10,25)))
        self.append_widget('fig', Widget('', Vec2d(10,40)))
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
            self.widgets['fig'].set_text(self.fig)
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
                if self.drawline.finished:
                    p = self.drawline.finish()
            elif button == mouse.RIGHT:
                p = self.drawline.finish()
            if (self.drawmode == self.DRAWMODE_STATIC):
                p.static = True
            if self.drawline.finished:
                p.add_to_space(self.space)
                self.objects.append(p)
                self.drawline = None
        else:
            #self.drawline = DrawLines('polygon')
            self.drawline = DrawLines(self.fig)
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
            elif symbol == key.L:
                self.fig = 'polygon'
            elif symbol == key.G:
                self.fig = 'segment'

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

# Класс, реализующий процесс "рисования" многоугольника
class DrawLines():
    points = []
    float_point = Vec2d(0,0)
    finished = False
    def __init__(self, fig):
        self.fig = fig
        if self.fig == 'polygon':
            self.points_amount = 0
        else:
            self.points_amount = 2
        self.points = []
    def add_point(self, point):
        self.points.append(point)
        if len(self.points) == self.points_amount:
            self.finished = True
    def set_float_point(self, point):
        self.float_point = point
    def finish(self):
        self.finished = True
        if self.fig == 'polygon':
            return Polygonal(self.points)
        elif self.fig == 'segment':
            return Segment(self.points[0], self.points[1], static=True)
    def draw(self):
        if len(self.points) > 1:
            last = self.points[0]
            for n in range(1, len(self.points)):
                current = self.points[n]
                PygletDraw.line(last, current)
                last = current
            PygletDraw.line(last, self.float_point)
