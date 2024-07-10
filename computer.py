from player import Player


class Computer(Player):
    def __init__(self, positions, items):
        super().__init__(positions, items)

    def make_best_move(self, game_logic):
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

    def distance_flag(self, start_pos, flag_pos, game_logic):
        # DFS to calculate the distance from start_pos to flag_pos
        stack = [(start_pos, 0)]  # (current_position, current_distance)
        visited = set()

        while stack:
            distance = 0
            current_pos, current_distance = stack.pop()
            if current_pos == flag_pos:
                return -current_distance  # Return negative distance to reward closer positions

            if current_pos in visited:
                continue
            visited.add(current_pos)

            row, col = current_pos
            neighbors = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
            valid_neighbors = [
                move for move in neighbors
                if 0 <= move[0] < 6 and 0 <= move[1] < 7
                and move not in visited
                and move not in game_logic.computer.positions
                and move != game_logic.wall_position
            ]

            for neighbor in valid_neighbors:
                stack.append((neighbor, current_distance + 1))
            distance-=1
        return distance  # If the flag is not reachable, return a large number

    def is_winner(self, old_pos, new_pos, game_logic):
        score = 0
        if new_pos in game_logic.player.positions:
            player_item = game_logic.player.items[new_pos]
            computer_item = game_logic.computer.items[old_pos]
            if player_item == computer_item:
                score += 10
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
