# constants.py

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600  # Increased width for the side column
CELL_SIZE = SCREEN_WIDTH // 10  # Adjust cell size if needed
RADIUS = CELL_SIZE // 3

# Image file paths
ROCK_PNG = 'rock.png'
FLAG_PNG = 'red-flag.png'
SCISSORS_PNG = 'scissors.png'
PAPER_PNG = 'paper.png'

# Colors
COLORS = {
    'Player': (0, 0, 255),
    'Computer': (186, 0, 0),
    'Empty': (255, 255, 255),
    'Wall': (128, 128, 128),
    'Aura': (255, 255, 255)
}

# Button properties
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
BUTTON_COLOR = (255, 222, 173)
BUTTON_HOVER_COLOR = (235, 202, 153)
BUTTON_TEXT_COLOR = (0, 0, 0)
BUTTON_COLOR_AFTER_CLICK = (128, 128, 128)

# Side column properties
SIDE_COLUMN_WIDTH = 300
SIDE_COLUMN_COLOR = (255, 255, 240)

# Cell colors
CELL_EVEN_COLOR = (179, 225, 172)
CELL_ODD_COLOR = (115, 195, 108)
