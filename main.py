from tkinter import Tk, BOTH, Canvas

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
    def __init__(self, x1, y1, x2, y2, canvas, top=True, bottom=True, left=True, right=True):
        self.has_top_wall = top
        self.has_bottom_wall = bottom
        self.has_left_wall = left
        self.has_right_wall = right
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self.pt_tl = Point(x1, y1) # Top left
        self.pt_bl = Point(x1, y2) # Bottom left
        self.pt_tr = Point(x2, y1) # Top right
        self.pt_br = Point(x2, y2) # Bottom right

        self._win = canvas

    def draw(self):
        top = Line(self.pt_tl, self.pt_tr)
        bottom = Line(self.pt_bl, self.pt_br)
        left = Line(self.pt_tl, self.pt_bl)
        right = Line(self.pt_tr, self.pt_br)

        if self.has_top_wall:
            self._win.draw_line(top, "red")

        if self.has_bottom_wall:
            self._win.draw_line(bottom, "red")

        if self.has_left_wall:
            self._win.draw_line(left, "red")

        if self.has_right_wall:
            self._win.draw_line(right, "red")



def main():
    win = Window(800, 600)

    pt1 = Point(0, 0)
    pt2 = Point(500, 500)
    l1 = Line(pt1, pt2)

    cell1 = Cell(10, 10, 100, 100, win, bottom=False)
    cell2 = Cell(110, 110, 210, 210, win)
    cell1.draw()
    cell2.draw()

    win.draw_line(l1, "red")

    win.wait_for_close()

main()