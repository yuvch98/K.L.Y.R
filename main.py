# main.py

import time
import pygame
import constants
from player import Player
from computer import Computer
from game import Game
from game_logic import GameLogic
import random

# Initialize Pygame
pygame.init()

# Initialize game components
player = Player(
    [(5, col) for col in range(7)] + [(4, col) for col in range(7)],
    {pos: random.choice(['Rock', 'Paper', 'Scissors']) for pos in [(5, col) for col in range(7)] + [(4, col) for col in range(7)]}
)
computer = Computer(
    [(0, col) for col in range(7)] + [(1, col) for col in range(7)],
    {pos: random.choice(['Rock', 'Paper', 'Scissors']) for pos in [(0, col) for col in range(7)] + [(1, col) for col in range(7)]}
)
game_logic = GameLogic(player, computer)
game = Game(game_logic)

# Game loop
running = True
selected_position = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the user closes the window
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:  # If the user clicks the mouse
            mouse_x, mouse_y = event.pos
            if mouse_x >= 7 * constants.CELL_SIZE:  # Click is in the side column (shuffle button)
                if game.handle_button_click(event, player):
                    print("Items have been shuffled!")
            elif game.player_turn:  # If it's the player's turn
                row, col = mouse_y // constants.CELL_SIZE, mouse_x // constants.CELL_SIZE
                if selected_position:
                    # If a position is selected, check if the move is valid
                    if (row, col) in game_logic.get_valid_moves(selected_position, player.positions, game_logic.wall_position):
                        game_logic.move_and_battle(player, computer, selected_position, (row, col))
                        selected_position = None
                        game.player_turn = False
                    else:
                        selected_position = None
                else:
                    # Select a position
                    for pos in player.positions:
                        if pos == (row, col):
                            selected_position = pos
                            break

                # Update the game display
                game.draw_board()
                if selected_position:
                    game.draw_piece(selected_position, constants.COLORS['Player'], player.items[selected_position], selected=True)
                pygame.display.flip()

    if not game.player_turn:  # If it's the computer's turn
        computer.make_best_move(game_logic)
        time.sleep(0.5)  # Delay for slower animation
        game.player_turn = True

    # Update the game display
    game.draw_board()
    if selected_position:
        game.draw_piece(selected_position, constants.COLORS['Player'], player.items[selected_position], selected=True)
    pygame.display.flip()

pygame.quit()
