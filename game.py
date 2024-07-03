# game.py
import pygame
import constants
from player import Player
from computer import Computer

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
FONT = pygame.font.Font(None, 36)
class Game:
    def __init__(self, logic):
        self.logic = logic
        self.COLORS = constants.COLORS
        self.shuffle_used = False
    def draw_board(self):
        screen.fill(self.COLORS['Empty'])
        for row in range(6):
            for col in range(7):
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, self.COLORS['Empty'], rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)
        self.draw_pieces()

    def draw_pieces(self):
        for pos in self.logic.player.positions:
            self.draw_piece(pos, self.COLORS['Player'], self.logic.player.items[pos])
        for pos in self.logic.computer.positions:
            self.draw_piece(pos, self.COLORS['Computer'], self.logic.computer.items[pos])
        self.draw_piece(self.logic.wall_position, self.COLORS['Wall'], None)

    def draw_piece(self, position, color, item, selected=False):
        row, col = position
        center = (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)
        if selected:
            pygame.draw.circle(screen, self.COLORS['Aura'], center, constants.RADIUS + 5)
        pygame.draw.circle(screen, color, center, constants.RADIUS)
        if item:
            screen.blit(images[item], (col * CELL_SIZE, row * CELL_SIZE))

    def draw_button(self, button_rect):
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, constants.BUTTON_HOVER_COLOR, button_rect)
        else:
            pygame.draw.rect(screen, constants.BUTTON_COLOR, button_rect)
        text = FONT.render('Shuffle', True, constants.BUTTON_TEXT_COLOR)
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)

    def handle_button_click(self, event, player):
        button_rect = pygame.Rect(constants.SCREEN_WIDTH - constants.BUTTON_WIDTH - 10,
                                  constants.SCREEN_HEIGHT - constants.BUTTON_HEIGHT - 10, constants.BUTTON_WIDTH,
                                  constants.BUTTON_HEIGHT)
        if button_rect.collidepoint(event.pos) and not self.shuffle_used:
            player.shuffle_items()
            self.shuffle_used = True  # Set the flag to True after shuffle
            return True
        return False