# player.py
import random
import tkinter as tk
from tkinter import messagebox


def show_message_box(message):
    """Displays a message box with the provided message."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showinfo("Shuffle", message)
    root.destroy()


class Player:
    def __init__(self, positions, items):
        """Initializes the player with positions and items."""
        self.positions = positions
        self.items = items
        self.flag_pos = random.choice(positions[:6])
        self.items[self.flag_pos] = 'Flag'

    def move(self, old_pos, new_pos):
        """Moves an item from old_pos to new_pos."""
        self.positions.remove(old_pos)
        self.positions.append(new_pos)
        self.items[new_pos] = self.items.pop(old_pos)

    def shuffle_items(self):
        """Shuffles items and places the flag in a new position."""
        for pos in self.positions:
            self.items[pos] = random.choice(['Rock', 'Paper', 'Scissors'])
        self.flag_pos = random.choice(self.positions)
        self.items[self.flag_pos] = 'Flag'
        show_message_box("Items have been shuffled!")
