from tkinter import Tk, BOTH, Canvas
import time

class Window():
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.__root = Tk()
        self.__root.title("Title")

        self.canvas = Canvas(self.__root, width=self.width, height=self.height)
        self.canvas.pack()

        self.running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True

        while self.running:
            self.redraw()

    def close(self):
        self.running = False

    def draw_line(self, Line, fill_color):
        Line.draw(self.canvas, fill_color)

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line():
    def __init__(self, pt1, pt2):
        self.x1 = pt1.x
        self.x2 = pt2.x
        self.y1 = pt1.y
        self.y2 = pt2.y

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.x1, self.y1, self.x2, self.y2, fill=fill_color, width=2
        )

class Cell():
    def __init__(self, canvas):
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.has_left_wall = True
        self.has_right_wall = True
        self._x1 = None
        self._y1 = None
        self._x2 = None
        self._y2 = None

        self._win = canvas

    def get_middle(self):
        mid_x = (self._x1 + self._x2) / 2
        mid_y = (self._y1 + self._y2) / 2

        return mid_x, mid_y

    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2

        pt_tl = Point(x1, y1) # Top left
        pt_bl = Point(x1, y2) # Bottom left
        pt_tr = Point(x2, y1) # Top right
        pt_br = Point(x2, y2) # Bottom right
    
        top = Line(pt_tl, pt_tr)
        bottom = Line(pt_bl, pt_br)
        left = Line(pt_tl, pt_bl)
        right = Line(pt_tr, pt_br)

        if self.has_top_wall:
            self._win.draw_line(top, "red")

        if self.has_bottom_wall:
            self._win.draw_line(bottom, "red")

        if self.has_left_wall:
            self._win.draw_line(left, "red")

        if self.has_right_wall:
            self._win.draw_line(right, "red")

    def draw_move(self, to_cell, undo=False):
        mid_x, mid_y = self.get_middle()
        pt1 = Point(mid_x, mid_y)

        mid_x, mid_y = to_cell.get_middle()
        pt2 = Point(mid_x, mid_y)

        ln1 = Line(pt1, pt2)

        if undo:
            self._win.draw_line(ln1, "grey")
        else:
            self._win.draw_line(ln1, "red")

class Maze():
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, canvas):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._win = canvas
        self._cells = []

    def _create_cells(self):
        for i in range(self.num_rows):
            row = []
            for j in range(self.num_cols):
                row.append(Cell(self._win))
            self._cells.append(row)

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        x1 = self.x1 + (j * self.cell_size_x)
        y1 = self.y1 + (i * self.cell_size_y)
        x2 = self.x1 + (j * self.cell_size_x) + self.cell_size_x
        y2 = self.y1 + (i * self.cell_size_y) + self.cell_size_y

        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        self._win.redraw()
        time.sleep(0.01)


def main():
    win = Window(800, 600)

    '''
    cell1 = Cell(win)
    cell1.has_top_wall = False

    cell2 = Cell(win)
    cell1.draw(10, 10, 100, 100)
    cell2.draw(110, 10, 200, 100)

    cell1.draw_move(cell2)
    '''

    maze = Maze(10, 10, 20, 20, 20, 20, win)
    maze._create_cells()

    win.wait_for_close()

main()