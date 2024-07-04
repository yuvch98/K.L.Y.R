# game_logic.py
import random
import sys
import tkinter as tk
from tkinter import messagebox
import pygame


def show_message_box(message):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showinfo("Game Over", message)
    root.destroy()


class GameLogic:
    def __init__(self, player, computer):
        self.player = player
        self.computer = computer
        self.wall_position = (random.randint(2, 3), random.randint(0, 6))

    def move_and_battle(self, player, opponent, position, new_position, is_computer=False):
        player.move(position, new_position)
        if new_position in opponent.positions:
            self.battle(player, opponent, new_position, is_computer)
        self.check_victory()

    def check_victory(self):
        if 'Flag' not in self.player.items.values():
            show_message_box("Computer wins!")
            pygame.quit()
            sys.exit()
        if 'Flag' not in self.computer.items.values():
            show_message_box("Player wins!")
            pygame.quit()
            sys.exit()

    def determine_winner(self, player_item, opponent_item, position, is_computer):
        while player_item == opponent_item:
            player_item = random.choice(['Rock', 'Paper', 'Scissors'])
            opponent_item = random.choice(['Rock', 'Paper', 'Scissors'])
        if is_computer:
            self.computer.items[position] = player_item
            self.player.items[position] = opponent_item
        else:
            self.player.items[position] = player_item
            self.computer.items[position] = opponent_item
        if (player_item == 'Rock' and opponent_item == 'Scissors') or \
           (player_item == 'Paper' and opponent_item == 'Rock') or \
           (player_item == 'Scissors' and opponent_item == 'Paper'):
            return "Attacker"
        if opponent_item == 'Flag':
            return "Attacker"
        else:
            return "Defender"

    def battle(self, attacker, defender, position, is_computer=False):
        attacker_item = attacker.items[position]
        defender_item = defender.items[position]
        result = self.determine_winner(attacker_item, defender_item, position, is_computer)
        print("Beginning battle")
        if result == "Attacker":
            print("Attacker Won")
            defender.positions.remove(position)
            defender.items.pop(position)
        else:
            print("Defender Won")
            attacker.positions.remove(position)
            attacker.items.pop(position)

    def get_valid_moves(self, position, other_positions, wall_position):
        row, col = position
        potential_moves = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
        valid_moves = [move for move in potential_moves if 0 <= move[0] < 6 and 0 <= move[1] < 7 and move not in other_positions + [wall_position]]
        return valid_moves
