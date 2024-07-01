import random
import sys
import tkinter as tk
from tkinter import messagebox
import pygame
from player import Player
from computer import Computer
import constants
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 700, 600
CELL_SIZE = SCREEN_WIDTH // 7

# Load images
rock_img = pygame.image.load('rock.png')
paper_img = pygame.image.load('paper.png')
scissors_img = pygame.image.load('scissors.png')
flag_img = pygame.image.load('red-flag.png')
images = {'Rock': rock_img, 'Paper': paper_img, 'Scissors': scissors_img, 'Flag': flag_img}

# Scale images to fit the cell size
rock_img = pygame.transform.scale(rock_img, (CELL_SIZE, CELL_SIZE))
paper_img = pygame.transform.scale(paper_img, (CELL_SIZE, CELL_SIZE))
scissors_img = pygame.transform.scale(scissors_img, (CELL_SIZE, CELL_SIZE))
flag_img = pygame.transform.scale(flag_img, (CELL_SIZE, CELL_SIZE))

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('K.L.Y.R')


# Helper functions
def show_message_box(message):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showinfo("Game Over", message)
    root.destroy()

class Game:
    def __init__(self):
        self.player = Player([(5, col) for col in range(7)] + [(4, col) for col in range(7)], {pos: random.choice(['Rock', 'Paper', 'Scissors']) for pos in [(5, col) for col in range(7)] + [(4, col) for col in range(7)]})
        self.computer = Computer([(0, col) for col in range(7)] + [(1, col) for col in range(7)], {pos: random.choice(['Rock', 'Paper', 'Scissors']) for pos in [(0, col) for col in range(7)] + [(1, col) for col in range(7)]})
        self.wall_position = (random.randint(2, 3), random.randint(0, 6))
        self.COLORS = {'Player': (0, 128, 255), 'Computer': (255, 128, 0), 'Empty': (255, 255, 255), 'Wall': (128, 128, 128), 'Aura': (0, 255, 0)}


    def draw_board(self):
        screen.fill(self.COLORS['Empty'])
        for row in range(6):
            for col in range(7):
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, self.COLORS['Empty'], rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)
        self.draw_pieces()

    def draw_pieces(self):
        for pos in self.player.positions:
            self.draw_piece(pos, self.COLORS['Player'], self.player.items[pos])
        for pos in self.computer.positions:
            self.draw_piece(pos, self.COLORS['Computer'], self.computer.items[pos])
        self.draw_piece(self.wall_position, self.COLORS['Wall'], None)

    def draw_piece(self, position, color, item, selected=False):
        row, col = position
        center = (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)
        if selected:
            pygame.draw.circle(screen, self.COLORS['Aura'], center, constants.RADIUS + 5)
        pygame.draw.circle(screen, color, center, constants.RADIUS)
        if item:
            screen.blit(images[item], (col * CELL_SIZE, row * CELL_SIZE))

    def move_and_battle(self, player, opponent, position, new_position,is_computer = False):
        player.move(position, new_position)
        if new_position in opponent.positions:
            player.battle(opponent, new_position, is_computer)
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
