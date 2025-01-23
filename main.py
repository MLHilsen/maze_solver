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



def main():
    win = Window(800, 600)

    pt1 = Point(0, 0)
    pt2 = Point(500, 500)
    l1 = Line(pt1, pt2)

    win.draw_line(l1, "red")

    win.wait_for_close()

main()