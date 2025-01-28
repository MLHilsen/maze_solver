from tkinter import Tk, BOTH, Canvas, Button, BooleanVar
import time, random

class Window():
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.__root = Tk()
        self.__root.title("Maze Solver")

        self.canvas = Canvas(self.__root, width=self.width, height=self.height, background="white")
        self.canvas.pack()

        self.running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def get_size(self):
        size_determined = BooleanVar()
        size_determined.set(False)

        def small():
            global num_cols
            global num_rows
            global cell_xy
            num_cols = 18
            num_rows = 20
            cell_xy = 30
            size_determined.set(True)

        button1 = Button(text="Small Maze", command=small)
        button1.place(x=50, y=50)

        def large():
            global num_cols
            global num_rows
            global cell_xy
            num_cols = 35
            num_rows = 50
            cell_xy = 15
            size_determined.set(True)

        button2 = Button(text="Large Maze", command=large)
        button2.place(x=200, y=50)

        self.__root.wait_variable(size_determined)
        
        button1.destroy()
        button2.destroy()
        

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True

        while self.running:
            self.redraw()

    def close(self):
        self.running = False

    def draw_line(self, Line, fill_color, w=2):
        Line.draw(self.canvas, fill_color, w)

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

    def draw(self, canvas, fill_color, w):
        canvas.create_line(
            self.x1, self.y1, self.x2, self.y2, fill=fill_color, width=w
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
        self.visited = False

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

        width = 3

        if self.has_top_wall:
            self._win.draw_line(top, "black", width)
        else:
            self._win.draw_line(top, "white", width)

        if self.has_bottom_wall:
            self._win.draw_line(bottom, "black", width)
        else:
            self._win.draw_line(bottom, "white", width)

        if self.has_left_wall:
            self._win.draw_line(left, "black", width)
        else:
            self._win.draw_line(left, "white", width)

        if self.has_right_wall:
            self._win.draw_line(right, "black", width)
        else:
            self._win.draw_line(right, "white", width)

    def draw_move(self, to_cell, undo=False):
        mid_x, mid_y = self.get_middle()
        pt1 = Point(mid_x, mid_y)

        mid_x, mid_y = to_cell.get_middle()
        pt2 = Point(mid_x, mid_y)

        ln1 = Line(pt1, pt2)

        if undo:
            self._win.draw_line(ln1, "white", 4)
            self._win.draw_line(ln1, "grey")
        else:
            self._win.draw_line(ln1, "red", 4)

class Maze():
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, canvas, seed=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._win = canvas
        self._cells = []
        if seed != None:
            seed = random.seed(seed)

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
        #self._animate() # Comment out to skip maze creation cinematic

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)

        self._cells[self.num_rows - 1][self.num_cols - 1].has_bottom_wall = False
        self._draw_cell(self.num_rows - 1, self.num_cols - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True

        while True:
            valid_directions = []

            try:
                if (i - 1 > 0) and (self._cells[i - 1][j].visited == False): # Check Up
                    valid_directions.append("up")
            except:
                pass
            try:
                if (i + 1 < self.num_rows) and self._cells[i + 1][j].visited == False: # Check Down
                    valid_directions.append("down")
            except:
                pass
            try:
                if (j - 1 > 0) and self._cells[i][j - 1].visited == False: # Check Left
                    valid_directions.append("left")
            except:
                pass
            try:
                if (j + 1 < self.num_cols) and self._cells[i][j + 1].visited == False: # Check Right
                    valid_directions.append("right")
            except:
                pass

            if len(valid_directions) == 0:
                self._draw_cell(i, j)
                break
            
            dir = random.choice(valid_directions)

            if dir == "up":
                self._cells[i][j].has_top_wall = False
                self._cells[i - 1][j].has_bottom_wall = False
                self._break_walls_r(i - 1, j)

            if dir == "down":
                self._cells[i][j].has_bottom_wall = False
                self._cells[i + 1][j].has_top_wall = False
                self._break_walls_r(i + 1, j)

            if dir == "left":
                self._cells[i][j].has_left_wall = False
                self._cells[i][j - 1].has_right_wall = False
                self._break_walls_r(i, j - 1)

            if dir == "right":
                self._cells[i][j].has_right_wall = False
                self._cells[i][j + 1].has_left_wall = False
                self._break_walls_r(i, j + 1)

    def _reset_cells_visited(self):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._cells[i][j].visited = False

    def solve(self):
        return self._solve_r(0, 0)
    
    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True

        if (i == self.num_rows - 1) and (j == self.num_cols - 1):
            return True
        
        if (i - 1 > 0) and (self._cells[i][j].has_top_wall == False) and (self._cells[i - 1][j].visited == False): # Check Up
            self._cells[i][j].draw_move(self._cells[i - 1][j])

            if self._solve_r(i - 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i - 1][j], undo=True)

        if (i + 1 < self.num_rows) and (self._cells[i][j].has_bottom_wall == False) and (self._cells[i + 1][j].visited == False): # Check Down
            self._cells[i][j].draw_move(self._cells[i + 1][j])

            if self._solve_r(i + 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i + 1][j], undo=True)

        if (j - 1 > 0) and (self._cells[i][j].has_left_wall == False) and (self._cells[i][j - 1].visited == False): # Check Left
            self._cells[i][j].draw_move(self._cells[i][j - 1])

            if self._solve_r(i, j - 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j - 1], undo=True)

        if (j + 1 < self.num_cols) and (self._cells[i][j].has_right_wall == False) and (self._cells[i][j + 1].visited == False): # Check Right
            self._cells[i][j].draw_move(self._cells[i][j + 1])

            if self._solve_r(i, j + 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j + 1], undo=True)

        return False


    def _animate(self):
        #return
        self._win.redraw()
        time.sleep(0.0001)


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

    padding_x, padding_y = 10, 10
    # num_cols = 35
    # num_rows = 50
    # cell_xy = 15

    win.get_size()    

    maze = Maze(padding_x,
                padding_y,
                num_cols,
                num_rows,
                cell_xy,
                cell_xy,
                win)
    
    maze._create_cells()
    maze._break_entrance_and_exit()
    maze._break_walls_r(0, 0)
    maze._reset_cells_visited()
    maze.solve()

    win.wait_for_close()

main()