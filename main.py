import random
import sys
import time
import tkinter as tk
from tkinter import messagebox
import pygame

#e Initialize pygame
pygame.init()

#e Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 700, 600
CELL_SIZE = SCREEN_WIDTH // 7
RADIUS = CELL_SIZE // 3
COLORS = {'Player': (0, 128, 255), 'Computer': (255, 128, 0), 'Empty': (255, 255, 255), 'Wall': (128, 128, 128), 'Aura': (0, 255, 0)}

#e Load images
rock_img = pygame.image.load('rock.png')
paper_img = pygame.image.load('paper.png')
scissors_img = pygame.image.load('scissors.png')
flag_img = pygame.image.load('red-flag.png')
images = {'Rock': rock_img, 'Paper': paper_img, 'Scissors': scissors_img, 'Flag': flag_img}

#e Scale images to fit the cell size
rock_img = pygame.transform.scale(rock_img, (CELL_SIZE, CELL_SIZE))
paper_img = pygame.transform.scale(paper_img, (CELL_SIZE, CELL_SIZE))
scissors_img = pygame.transform.scale(scissors_img, (CELL_SIZE, CELL_SIZE))
flag_img = pygame.transform.scale(flag_img, (CELL_SIZE,CELL_SIZE))

#e Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('K.L.Y.R')

#e Initial positions
player_positions = [(5, col) for col in range(7)] + [(4, col) for col in range(7)]
computer_positions = [(0, col) for col in range(7)] + [(1, col) for col in range(7)]
wall_position = (random.randint(2,3), random.randint(0,6))

#e Assign items to soldiers
player_items = {pos: random.choice(['Rock', 'Paper', 'Scissors']) for pos in player_positions}
computer_items = {pos: random.choice(['Rock', 'Paper', 'Scissors']) for pos in computer_positions}

#e Assign flag to one soldier for each player
player_flag_pos= random.choice(list(player_positions[:6]))
computer_flag_pos = random.choice(list(computer_positions[:6]))
player_items[player_flag_pos] = 'Flag'
computer_items[computer_flag_pos] = 'Flag'
#e Functions
def draw_board():
    screen.fill(COLORS['Empty'])
    for row in range(6):
        for col in range(7):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, COLORS['Empty'], rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)
    draw_pieces()

def draw_pieces():
    for pos in player_positions:
        draw_piece(pos, COLORS['Player'], player_items[pos])
    for pos in computer_positions:
        draw_piece(pos, COLORS['Computer'], computer_items[pos])
    draw_piece(wall_position, COLORS['Wall'], None)

def draw_piece(position, color, item, selected=False):
    row, col = position
    center = (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)
    if selected:
        pygame.draw.circle(screen, COLORS['Aura'], center, RADIUS + 5)
    pygame.draw.circle(screen, color, center, RADIUS)
    if item:
        screen.blit(images[item], (col * CELL_SIZE, row * CELL_SIZE))

def get_valid_moves(position, current):
    row, col = position
    potential_moves = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
    valid_moves = [move for move in potential_moves if 0 <= move[0] < 6 and 0 <= move[1] < 7 and move not in current + [wall_position]]
    return valid_moves

def player_move(position, new_position):
    global player_positions
    player_positions.remove(position)
    player_positions.append(new_position)
    player_items[new_position] = player_items.pop(position)
    check_victory()


def computer_move():
    global computer_positions

    best_move = None
    best_score = -float('inf')
    for position in computer_positions:
        for move in get_valid_moves(position, computer_positions):
            score = heuristic(move)
            if score > best_score:
                best_score = score
                best_move = (position, move)
    if best_move:
       computer_move_and_battle(computer_positions, computer_items, player_positions, player_items, best_move[0], best_move[1])
    check_victory()


def heuristic(position):
    # A simple heuristic: prefer moves that get closer to the player's flag
    player_flag_pos = list(player_items.keys())[list(player_items.values()).index('Flag')]
    row, col = position
    flag_row, flag_col = player_flag_pos
    return -abs(row - flag_row) - abs(col - flag_col)


def move_and_battle(player_positions, player_items, opponent_positions, opponent_items, position, new_position):
    player_positions.remove(position)
    player_positions.append(new_position)
    player_items[new_position] = player_items.pop(position)

    if new_position in opponent_positions:
        battle(player_positions, player_items, opponent_positions, opponent_items, new_position)

    check_victory()
def computer_move_and_battle(computer_positions, computer_items, opponent_positions, opponent_items, position, new_position):
    computer_positions.remove(position)
    computer_positions.append(new_position)
    computer_items[new_position] = computer_items.pop(position)

    if new_position in opponent_positions:
        battle(computer_positions, computer_items, opponent_positions, opponent_items, new_position)

    check_victory()


def battle(player_positions, player_items, opponent_positions, opponent_items, position):
    player_item = player_items[position]
    opponent_item = opponent_items[position]
    result = determine_winner(player_item, opponent_item)

    if result == "Player":
        opponent_positions.remove(position)
        opponent_items.pop(position)
    elif result == "Opponent":
        player_positions.remove(position)
        player_items.pop(position)

def determine_winner(player_item, opponent_item):
    if player_item == opponent_item:
        player_item = random.choice(['Rock', 'Paper', 'Scissors'])
        opponent_item = random.choice(['Rock', 'Paper', 'Scissors'])
    if (player_item == 'Rock' and opponent_item == 'Scissors') or (
            player_item == 'Paper' and opponent_item == 'Rock') or (
            player_item == 'Scissors' and opponent_item == 'Paper'):
        return "Player"
    if opponent_item == 'Flag':
        return "Player"
    else:
        return "Opponent"
def check_victory():
    if 'Flag' not in player_items.values():
        show_message_box("Computer wins!")
        pygame.quit()
        sys.exit()
    if 'Flag' not in computer_items.values():
        show_message_box("Player wins!")
        pygame.quit()
        sys.exit()


def show_message_box(message):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showinfo("Game Over", message)
    root.destroy()
# # Game loop
running = True
player_turn = True
selected_position = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and player_turn:
            mouse_x, mouse_y = event.pos
            row, col = mouse_y // CELL_SIZE, mouse_x // CELL_SIZE
            if selected_position:
                if (row, col) in get_valid_moves(selected_position, player_positions):
                    move_and_battle(player_positions, player_items, computer_positions, computer_items,
                                    selected_position, (row, col))
                    selected_position = None
                    player_turn = False
                else:
                    selected_position = None
            else:
                for pos in player_positions:
                    if pos == (row, col):
                        selected_position = pos
                        break

            draw_board()
            if selected_position:
                draw_piece(selected_position, COLORS['Player'], player_items[selected_position], selected=True)
            pygame.display.flip()
    if not player_turn:
        time.sleep(1)  # Wait for 2 seconds before computer's turn
        computer_move()
        player_turn = True

    draw_board()
    if selected_position:
        draw_piece(selected_position, COLORS['Player'], player_items[selected_position], selected=True)
    pygame.display.flip()

pygame.quit()