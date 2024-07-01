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

    def battle(self, opponent, position):
        player_item = self.items[position]
        opponent_item = opponent.items[position]
        result = determine_winner(player_item, opponent_item)
        print("Begining battle")
        print("Result is ", result)
        if result == "Player":
            opponent.positions.remove(position)
            opponent.items.pop(position)
        elif result == "Opponent":
            self.positions.remove(position)
            self.items.pop(position)

def determine_winner(player_item, opponent_item):
    if player_item == opponent_item:
        player_item = random.choice(['Rock', 'Paper', 'Scissors'])
        opponent_item = random.choice(['Rock', 'Paper', 'Scissors'])
    if (player_item == 'Rock' and opponent_item == 'Scissors') or (
            player_item == 'Paper' and opponent_item == 'Rock') or (
            player_item == 'Scissors' and opponent_item == 'Paper'):
        return "Player"
    if opponent_item == 'Flag':
        return "Player"
    else:
        return "Opponent"