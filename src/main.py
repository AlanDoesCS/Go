import tkinter as tk
from game_logic import GameLogic
from src.AlphaZero.mcts import MCTS


class GoBoard:
    def __init__(self, window, model, canvas_size=500, size=19, margin=30):
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
        self.model = model
        self.mcts = MCTS(self.model, self.logic, num_simulations=800)
        self.ai_mode = False

        # Load model weights for AI
        self.model.load_weights("alphazero_model.weights.h5")

        self.create_board()
        self.pass_button = tk.Button(window, text="Pass", command=self.pass_turn)
        self.pass_button.pack()
        self.ai_toggle_button = tk.Button(window, text="Toggle AI Mode", command=self.toggle_ai_mode)
        self.ai_toggle_button.pack()

        self.canvas.bind("<Button-1>", self.place_stone)  # left click

    def toggle_ai_mode(self):
        self.ai_mode = not self.ai_mode
        print(f"AI Mode is now {'enabled' if self.ai_mode else 'disabled'}.")

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
        if self.logic.is_game_over():
            print("Game already over!")
            return

        row = round((event.y - self.margin) / self.cell_size)
        col = round((event.x - self.margin) / self.cell_size)

        if 0 <= row < self.size and 0 <= col < self.size and (row, col) not in self.logic.stones:
            if self.logic.is_valid_move(row, col, self.current_color):
                self.add_stone(row, col)
                captured_stones = self.logic.check_captures(row, col, self.current_color)
                if captured_stones:
                    self.remove_captured_stones(captured_stones)

                # Switch to the next player
                self.current_color = "white" if self.current_color == "black" else "black"
                self.last_player_passed = False

                if self.ai_mode:
                    self.ai_move()

    def ai_move(self):
        print("AI is thinking...")
        state = self.logic.get_current_state()
        self.mcts.run_mcts(state, 1 if self.current_color == "black" else -1)
        action = self.mcts.select_action(state, temperature=0.1)  # Greedy move selection

        if action is None:
            print("AI passed.")
            self.pass_turn()
        else:
            row, col = action
            self.add_stone(row, col)
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

    def pass_turn(self):
        if self.last_player_passed:  # 2 passes in a row ends the game
            self.passed_twice = True
            print("Both players passed. Game over!")
            self.calculate_score()  # score calc
        else:
            self.last_player_passed = True
            self.current_color = "white" if self.current_color == "black" else "black"
            print(f"{self.current_color}'s turn to play.")

    def calculate_score(self):  # Chinese rules
        black_score = len([stone for stone in self.logic.stones.values() if stone == "black"])
        white_score = len([stone for stone in self.logic.stones.values() if stone == "white"])

        # Flood fill
        black_territory, white_territory = self.logic.calculate_territory()

        black_score += black_territory
        white_score += white_territory

        print(f"Final Score - Black: {black_score}, White: {white_score}")
        if black_score > white_score:
            print("Black wins!")
        elif white_score > black_score:
            print("White wins!")
        else:
            print("It's a tie!")


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Go Board")

    board = GoBoard(window, size=19)

    window.mainloop()
