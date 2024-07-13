# game.py
import pygame
import constants

pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT
CELL_SIZE = constants.CELL_SIZE

# Load images
rock_img = pygame.image.load(constants.rock_png)
paper_img = pygame.image.load(constants.paper_png)
scissors_img = pygame.image.load(constants.scissors_png)
flag_img = pygame.image.load(constants.flag_png)
images = {'Rock': rock_img, 'Paper': paper_img, 'Scissors': scissors_img, 'Flag': flag_img}

# Scale images to fit the cell size
rock_img = pygame.transform.scale(rock_img, (CELL_SIZE, CELL_SIZE))
paper_img = pygame.transform.scale(paper_img, (CELL_SIZE, CELL_SIZE))
scissors_img = pygame.transform.scale(scissors_img, (CELL_SIZE, CELL_SIZE))
flag_img = pygame.transform.scale(flag_img, (CELL_SIZE, CELL_SIZE))

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('K.L.Y.R')
FONT = pygame.font.Font(None, 24)

class Game:
    def __init__(self, logic):
        self.logic = logic
        self.COLORS = constants.COLORS
        self.shuffle_used = False
        self.player_turn = True

    def draw_board(self):
        screen.fill((255,255,255))
        for row in range(6):
            for col in range(7):
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, self.COLORS['Empty'], rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)
        self.draw_pieces()
        self.draw_side_column()

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

    def draw_side_column(self):
        # Draw the background for the side column
        side_column_rect = pygame.Rect(7 * CELL_SIZE, 0, constants.SIDE_COLUMN_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(screen, (255, 255, 255), side_column_rect)

        # Display whose turn it is
        turn_text = FONT.render("Player's Turn" if self.player_turn else "Computer's Turn", True, (0, 0, 0))
        screen.blit(turn_text, (7 * CELL_SIZE + 10, 10))

        # Display the number of soldiers
        player_soldiers_text = FONT.render(f"Player Soldiers: {len(self.logic.player.positions)}", True, (0, 0, 0))
        screen.blit(player_soldiers_text, (7 * CELL_SIZE + 10, 50))

        computer_soldiers_text = FONT.render(f"Computer Soldiers: {len(self.logic.computer.positions)}", True, (0, 0, 0))
        screen.blit(computer_soldiers_text, (7 * CELL_SIZE + 10, 90))

        # Draw the shuffle button
        button_rect = pygame.Rect(7 * CELL_SIZE + 10, 150, constants.BUTTON_WIDTH, constants.BUTTON_HEIGHT)
        self.draw_button(button_rect)

    def draw_button(self, button_rect):
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos) and not self.shuffle_used:
            pygame.draw.rect(screen, constants.BUTTON_HOVER_COLOR, button_rect)
        elif button_rect.collidepoint(mouse_pos) and not self.shuffle_used:
            pygame.draw.rect(screen, constants.BUTTON_COLOR, button_rect)
        elif self.shuffle_used:
            pygame.draw.rect(screen, constants.BUTTON_COLOR_AFTER_CLICK, button_rect)
        else:
            pygame.draw.rect(screen, constants.BUTTON_COLOR, button_rect)

        text = FONT.render('Shuffle', True, constants.BUTTON_TEXT_COLOR)
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)

    def handle_button_click(self, event, player):
        button_rect = pygame.Rect(7 * CELL_SIZE + 10, 150, constants.BUTTON_WIDTH, constants.BUTTON_HEIGHT)
        if button_rect.collidepoint(event.pos) and not self.shuffle_used:
            player.shuffle_items()
            self.shuffle_used = True  # Set the flag to True after shuffle
            return True
        return False
