import random

class GameState:
    def __init__(self, player_positions, computer_positions, player_items, computer_items, wall_position, player_flag_pos, computer_flag_pos):
        self.player_positions = player_positions
        self.computer_positions = computer_positions
        self.player_items = player_items
        self.computer_items = computer_items
        self.wall_position = wall_position
        self.player_flag_pos = player_flag_pos
        self.computer_flag_pos = computer_flag_pos

    def clone(self):
        return GameState(
            self.player_positions.copy(),
            self.computer_positions.copy(),
            self.player_items.copy(),
            self.computer_items.copy(),
            self.wall_position,
            self.player_flag_pos,
            self.computer_flag_pos
        )

    def get_valid_moves(self, position, current):
        row, col = position
        potential_moves = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
        return [move for move in potential_moves if 0 <= move[0] < 6 and 0 <= move[1] < 7 and move not in current + [self.wall_position]]

    def make_move(self, is_computer, position, new_position):
        if is_computer:
            self._update_position(self.computer_positions, self.computer_items, position, new_position)
        else:
            self._update_position(self.player_positions, self.player_items, position, new_position)
        self._check_battle(is_computer, new_position)

    def _update_position(self, positions, items, old_pos, new_pos):
        positions.remove(old_pos)
        positions.append(new_pos)
        items[new_pos] = items.pop(old_pos)

    def _check_battle(self, is_computer, new_position):
        if new_position in (self.player_positions if is_computer else self.computer_positions):
            self.battle(is_computer, new_position)

    def battle(self, is_computer, position):
        attacker_items = self.computer_items if is_computer else self.player_items
        defender_items = self.player_items if is_computer else self.computer_items
        attacker_positions = self.computer_positions if is_computer else self.player_positions
        defender_positions = self.player_positions if is_computer else self.computer_positions

        attacker_item = attacker_items[position]
        defender_item = defender_items[position]
        result = self._determine_winner(attacker_item, defender_item, position, is_computer)

        if result == "Attacker":
            defender_positions.remove(position)
            defender_items.pop(position)
        else:
            attacker_positions.remove(position)
            attacker_items.pop(position)

    def _determine_winner(self, attacker_item, defender_item, position, is_computer):
        while attacker_item == defender_item:
            attacker_item = random.choice(['Rock', 'Paper', 'Scissors'])
            defender_item = random.choice(['Rock', 'Paper', 'Scissors'])
        if is_computer:
            self.computer_items[position] = attacker_item
            self.player_items[position] = defender_item
        else:
            self.player_items[position] = attacker_item
            self.computer_items[position] = defender_item
        return "Attacker" if self._is_winner(attacker_item, defender_item) else "Defender"

    def _is_winner(self, player_item, opponent_item):
        return (player_item == 'Rock' and opponent_item == 'Scissors') or \
               (player_item == 'Paper' and opponent_item == 'Rock') or \
               (player_item == 'Scissors' and opponent_item == 'Paper')

    def is_terminal(self):
        return 'Flag' not in self.player_items.values() or 'Flag' not in self.computer_items.values()

    def evaluate(self):
        if 'Flag' not in self.player_items.values():
            return float('inf')  # Computer wins
        if 'Flag' not in self.computer_items.values():
            return -float('inf')  # Player wins

        positional_score = self._calculate_positional_advantage()
        safety_score = self._calculate_piece_safety()
        winning_score = self._calculate_winning_score()
        mobility_score = self._calculate_mobility_score()
        control_score = self._calculate_central_control_score()
        threat_defense_score = self._calculate_threat_defense_score()

        return positional_score + safety_score + winning_score + mobility_score + control_score + threat_defense_score

    def _calculate_mobility_score(self):
        score = 0
        for pos in self.computer_positions:
            score += len(self.get_valid_moves(pos, self.computer_positions))
        for pos in self.player_positions:
            score -= len(self.get_valid_moves(pos, self.player_positions))
        return score

    def _calculate_central_control_score(self):
        center_positions = [(2, 3), (3, 3), (2, 4), (3, 4)]
        score = 0
        for pos in self.computer_positions:
            if pos in center_positions:
                score += 5
        for pos in self.player_positions:
            if pos in center_positions:
                score -= 5
        return score

    def _calculate_threat_defense_score(self):
        score = 0
        for pos in self.computer_positions:
            if pos in self.player_positions:
                score += 10  # Threatening an opponent piece
        for pos in self.player_positions:
            if pos in self.computer_positions:
                score -= 10  # Opponent threatening a piece
        return score

    def _calculate_positional_advantage(self):
        score = 0
        for pos in self.computer_positions:
            score -= self._distance(pos, self.player_flag_pos)  # Closer to player's flag is better
        for pos in self.player_positions:
            score += self._distance(pos, self.computer_flag_pos)  # Closer to computer's flag is worse
        return score
    def _calculate_mobility_score(self):
        score = 0
        for pos in self.computer_positions:
            score += len(self.get_valid_moves(pos, self.computer_positions))
        for pos in self.player_positions:
            score -= len(self.get_valid_moves(pos, self.player_positions))
        return score

    def _calculate_central_control_score(self):
        center_positions = [(2, 3), (3, 3), (2, 4), (3, 4)]
        score = 0
        for pos in self.computer_positions:
            if pos in center_positions:
                score += 5
        for pos in self.player_positions:
            if pos in center_positions:
                score -= 5
        return score

    def _calculate_threat_defense_score(self):
        score = 0
        for pos in self.computer_positions:
            if pos in self.player_positions:
                score += 10  # Threatening an opponent piece
        for pos in self.player_positions:
            if pos in self.computer_positions:
                score -= 10  # Opponent threatening a piece
        return score

    def _calculate_winning_score(self):
        score = 0
        for pos in self.computer_positions:
            score += self._evaluate_fight_outcome(pos, self.player_positions, self.computer_items, self.player_items)
        for pos in self.player_positions:
            score -= self._evaluate_fight_outcome(pos, self.computer_positions, self.player_items, self.computer_items)
        return score

    def _evaluate_fight_outcome(self, position, opponent_positions, own_items, opponent_items):
        score = 0
        if position in opponent_positions:
            opponent_item = opponent_items[position]
            own_item = own_items[position]
            if self._is_winner(own_item, opponent_item):
                score += 1000  # High score for winning a fight
            else:
                score -= 20  # Low score for losing a fight
        return score
    def _calculate_piece_safety(self):
        score = 0
        for pos in self.computer_positions:
            if pos == self.computer_flag_pos:
                score += 10  # High value for flag safety
        for pos in self.player_positions:
            if pos == self.player_flag_pos:
                score -= 10  # High value for opponent flag safety
        return score
    def _distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    def minimax_alpha_beta(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.is_terminal():
            return self.evaluate()

        if maximizing_player:
            return self._maximize(depth, alpha, beta)
        else:
            return self._minimize(depth, alpha, beta)

    def _maximize(self, depth, alpha, beta):
        max_eval = float('-inf')
        for position in self.computer_positions:
            for move in self.get_valid_moves(position, self.computer_positions):
                cloned_state = self.clone()
                cloned_state.make_move(True, position, move)
                eval = cloned_state.minimax_alpha_beta(depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval

    def _minimize(self, depth, alpha, beta):
        min_eval = float('inf')
        for position in self.player_positions:
            for move in self.get_valid_moves(position, self.player_positions):
                cloned_state = self.clone()
                cloned_state.make_move(False, position, move)
                eval = cloned_state.minimax_alpha_beta(depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval
