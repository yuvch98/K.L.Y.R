# computer.py

from player import Player
from game_state import GameState
import game
from player import determine_winner

class Computer(Player):
    def __init__(self, positions, items):
        super().__init__(positions, items)

    def heuristic(self, state, position, new_position, player_flag_pos):
        score = 0
        row, col = new_position
        flag_row, flag_col = player_flag_pos
        score -= abs(row - flag_row) + abs(col - flag_col)  # Closer to the enemy flag

        # Battle evaluation
        if new_position in state.player.positions:
            player_item = state.player.items[new_position]
            computer_item = self.items[position]
            result = determine_winner(computer_item, player_item)
            if result == "Player":
                score += 50  # Prioritize killing enemy soldier
            elif result == "Opponent":
                score -= 50  # Strongly prioritize killing enemy soldier

        # Avoid compromising own flag
        for player_pos in state.player.positions:
            player_item = state.player.items[player_pos]
            computer_item = self.items[position]
            if determine_winner(player_item, computer_item) == "Player":
                score -= 5

        # Avoid moving to the own flag position
        if new_position == self.flag_pos:
            score -= 50

        return score

    def make_best_move(self, game):
        best_move = None
        best_score = -float('inf')
        for position in self.positions:
            for move in self.get_valid_moves(position, self.positions, game.wall_position):
                score = self.heuristic(game, position, move, game.player.flag_pos)
                if score > best_score:
                    best_score = score
                    best_move = (position, move)
        if best_move:
            game.move_and_battle(self, game.player, best_move[0], best_move[1], is_computer = True)
            game.check_victory()
