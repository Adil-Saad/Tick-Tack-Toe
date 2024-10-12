# Awesome Tic-Tac-Toe Game

This is a fun and feature-rich Tic-Tac-Toe game with multiple AI difficulty levels and a sleek GUI built using Python's Tkinter. The game also features sounds, animations, and keeps track of game statistics.

## Features

- Play against Human or AI (Easy, Medium, Hard, and Unbeatable modes)
- Defensive AI that blocks your moves and aims to win when possible
- Animated moves and win celebrations
- Sound effects for moves, wins, and draws
- Game statistics tracking: wins, losses, and draws for both players
- Beautiful GUI with color-coded players and animations
- AI logic using Minimax algorithm for unbeatable difficulty

## Prerequisites

To run this project, you need to have **Python 3.x** installed on your system.

If you do not have Python installed, download it from [python.org](https://www.python.org/downloads/). During installation, make sure to select the option to **Add Python to PATH**.

## Installation

### Method 1: Manual Setup

1. Clone this repository to your local machine:
    ```bash
    git clone https://github.com/Adil-Saad/Tick-Tack-Toe.git
    ```

2. Navigate to the project folder:
    ```bash
    cd Tick-Tack-Toe
    ```

3. Install the required dependencies. If `pip` is not recognized, use `python -m pip` instead of `pip`:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the game:
    ```bash
    python best.py
    ```

### Method 2: Automatically Install Missing Libraries (for Windows)

If the required libraries are not installed on your system, the game will try to install them automatically using the following steps:

1. Clone this repository to your local machine:
    ```bash
    git clone https://github.com/Adil-Saad/Tic-Tac-Toe.git
    ```

2. Navigate to the project folder:
    ```bash
    cd Tick-Tack-Toe
    ```

3. Run the game directly using the following command. The code will check for missing libraries and install them:
    ```bash
    python best.py
    ```

### Method 3: Use `requirements.txt`

1. Clone the repository:
    ```bash
    git clone https://github.com/Adil-Saad/Tick-Tack-Toe.git
    ```

2. Navigate to the project directory:
    ```bash
    cd Tick-Tack-Toe
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the game:
    ```bash
    python best.py
    ```

## How to Play

1. Run the game, and the GUI window will pop up.
2. Select your opponent: Human or one of the AI difficulty levels (Easy, Medium, Hard, Unbeatable).
3. Player X goes first.
4. Click on any empty square to make your move.
5. The game will automatically switch to the next player, either Human or AI.
6. After each game, a "Game Over" message will show who won or if the game was a draw.
7. The game statistics (Wins, Losses, Draws) will be updated after each game.
8. Click **New Game** to reset the board and start again.

## AI Difficulty Levels

- **Easy AI**: Makes random moves with no strategy.
- **Medium AI**: Plays strategically but prioritizes blocking player wins.
- **Hard AI**: Plays more defensively and offensively, using Minimax to a certain depth.
- **Unbeatable AI**: Uses the full Minimax algorithm to never lose.

## Sound Effects

- Move Sound: Plays when a player makes a move.
- Win Sound: Plays when a player wins.
- Draw Sound: Plays when the game results in a draw.

### Note:
Make sure to have the sound files (`move.wav`, `win.wav`, `draw.wav`) in the same directory as the `best.py` file.

## Technologies Used

- Python 3.x
- Tkinter (for the GUI)
- Pygame (for sound effects)
- Numpy (for board representation and AI)
- Minimax Algorithm (for unbeatable AI)

## Future Enhancements

- Online multiplayer mode
- Customizable themes and sounds
- Timed moves for added challenge

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Adil Mahmud Saad**  
GitHub:(https://github.com/Adil-Saad)

