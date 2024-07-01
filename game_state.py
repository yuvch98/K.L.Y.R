from player import determine_winner
class GameState:
    def __init__(self, player_positions, computer_positions, player_items, computer_items, wall_position):
        self.player_positions = player_positions[:]
        self.computer_positions = computer_positions[:]
        self.player_items = player_items.copy()
        self.computer_items = computer_items.copy()
        self.wall_position = wall_position

    def get_valid_moves(self, position, current, wall_position):
        row, col = position
        potential_moves = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
        valid_moves = [move for move in potential_moves if 0 <= move[0] < 6 and 0 <= move[1] < 7 and move not in current + [wall_position]]
        return valid_moves

    def make_move(self, is_computer, position, new_position):
        if is_computer:
            self.computer_positions.remove(position)
            self.computer_positions.append(new_position)
            self.computer_items[new_position] = self.computer_items.pop(position)
        else:
            self.player_positions.remove(position)
            self.player_positions.append(new_position)
            self.player_items[new_position] = self.player_items.pop(position)

        if new_position in (self.player_positions if is_computer else self.computer_positions):
            self.battle(is_computer, new_position)

    def battle(self, is_computer, position):
        attacker_items = self.computer_items if is_computer else self.player_items
        defender_items = self.player_items if is_computer else self.computer_items
        attacker_positions = self.computer_positions if is_computer else self.player_positions
        defender_positions = self.player_positions if is_computer else self.computer_positions

        attacker_item = attacker_items[position]
        defender_item = defender_items[position]
        result = determine_winner(attacker_item, defender_item)

        if result == "Player":
            defender_positions.remove(position)
            defender_items.pop(position)
        elif result == "Computer":
            attacker_positions.remove(position)
            attacker_items.pop(position)

    def is_terminal(self):
        return 'Flag' not in self.player_items.values() or 'Flag' not in self.computer_items.values()

    def evaluate(self):
        if 'Flag' not in self.player_items.values():
            return float('inf')  # Computer wins
        if 'Flag' not in self.computer_items.values():
            return -float('inf')  # Player wins
        return 0  # Placeholder for more complex evaluation
