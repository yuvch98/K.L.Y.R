import random
import sys
import constants
import time
import tkinter as tk
from tkinter import messagebox
import pygame
from player import Player
import game




# Game loop
game = game.Game()
running = True
player_turn = True
selected_position = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and player_turn:
            mouse_x, mouse_y = event.pos
            row, col = mouse_y // constants.CELL_SIZE, mouse_x // constants.CELL_SIZE
            if selected_position:
                if (row, col) in game.player.get_valid_moves(selected_position, game.player.positions, game.wall_position):
                    game.move_and_battle(game.player, game.computer, selected_position, (row, col))
                    selected_position = None
                    player_turn = False
                else:
                    selected_position = None
            else:
                for pos in game.player.positions:
                    if pos == (row, col):
                        selected_position = pos
                        break

            game.draw_board()
            if selected_position:
                game.draw_piece(selected_position, game.COLORS['Player'], game.player.items[selected_position], selected=True)
            pygame.display.flip()
    if not player_turn:
        time.sleep(1)
        game.computer.make_best_move(game)
        player_turn = True

    game.draw_board()
    if selected_position:
        game.draw_piece(selected_position, game.COLORS['Player'], game.player.items[selected_position], selected=True)
    pygame.display.flip()

pygame.quit()