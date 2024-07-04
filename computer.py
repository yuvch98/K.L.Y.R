from player import Player

class Computer(Player):
    def __init__(self, positions, items):
        super().__init__(positions, items)

    def make_best_move(self, game_state, game_logic):
        best_move = None
        best_score = -float('inf')
        for position in self.positions:
            for move in game_state.get_valid_moves(position, self.positions):
                cloned_state = game_state.clone()
                cloned_state.make_move(True, position, move)
                score = cloned_state.minimax_alpha_beta(2, -float('inf'), float('inf'), True)
                if score > best_score:
                    best_score = score
                    best_move = (position, move)
        if best_move:
            game_logic.move_and_battle(self, game_logic.player, best_move[0], best_move[1], is_computer=True)
            game_logic.check_victory()
