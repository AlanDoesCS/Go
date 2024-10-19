import tkinter as tk
from game_logic import GameLogic


class GoBoard:
    def __init__(self, window, canvas_size=500, size=19, margin=30):
        self.window = window
        self.canvas_size = canvas_size
        self.size = size
        self.margin = margin
        self.cell_size = (canvas_size - 2 * margin) / (size - 1)
        self.canvas = tk.Canvas(window, width=canvas_size, height=canvas_size)
        self.canvas.pack()
        self.logic = GameLogic(size)
        self.current_color = "black"  # black always starts
        self.bg_color = "#e0c69d"  # board color
        self.create_board()

        self.canvas.bind("<Button-1>", self.place_stone)  # left click

    def create_board(self):
        self.canvas.create_rectangle(0, 0, self.canvas_size, self.canvas_size, fill=self.bg_color,
                                     outline=self.bg_color)

        for i in range(self.size):
            x0, y0 = self.margin, self.margin + i * self.cell_size
            x1, y1 = self.canvas_size - self.margin, self.margin + i * self.cell_size
            self.canvas.create_line(x0, y0, x1, y1)

            x0, y0 = self.margin + i * self.cell_size, self.margin
            x1, y1 = self.margin + i * self.cell_size, self.canvas_size - self.margin
            self.canvas.create_line(x0, y0, x1, y1)

        match self.size:
            case 19:
                star_points = [
                    (3, 3), (3, 9), (3, 15),
                    (9, 3), (9, 9), (9, 15),
                    (15, 3), (15, 9), (15, 15)]
            case 13:
                star_points = [
                    (3, 3), (3, 9),
                    (9, 3), (9, 9),
                    (6, 6)]
            case 9:
                star_points = [
                    (2, 2), (2, 6),
                    (6, 2), (6, 6),
                    (4, 4)]
            case _:
                star_points = []

        for point in star_points:
            x = self.margin + point[1] * self.cell_size
            y = self.margin + point[0] * self.cell_size
            radius = 3
            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="black")

    def place_stone(self, event):
        row = round((event.y - self.margin) / self.cell_size)
        col = round((event.x - self.margin) / self.cell_size)

        if 0 <= row < self.size and 0 <= col < self.size and (row, col) not in self.logic.stones:
            if self.logic.is_valid_move(row, col, self.current_color):
                self.add_stone(row, col)
                captured_stones = self.logic.check_captures(row, col, self.current_color)
                if captured_stones:
                    self.remove_captured_stones(captured_stones)
                self.current_color = "white" if self.current_color == "black" else "black"

    def add_stone(self, row, col):
        x = self.margin + col * self.cell_size
        y = self.margin + row * self.cell_size
        radius = self.cell_size / 2.5

        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=self.current_color, outline="")

        self.logic.stones[(row, col)] = self.current_color

    def remove_captured_stones(self, captured_stones):
        for (row, col) in captured_stones:
            if (row, col) in self.logic.stones:
                del self.logic.stones[(row, col)]

            x = self.margin + col * self.cell_size
            y = self.margin + row * self.cell_size
            radius = self.cell_size / 2.5

            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=self.bg_color,
                                    outline=self.bg_color)

            # Vertical Line
            x0, y0 = x, y - self.cell_size / 2
            x1, y1 = x, y + self.cell_size / 2
            self.canvas.create_line(x0, y0, x1, y1)

            # Horizontal line
            x0, y0 = x - self.cell_size / 2, y
            x1, y1 = x + self.cell_size / 2, y
            self.canvas.create_line(x0, y0, x1, y1)


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Go Board")

    board = GoBoard(window, size=19)

    window.mainloop()
