import time

from player import Player


class Computer(Player):
    def __init__(self, positions, items):
        super().__init__(positions, items)
        self.flag_compromised = False

    def make_best_move(self, game_logic):
        self.shuffle_items_check(game_logic= game_logic)
        best_move = None
        best_score = -float('inf')
        for position in self.positions:
            for move in game_logic.get_valid_moves(position, self.positions, game_logic.wall_position):
                score = self._evaluate_move(old_pos=position, new_pos=move, game_logic=game_logic)
                if score > best_score:
                    best_score = score
                    best_move = (position, move)
        if best_move:
            game_logic.move_and_battle(self, game_logic.player, best_move[0], best_move[1], is_computer=True)
            game_logic.check_victory()

    def _evaluate_move(self, old_pos, new_pos, game_logic):
        # Heuristic evaluation function for a move
        score = 0
        score += self.is_winner(old_pos, new_pos, game_logic)
        score += self.distance_flag(new_pos, game_logic.player.flag_pos, game_logic)  # Add distance evaluation
        return score

    def distance_flag(self, start_pos, flag_pos, game_logic): # uses IDA*
        def heuristic(pos1, pos2):
            return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

        def search(path, g, bound): # Helper function for IDA*
            node = path[-1] # node = (0, 1)
            f = g + heuristic(node, flag_pos) # 0 + number
            if f > bound: # f == bound
                return f
            if node == flag_pos:
                return 'FOUND'
            min_bound = float('inf')
            for neighbor in get_neighbors(node):
                if neighbor not in path: # valid moves = neighbor
                    path.append(neighbor)
                    t = search(path, g + 1, bound)
                    if t == 'FOUND':
                        return 'FOUND'
                    if t < min_bound:
                        min_bound = t
                    path.pop()
            return min_bound

        def ida_star(root):
            bound = heuristic(root, flag_pos)
            path = [root]
            while True:
                t = search(path, 0, bound)
                if t == 'FOUND':
                    return len(path) - 1
                if t == float('inf'):
                    return float('inf')
                bound = t

        def get_neighbors(pos):
            row, col = pos
            neighbors = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
            valid_neighbors = [
                move for move in neighbors
                if 0 <= move[0] < 6 and 0 <= move[1] < 7
                and move not in game_logic.computer.positions
                and move != game_logic.wall_position
            ]
            return valid_neighbors

        distance = ida_star(start_pos)
        return -distance

    def is_winner(self, old_pos, new_pos, game_logic):
        score = 0
        if new_pos in game_logic.player.positions:
            player_item = game_logic.player.items[new_pos]
            computer_item = game_logic.computer.items[old_pos]
            if player_item == computer_item:
                score += 10  # worth taking the chance...
                return score
            if self.win(computer_item, player_item):
                score += 200
            #if it's a loss for the computer
            else:
                score -= 20
        return score

    def win(self, computer_item, opponent_item):
        if (computer_item == 'Rock' and opponent_item == 'Scissors') or \
                (computer_item == 'Paper' and opponent_item == 'Rock') or \
                (computer_item == 'Scissors' and opponent_item == 'Paper'):
            return True
        if opponent_item == 'Flag':
            return True
        else:
            return False

    def shuffle_items_check(self, game_logic):
        if self.flag_compromised: # if the computer already did shuffle
            return
        time.sleep(1)
        for position in self.positions:
            if position == self.flag_pos:
                for move in game_logic.get_valid_moves(position, self.positions, game_logic.wall_position):
                    if move in game_logic.player.positions:
                        self.flag_compromised = True
        if self.flag_compromised:
            self.shuffle_items()

