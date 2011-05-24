# -*- encoding: utf-8 -*-

import pyglet

class PygletDraw():
    """
    Отрисовка примитивов в Pyglet
    """
    @staticmethod
    def tetragon(coords):
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
    @staticmethod
    def point(coords):
        x = int(coords.x)
        y = int(coords.y)
        pyglet.graphics.draw(2, pyglet.gl.GL_POINTS,
                             ('v2i',
                                 (x, y, x, y)
                             ))

