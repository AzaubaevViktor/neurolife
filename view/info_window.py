from tkinter import Toplevel, Frame, Label, Listbox, SINGLE, END, Canvas

from model import World
from model.creature.neuro import Neuro


def beetween(a, x, b):
    return min(b, max(a, x))


class InfoWindow:
    def __init__(self, model: World):
        self.model = model

        self.window = Toplevel()
        self.window.title('Информация об объектах и мире')
        self.window.geometry("640x600+250+200")

        self.inner_init()
        self.frame.pack()

        self.window.mainloop()

    def inner_init(self):
        self.frame = Frame(self.window,
                           width=640,
                           height=600,
                           bd=2)
        self.frame.grid_bbox(2, 2)

        self._about_world()
        self._about_creatures()

    def _about_world(self):
        self.world_indo = self.model.info()

        TEXT = "Кол-во объектов: {cr_count}\n" \
               "Из них живые: {cr_alive}".format(**self.world_indo)
        Label(self.frame,
              text=TEXT).grid(row=1, column=1)

    def _about_creatures(self):
        lb = Listbox(self.frame,
                     height=15,
                     width=50,
                     selectmode=SINGLE)
        lb.bind('<<ListboxSelect>>', self._onselect)
        lb.grid(row=1, column=2)

        items = self.model.creatures.items()
        items = sorted(items, key=lambda k: k[0][0] * self.model.width + k[0][1])

        for (x, y), creature in items:
            lb.insert(END, [x, y, creature.life])

        self.canvas = NeuroCanvas(self.frame, (2, 2), 400, 300)

    def _onselect(self, evt):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        x, y, *_ = value[1:].split(",")
        x = int(x)
        y = int(y)
        cr = self.model.creatures[(x, y)]

        neuro = cr.genome

        self.canvas.draw(neuro)


class NeuroCanvas:
    def __init__(self, parent, grid, width, height):
        self.height = height
        self.width = width

        self.canvas = \
            Canvas(parent,
                   width=width,
                   height=height)
        self.canvas.grid(
                row=grid[0],
                column=grid[1]
        )
        self.canvas.create_rectangle(0, 0,
                                     width, height,
                                     fill='white')

    def draw(self, neuro: Neuro):
        self.neuro = neuro

        self.cols = max([max(x.size_left, x.size_right) for x in neuro.layers])
        self.rows = len(neuro.layers) + 1

        self.max_weight = 0
        for layer in neuro.layers:
            for section in layer.weights:
                for v in section:
                    if self.max_weight < abs(v):
                        self.max_weight = abs(v)

        self.color_coef = 1 / self.max_weight

        self.circle_diam = int(self.height / (self.cols + 1))
        self.d_row = (self.width - 2 * self.circle_diam) / (self.rows - 1)

        self._draw_all()

    def _draw_col(self, x, col_size):
        cd = self.circle_diam
        cr = cd / 2
        start = (cd - cr) / 2
        for y in range(col_size):
            self.canvas.create_oval(x + start, y * cd + start,
                                    x + start + cr, y * cd + start + cr)

    def _draw_weight(self, x, prev_n, next_n, weight):
        red, green = \
            (hex(-int(beetween(-1, weight, 0) * self.color_coef * 255))[2:],
             hex(int(beetween(0, weight, 1) * self.color_coef * 255))[2:])
        color = "#{:0>2}{:0>2}00".format(red, green)

        dr = self.d_row
        cr = self.circle_diam / 2
        cd = self.circle_diam

        self.canvas.create_line(
                x + cr, prev_n * cd + cr,
                x + dr + cr, next_n * cd + cr,
                fill=color,
                width=2
        )

    def _draw_all(self):
        count = 0

        dr = self.d_row

        for layer in self.neuro.layers:
            self._draw_col(count * dr, layer.size_left)
            self._draw_col((count + 1) * dr, layer.size_right)
            for p in range(layer.size_left):
                for n in range(layer.size_right):
                    self._draw_weight(count * dr, p, n,
                                      layer.weights[n][p])
            count += 1
