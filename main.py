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

# Game loop
player = Player([(5, col) for col in range(7)] + [(4, col) for col in range(7)], {pos: random.choice(['Rock', 'Paper', 'Scissors']) for pos in [(5, col) for col in range(7)] + [(4, col) for col in range(7)]})
computer = Computer([(0, col) for col in range(7)] + [(1, col) for col in range(7)], {pos: random.choice(['Rock', 'Paper', 'Scissors']) for pos in [(0, col) for col in range(7)] + [(1, col) for col in range(7)]})
game_logic = GameLogic(player, computer)
game = Game(game_logic)

running = True
selected_position = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if mouse_x >= 7 * constants.CELL_SIZE:  # Click is in the side column
                if game.handle_button_click(event, player):
                    print("Item's has been shuffled !")
            elif game.player_turn:
                row, col = mouse_y // constants.CELL_SIZE, mouse_x // constants.CELL_SIZE
                if selected_position:
                    if (row, col) in game_logic.get_valid_moves(selected_position, player.positions, game_logic.wall_position):
                        game_logic.move_and_battle(player, computer, selected_position, (row, col))
                        selected_position = None
                        game.player_turn = False
                    else:
                        selected_position = None
                else:
                    for pos in player.positions:
                        if pos == (row, col):
                            selected_position = pos
                            break

                game.draw_board()
                if selected_position:
                    game.draw_piece(selected_position, constants.COLORS['Player'], player.items[selected_position], selected=True)
                pygame.display.flip()
    if not game.player_turn:
        computer.make_best_move(game_logic)
        time.sleep(1)
        game.player_turn = True

    game.draw_board()
    if selected_position:
        game.draw_piece(selected_position, constants.COLORS['Player'], player.items[selected_position], selected=True)
    pygame.display.flip()

pygame.quit()
