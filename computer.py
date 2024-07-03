# computer.py
from player import Player

class Computer(Player):
    def __init__(self, positions, items):
        super().__init__(positions, items)

    def heuristic(self, game_logic, position, new_position, player_flag_pos):
        score = 0
        row, col = new_position
        flag_row, flag_col = player_flag_pos
        score -= abs(row - flag_row) + abs(col - flag_col)  # Closer to the enemy flag

        # Battle evaluation
        if new_position in game_logic.player.positions:
            player_item = game_logic.player.items[new_position]
            computer_item = self.items[position]
            result = game_logic.determine_winner(computer_item, player_item)
            if result == "Attacker":
                score += 50  # Prioritize killing enemy soldier
            elif result == "Defender":
                score -= 50  # Strongly prioritize killing enemy soldier

        # Avoid compromising own flag
        for player_pos in game_logic.player.positions:
            player_item = game_logic.player.items[player_pos]
            computer_item = self.items[position]
            if game_logic.determine_winner(player_item, computer_item) == "Attacker":
                score -= 5

        # Avoid moving to the own flag position
        if new_position == self.flag_pos:
            score -= 50

        return score

    def make_best_move(self, game_logic):
        best_move = None
        best_score = -float('inf')
        for position in self.positions:
            for move in self.get_valid_moves(position, self.positions, game_logic.wall_position):
                score = self.heuristic(game_logic, position, move, game_logic.player.flag_pos)
                if score > best_score:
                    best_score = score
                    best_move = (position, move)
        if best_move:
            game_logic.move_and_battle(self, game_logic.player, best_move[0], best_move[1], is_computer=True)
            game_logic.check_victory()
