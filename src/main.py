import tkinter as tk


def create_board(window, canvas_size=500, size=19, margin=20):
    cell_size = (canvas_size - 2 * margin) / (size - 1)

    canvas = tk.Canvas(window, width=canvas_size, height=canvas_size)
    canvas.pack()

    for i in range(size):
        x0, y0 = margin, margin + i * cell_size
        x1, y1 = canvas_size - margin, margin + i * cell_size
        canvas.create_line(x0, y0, x1, y1)

        x0, y0 = margin + i * cell_size, margin
        x1, y1 = margin + i * cell_size, canvas_size - margin
        canvas.create_line(x0, y0, x1, y1)

    match size:
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
        x = margin + point[1] * cell_size
        y = margin + point[0] * cell_size
        radius = 3
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="black")


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Go Board")

    create_board(window, size=9)

    window.mainloop()
