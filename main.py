import subprocess
import sys

# Function to check and install a package if it's not installed
def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Package '{package}' not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"'{package}' has been installed.")
    finally:
        globals()[package] = __import__(package)

# List of packages required
packages = ['pygame', 'numpy', 'tkinter']

# Check and install missing packages
for package in packages:
    install_and_import(package)

import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import pygame
import numpy as np
import copy
import os

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Awesome Tic-Tac-Toe!")
        self.master.configure(bg='black')

        # Set window size
        self.window_width = 400
        self.window_height = 650

        # Center the window
        self.center_window()

        self.current_player = 'X'
        self.board = Board()
        self.game_active = True
        self.winning_combo = None
        self.animation_in_progress = False

        self.stats = {
            'X': {'wins': 0, 'losses': 0, 'draws': 0},
            'O': {'wins': 0, 'losses': 0, 'draws': 0},
            'cats': 0
        }

        # Initialize pygame for sound
        pygame.mixer.init()
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current directory of the script

            self.move_sound = pygame.mixer.Sound(os.path.join(base_dir, "move.wav"))
            self.win_sound = pygame.mixer.Sound(os.path.join(base_dir, "win.wav"))
            self.draw_sound = pygame.mixer.Sound(os.path.join(base_dir, "draw.wav"))
        except pygame.error as e:
            print(f"Error loading sound files: {e}")
            self.move_sound = None
            self.win_sound = None
            self.draw_sound = None

        self.create_widgets()
        
        # Initialize AI
        self.ai = AI()

    def center_window(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        position_x = (screen_width // 2) - (self.window_width // 2)
        position_y = (screen_height // 2) - (self.window_height // 2)
        self.master.geometry(f"{self.window_width}x{self.window_height}+{position_x}+{position_y}")

    def create_widgets(self):
        # Game board
        self.board_frame = tk.Frame(self.master, bg='gray')
        self.board_frame.pack(pady=20)

        self.buttons = []
        for i in range(9):
            button = tk.Button(self.board_frame, text='', font=('Courier', 20, 'bold'), 
                               width=5, height=2, command=lambda x=i: self.make_move(x))
            button.grid(row=i//3, column=i%3, padx=2, pady=2)
            self.buttons.append(button)

        # Opponent selection
        self.opponent_frame = tk.Frame(self.master, bg='black')
        self.opponent_frame.pack(pady=10)

        tk.Label(self.opponent_frame, text="Opponent:", 
                 font=('Courier', 12), fg='yellow', bg='black').grid(row=0, column=0, padx=5)
        self.opponent_type = ttk.Combobox(self.opponent_frame, 
            values=['Human', 'Easy AI', 'Medium AI', 'Hard AI', 'Unbeatable AI'], 
            state='readonly', width=15, font=('comic sans ms', 10))
        self.opponent_type.set('Human')
        self.opponent_type.grid(row=0, column=1, padx=5)

        # Statistics
        self.stats_frame = tk.Frame(self.master, bg='black')
        self.stats_frame.pack(pady=10)

        tk.Label(self.stats_frame, text="Game Statistics", 
                 font=('Courier', 16, 'bold'), fg='yellow', bg='black').pack(pady=5)

        self.stats_table = ttk.Treeview(self.stats_frame, columns=('Player', 'Wins', 'Losses', 'Draws'), show='headings', height=3)
        self.stats_table.pack()

        for col in self.stats_table['columns']:
            self.stats_table.heading(col, text=col)
            self.stats_table.column(col, anchor='center', width=80)

        self.stats_table.insert('', 'end', values=('X', 0, 0, 0))
        self.stats_table.insert('', 'end', values=('O', 0, 0, 0))
        self.stats_table.insert('', 'end', values=('Cats', 0, '-', '-'))

        # New Game button
        self.new_game_button = tk.Button(self.master, text="New Game", font=('Courier', 12, 'bold'),
                                         command=self.reset_game, bg='green', fg='white')
        self.new_game_button.pack(pady=10)

        # Current player display
        self.current_player_label = tk.Label(self.master, text="Current Player: X", 
                                             font=('Courier', 14, 'bold'), fg='white', bg='black')
        self.current_player_label.pack(pady=5)

        # Scoreboard
        self.scoreboard = tk.Label(self.master, text="X: 0  O: 0", 
                                   font=('Courier', 16, 'bold'), fg='yellow', bg='black')
        self.scoreboard.pack(pady=5)

    def make_move(self, index):
        if not self.game_active or self.animation_in_progress:
            return

        row, col = index // 3, index % 3
        if self.board.empty_sqr(row, col):
            player = 1 if self.current_player == 'X' else 2
            self.board.mark_sqr(row, col, player)
            self.buttons[index].config(text=self.current_player, fg='green' if self.current_player == 'X' else 'red')
            self.animate_move(self.buttons[index])
            if self.move_sound:
                self.move_sound.play()
            
            if self.check_game_over():
                return

            self.current_player = 'O' if self.current_player == 'X' else 'X'
            self.current_player_label.config(text=f"Current Player: {self.current_player}")
            self.update_board_color()
            
            if self.opponent_type.get() != 'Human' and self.current_player == 'O':
                self.master.after(500, self.ai_move)

    def check_game_over(self):
        winner = self.board.final_state()
        if winner != 0:
            self.winning_combo = self.board.get_winning_combo()
            if self.win_sound:
                self.win_sound.play()
            self.animate_win()
            winner_symbol = 'X' if winner == 1 else 'O'
            self.game_active = False
            self.master.after(1000, lambda: self.show_game_over_message(f"Player {winner_symbol} wins!"))
            return True
        elif self.board.isfull():
            if self.draw_sound:
                self.draw_sound.play()
            self.game_active = False
            self.master.after(1000, lambda: self.show_game_over_message("It's a draw!"))
            return True
        return False

    def show_game_over_message(self, message):
        messagebox.showinfo("Game Over", message)
        self.update_stats('X' if message.startswith("Player X") else 'O' if message.startswith("Player O") else 'cat')
        self.reset_board()

    def reset_board(self):
        self.board = Board()
        for button in self.buttons:
            button.config(text='', fg='black', bg='SystemButtonFace')
        self.game_active = True
        self.current_player = 'X'
        self.current_player_label.config(text="Current Player: X")
        self.update_board_color()
        self.winning_combo = None
        self.animation_in_progress = False

        # This line prevents immediate AI move after resetting
        if self.opponent_type.get() != 'Human' and self.current_player == 'O':
            self.master.after(500, self.ai_move)

    def show_game_over_message(self, message):
        messagebox.showinfo("Game Over", message)
        self.update_stats('X' if message.startswith("Player X") else 'O' if message.startswith("Player O") else 'cat')
        self.reset_board()

    def animate_move(self, button):
        original_color = button.cget("background")
        button.config(bg='yellow')
        self.master.after(200, lambda: button.config(bg=original_color))

    def animate_win(self):
        self.animation_in_progress = True
        for tile in self.winning_combo:
            self.animate_rgb(self.buttons[tile[0]*3 + tile[1]])

    def animate_rgb(self, button):
        for _ in range(5):  # Change colors 5 times
            button.config(bg=random.choice(['red', 'green', 'blue', 'yellow', 'purple', 'cyan']))
            self.master.update()
            time.sleep(0.1)
        self.animation_in_progress = False

    def update_board_color(self):
        self.board_frame.config(bg='blue' if self.current_player == 'X' else 'red')

    def reset_board_color(self):
        self.board_frame.config(bg='gray')

    def ai_move(self):
        if not self.game_active:
            return

        difficulty = self.opponent_type.get()
        ai_player = 2  # AI is always 'O'
        self.ai.player = ai_player
        
        if difficulty == 'Easy AI':
            self.ai.level = 0
        elif difficulty == 'Medium AI':
            self.ai.level = 1
        elif difficulty == 'Hard AI':
            self.ai.level = 2
        else:  # Unbeatable AI
            self.ai.level = 3
        
        row, col = self.ai.eval(self.board)
        index = row * 3 + col
        self.make_move(index)

    def update_stats(self, winner):
        if winner in ['X', 'O']:
            self.stats[winner]['wins'] += 1
            other_player = 'O' if winner == 'X' else 'X'
            self.stats[other_player]['losses'] += 1
        else:  # It's a cat's game (draw)
            self.stats['cats'] += 1
            self.stats['X']['draws'] += 1
            self.stats['O']['draws'] += 1

        self.update_stats_display()
        self.update_scoreboard()

    def update_stats_display(self):
        for player in ['X', 'O']:
            self.stats_table.item(
                self.stats_table.get_children()[['X', 'O'].index(player)], 
                values=(player, self.stats[player]['wins'], 
                        self.stats[player]['losses'], 
                        self.stats[player]['draws'])
            )
        
        self.stats_table.item(
            self.stats_table.get_children()[2], 
            values=('Cats', self.stats['cats'], '-', '-')
        )

    def update_scoreboard(self):
        self.scoreboard.config(text=f"X: {self.stats['X']['wins']}  O: {self.stats['O']['wins']}")

    def reset_board(self):
        self.board = Board()
        for button in self.buttons:
            button.config(text='', fg='black', bg='SystemButtonFace')
        self.game_active = True
        self.current_player = 'X'
        self.current_player_label.config(text="Current Player: X")
        self.update_board_color()
        self.winning_combo = None
        self.animation_in_progress = False

    def reset_game(self):
        self.reset_board()
        self.stats = {
            'X': {'wins': 0, 'losses': 0, 'draws': 0},
            'O': {'wins': 0, 'losses': 0, 'draws': 0},
            'cats': 0
        }
        self.update_stats_display()
        self.update_scoreboard()

class Board:
    def __init__(self):
        self.squares = np.zeros((3, 3))
        self.empty_sqrs = self.squares
        self.marked_sqrs = 0

    def final_state(self):
        # vertical wins
        for col in range(3):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                return self.squares[0][col]

        # horizontal wins
        for row in range(3):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                return self.squares[row][0]

        # desc diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            return self.squares[1][1]

        # asc diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            return self.squares[1][1]

        # no win yet
        return 0

    def get_winning_combo(self):
        # vertical wins
        for col in range(3):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                return [(0, col), (1, col), (2, col)]

        # horizontal wins
        for row in range(3):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                return [(row, 0), (row, 1), (row, 2)]

        # desc diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            return [(0, 0), (1, 1), (2, 2)]

        # asc diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            return [(2, 0), (1, 1), (0, 2)]

        return []

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(3):
            for col in range(3):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))
        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs == 0

class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))
        return empty_sqrs[idx]

    def minimax(self, board, maximizing, depth):
        case = board.final_state()

        # Terminal state reached: return evaluation based on winner or draw
        if case == 1:  # X wins
            return 1, None
        if case == 2:  # O wins
            return -1, None
        elif board.isfull() or depth == 0:  # Draw or depth limit reached
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)  # Player X is maximizing
                eval = self.minimax(temp_board, False, depth - 1)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        else:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)  # Player O is minimizing
                eval = self.minimax(temp_board, True, depth - 1)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    def check_for_win(self, board, ai_player):
        """
        Checks if there is an opportunity for the AI to win the game.
        """
        empty_sqrs = board.get_empty_sqrs()

        # Check all empty squares and see if AI can win if it marks that square
        for (row, col) in empty_sqrs:
            temp_board = copy.deepcopy(board)
            temp_board.mark_sqr(row, col, ai_player)
            if temp_board.final_state() == ai_player:
                return (row, col)  # Found a winning move

        return None  # No winning move found

    def check_for_block(self, board, opponent):
        """
        Checks if there is an opportunity to block the opponent's winning move.
        """
        empty_sqrs = board.get_empty_sqrs()

        # Check all empty squares and see if opponent can win if they mark that square
        for (row, col) in empty_sqrs:
            temp_board = copy.deepcopy(board)
            temp_board.mark_sqr(row, col, opponent)
            if temp_board.final_state() == opponent:
                return (row, col)  # Found a block move

        return None  # No block needed

    def eval(self, main_board):
        # Different AI behaviors based on difficulty level
        if self.level == 0:
            # Easy AI: Random move
            move = self.rnd(main_board)

        elif self.level == 1:
            # Medium AI: Play defensively (block player), aggressively (win if possible), or random move

            # Step 1: Check if AI can win
            win_move = self.check_for_win(main_board, ai_player=self.player)
            if win_move:
                move = win_move
            else:
                # Step 2: Check if AI can block the player (player is X, so opponent = 1)
                block_move = self.check_for_block(main_board, opponent=1)
                if block_move:
                    move = block_move
                else:
                    # Step 3: No immediate win or block needed, make a random move
                    move = self.rnd(main_board)

        elif self.level == 2:
            # Hard AI: Predict 6 moves ahead
            depth = 6
            eval, move = self.minimax(main_board, False, depth)

        else:
            # Unbeatable AI: Max depth, predict all possible outcomes
            depth = float('inf')  # No depth limit
            eval, move = self.minimax(main_board, False, depth)

        print(f'AI (Level {self.level}) has chosen to mark the square in pos {move}')
        return move

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
