# player.py
import random

class Player:
    def __init__(self, positions, items):
        self.positions = positions
        self.items = items
        self.flag_pos = random.choice(positions[:6])
        self.items[self.flag_pos] = 'Flag'

    def move(self, old_pos, new_pos):
        self.positions.remove(old_pos)
        self.positions.append(new_pos)
        self.items[new_pos] = self.items.pop(old_pos)

    def get_valid_moves(self, position, other_positions, wall_position):
        row, col = position
        potential_moves = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
        valid_moves = [move for move in potential_moves if 0 <= move[0] < 6 and 0 <= move[1] < 7 and move not in other_positions + [wall_position]]
        return valid_moves
    def shuffle_items(self):
        for pos in self.positions:
            self.items[pos] = random.choice(['Rock', 'Paper', 'Scissors'])
        flag_new_pos = random.choice(self.positions)
        self.items[flag_new_pos] = 'Flag'