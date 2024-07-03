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

# Button position
button_x = constants.SCREEN_WIDTH - constants.BUTTON_WIDTH - 10
button_y = constants.SCREEN_HEIGHT - constants.BUTTON_HEIGHT - 10

running = True
player_turn = True
selected_position = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            button_rect = pygame.Rect(button_x, button_y, constants.BUTTON_WIDTH, constants.BUTTON_HEIGHT)
            if button_rect.collidepoint(event.pos):
                game.handle_button_click(event, player)
            elif player_turn:
                row, col = mouse_y // constants.CELL_SIZE, mouse_x // constants.CELL_SIZE
                if selected_position:
                    if (row, col) in player.get_valid_moves(selected_position, player.positions, game_logic.wall_position):
                        game_logic.move_and_battle(player, computer, selected_position, (row, col))
                        selected_position = None
                        player_turn = False
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
    if not player_turn:
        time.sleep(1)
        computer.make_best_move(game_logic)
        player_turn = True

    game.draw_board()
    button_rect = pygame.Rect(button_x, button_y, constants.BUTTON_WIDTH, constants.BUTTON_HEIGHT)
    game.draw_button(button_rect)
    if selected_position:
        game.draw_piece(selected_position, constants.COLORS['Player'], player.items[selected_position], selected=True)
    pygame.display.flip()

pygame.quit()
