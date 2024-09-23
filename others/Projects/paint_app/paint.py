from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Line
from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty, ObjectProperty
import json
import os

class PaintWidget(Widget):
    def __init__(self, **kwargs):
        super(PaintWidget, self).__init__(**kwargs)
        self.pen_down = False
        self.pen_color = (0, 0, 0, 1)  # 黑色
        self.pen_width = 2
        self.history = []
        self.current_index = -1

    def on_touch_down(self, touch):
        with self.canvas:
            Color(*self.pen_color)
            touch.ud['line'] = Line(points=(touch.x, touch.y), width=self.pen_width)
        self.pen_down = True
        self.history.append(self.canvas.get_group('line'))
        self.current_index += 1
        while len(self.history) > self.current_index + 1:
            del self.history[self.current_index + 1]

    def on_touch_move(self, touch):
        if self.pen_down:
            touch.ud['line'].points += [touch.x, touch.y]

    def on_touch_up(self, touch):
        self.pen_down = False

    def set_pen_color(self, color):
        self.pen_color = color

    def set_pen_width(self, width):
        self.pen_width = width

    def clear_canvas(self):
        self.canvas.clear()
        self.history = []
        self.current_index = -1

    def undo(self):
        if self.current_index >= 0:
            for line in self.history[self.current_index]:
                self.canvas.remove(line)
            self.current_index -= 1

    def save(self, filename):
        data = {
            "history": [],
            "current_index": self.current_index,
            "pen_color": list(self.pen_color),
            "pen_width": self.pen_width
        }
        for group in self.history:
            lines = []
            for line in group:
                points = line.points
                lines.append(points)
            data["history"].append(lines)

        with open(filename, 'w') as f:
            json.dump(data, f)

    def load(self, filename):
        if not os.path.exists(filename):
            return

        with open(filename, 'r') as f:
            data = json.load(f)
            self.history = []
            self.current_index = data["current_index"]
            self.pen_color = tuple(data["pen_color"])
            self.pen_width = data["pen_width"]

            for lines in data["history"]:
                with self.canvas:
                    for points in lines:
                        Color(*self.pen_color)
                        Line(points=points, width=self.pen_width)


class PaintApp(FloatLayout):
    menu_visible = BooleanProperty(False)
    pen_menu_visible = BooleanProperty(False)
    eraser_menu_visible = BooleanProperty(False)

    def toggle_menu(self):
        self.menu_visible = not self.menu_visible
        if self.menu_visible:
            self.ids.menu_layout.opacity = 1
        else:
            self.ids.menu_layout.opacity = 0

    def show_pen_options(self):
        self.pen_menu_visible = not self.pen_menu_visible
        if self.pen_menu_visible:
            self.ids.pen_menu_layout.opacity = 1
        else:
            self.ids.pen_menu_layout.opacity = 0

    def show_eraser_options(self):
        self.eraser_menu_visible = not self.eraser_menu_visible
        if self.eraser_menu_visible:
            self.ids.eraser_menu_layout.opacity = 1
        else:
            self.ids.eraser_menu_layout.opacity = 0

    def undo(self):
        self.ids.paint_widget.undo()

    def save(self):
        self.ids.paint_widget.save('paint_data.json')

    def load(self):
        self.ids.paint_widget.load('paint_data.json')

    def set_pen_color(self, color):
        self.ids.paint_widget.set_pen_color(color)

    def set_pen_width(self, width):
        self.ids.paint_widget.set_pen_width(width)


class MainApp(App):
    def build(self):
        return PaintApp()


if __name__ == '__main__':
    MainApp().run()
