class GameLogic:
    def __init__(self, size):
        self.size = size
        self.stones = {}

    def get_neighbors(self, row, col):
        neighbors = []
        if row > 0:
            neighbors.append((row - 1, col))
        if row < self.size - 1:
            neighbors.append((row + 1, col))
        if col > 0:
            neighbors.append((row, col - 1))
        if col < self.size - 1:
            neighbors.append((row, col + 1))
        return neighbors

    def get_liberties(self, row, col, visited=None):
        if visited is None:
            visited = set()
        visited.add((row, col))

        liberties = 0
        for neighbor in self.get_neighbors(row, col):
            if neighbor not in self.stones:
                liberties += 1
            elif self.stones[neighbor] == self.stones[(row, col)] and neighbor not in visited:
                liberties += self.get_liberties(neighbor[0], neighbor[1], visited)

        return liberties

    def is_valid_move(self, row, col, color):
        self.stones[(row, col)] = color
        if self.get_liberties(row, col) > 0:
            del self.stones[(row, col)]
            return True
        else:
            opponent_color = "white" if color == "black" else "black"
            for neighbor in self.get_neighbors(row, col):
                if self.stones.get(neighbor) == opponent_color and self.get_liberties(*neighbor) == 0:
                    del self.stones[(row, col)]  # undo temporarily
                    return True

        del self.stones[(row, col)]  # undo
        return False

    def check_captures(self, row, col, color):
        opponent_color = "white" if color == "black" else "black"
        captured_stones = []
        for neighbor in self.get_neighbors(row, col):
            if self.stones.get(neighbor) == opponent_color and self.get_liberties(*neighbor) == 0:
                captured_stones.extend(self.capture_group(*neighbor))
        return captured_stones

    def capture_group(self, row, col):
        color = self.stones[(row, col)]
        to_capture = [(row, col)]
        captured = set()

        while to_capture:
            r, c = to_capture.pop()
            if (r, c) not in captured:
                captured.add((r, c))
                del self.stones[(r, c)]

                for neighbor in self.get_neighbors(r, c):
                    if self.stones.get(neighbor) == color:
                        to_capture.append(neighbor)

        return list(captured)
