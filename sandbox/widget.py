import pyglet
from pymunk import Vec2d

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
