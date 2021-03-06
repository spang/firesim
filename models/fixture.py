import logging as log
import colorsys
import random

from PySide import QtCore

from ui.fixturewidget import FixtureWidget


class Fixture:

    def __init__(self, data=None, controller=None):
        self.strand = 0
        self.address = 0
        self.type = "linear"
        self.pixels = 32
        self.pos1 = (10, 10)
        self.pos2 = (50, 50)
        self.locked = False

        if data is not None:
            self.unpack(data)

        self.widget = None
        self.controller = controller

        self.pixel_data = [(0, 0, 0)] * self.pixels

    def __repr__(self):
        return "[%d:%d]*%d" % (self.strand, self.address, self.pixels)

    def destroy(self):
        self.widget.deleteLater()

    def request_destruction(self):
        self.controller.delete_fixture(self)

    def get_widget(self):
        if self.widget is None:
            self.widget = FixtureWidget(self.controller.get_canvas(), model=self)
            x, y = self.pos1[0], self.pos1[1]
            self.widget.setPos(x, y)
            #self.widget.setRotation(self.angle)
        return self.widget

    def unpack(self, data):
        self.strand = data.get("strand", 0)
        self.address = data.get("address", 0)
        self.type = data.get("type", "")
        self.pixels = data.get("pixels", 0)
        self.pos1 = data.get("pos1", [0, 0])
        self.pos2 = data.get("pos2", [0, 0])

    def pack(self):
        return {
                'strand': self.strand,
                'address': self.address,
                'type': self.type,
                'pixels': self.pixels,
                'pos1': self.pos1,
                'pos2': self.pos2
                }

    def fixture_move_callback(self, fixture):
        self.pos1 = map(int, fixture.drag1.pos().toTuple())
        self.pos2 = map(int, fixture.drag2.pos().toTuple())
        fixture.update_geometry()

    def blackout(self):
        self.pixel_data = [(0, 0, 0)] * self.pixels
        self.widget.update()

    def set(self, pixel, color):
        assert isinstance(color, tuple), "Color must be a 3-tuple (R, G, B)"
        self.pixel_data[pixel] = color
        self.widget.update()

    def set_all(self, color):
        assert isinstance(color, tuple), "Color must be a 3-tuple (R, G, B)"
        self.pixel_data = [color] * self.pixels
        self.widget.update()

    def random_color(self):
        r, g, b = [int(255.0 * c) for c in colorsys.hsv_to_rgb(random.random(), 1.0, 1.0)]
        self.set_all((r, g, b))