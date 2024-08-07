# K.L.Y.R. Game

K.L.Y.R. is a strategic game based on the classic Rock-Paper-Scissors rules with some additional features and adjustments. This game is implemented using Python and Pygame.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Game Rules](#game-rules)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/klyr-game.git
2. Navigate to the project directory:
   ```bash
   cd klyr-game
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt

## Usage
To start the game, run the "main.py" file:
   ```bash
   python main.py
   ```

## Game Rules

- The game is played on a grid where each player (human and computer) has pieces representing Rock, Paper, Scissors, and a Flag.
- Players take turns moving their pieces on the board.
- When two pieces meet, they battle according to the classic Rock-Paper-Scissors rules:
  - Rock beats Scissors
  - Scissors beats Paper
  - Paper beats Rock
- The goal is to capture the opponent's Flag.

## Project Structure

```klyr-game/
├── main.py           # Entry point of the game
├── player.py         # Player class implementation
├── computer.py       # Computer (AI) player class implementation
├── game.py           # Game class implementation
├── game_logic.py     # Game logic and rules implementation
├── constants.py      # Game constants and configuration
├── requirements.txt  # Project dependencies
├── README.md         # Project README file
└── assets/           # Directory for game assets (images, etc.)
```
## File Descriptions
- main.py: Contains the main game loop and initializes game components.
- player.py: Defines the Player class with methods for movement and shuffling items.
- computer.py: Defines the Computer class, inheriting from Player, with additional AI logic for making the best moves.
- game.py: Contains the Game class responsible for rendering the game board, handling user inputs, and updating the game state.
- game_logic.py: Implements the game logic, including movement, battles, and victory conditions.
- constants.py: Holds constant values and configuration settings used throughout the game.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request !