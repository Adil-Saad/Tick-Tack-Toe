import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import pygame
import numpy as np
import copy

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

        self.stats = {
            'X': {'wins': 0, 'losses': 0, 'draws': 0},
            'O': {'wins': 0, 'losses': 0, 'draws': 0},
            'cats': 0
        }

        # Initialize pygame for sound
        pygame.mixer.init()
        try:
            self.move_sound = pygame.mixer.Sound("move.wav")
            self.win_sound = pygame.mixer.Sound("win.wav")
            self.draw_sound = pygame.mixer.Sound("draw.wav")
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

        # Player type selection
        self.player_frame = tk.Frame(self.master, bg='black')
        self.player_frame.pack(pady=10)

        # Player 1 selects X or O
        tk.Label(self.player_frame, text="Player 1 (Choose X or O):", 
                 font=('Courier', 12), fg='yellow', bg='black').grid(row=0, column=0, padx=5)

        self.player_types = {}
        self.player_types['X_O'] = ttk.Combobox(self.player_frame, 
            values=['X', 'O'], state='readonly', width=5, font=('comic sans ms', 10))
        self.player_types['X_O'].set('X')
        self.player_types['X_O'].grid(row=0, column=1, padx=5)

        # Player 2 (AI or Human)
        tk.Label(self.player_frame, text="Player 2:", 
                 font=('Courier', 12), fg='yellow', bg='black').grid(row=1, column=0, padx=5)
        self.player_types['P2'] = ttk.Combobox(self.player_frame, 
            values=['Human', 'Easy', 'Medium', 'Hard', 'Unbeatable'], 
            state='readonly', width=15, font=('comic sans ms', 10))
        self.player_types['P2'].set('Human')
        self.player_types['P2'].grid(row=1, column=1, padx=5)

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
        if not self.game_active:
            print("Game is not active")
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
            
            if self.player_types['P2'].get() != 'Human' and self.current_player != self.player_types['X_O'].get():
                self.master.after(500, self.ai_move)

    def check_game_over(self):
        winner = self.board.final_state()
        if winner != 0:
            self.winning_combo = self.board.get_winning_combo()
            if self.win_sound:
                self.win_sound.play()
            self.animate_win()
            winner_symbol = 'X' if winner == 1 else 'O'
            messagebox.showinfo("Game Over", f"Player {winner_symbol} wins!")
            self.update_stats(winner_symbol)
            self.game_active = False
            return True
        elif self.board.isfull():
            if self.draw_sound:
                self.draw_sound.play()
            messagebox.showinfo("Game Over", "It's a draw!")
            self.update_stats('cat')
            self.reset_board_color()
            self.game_active = False
            return True
        return False

    def animate_move(self, button):
        original_color = button.cget("background")
        button.config(bg='yellow')
        self.master.after(200, lambda: button.config(bg=original_color))

    def animate_win(self):
        for tile in self.winning_combo:
            self.animate_rgb(self.buttons[tile[0]*3 + tile[1]])

        for i in range(9):
            if (i//3, i%3) not in self.winning_combo:
                self.animate_tile_break(self.buttons[i])

    def animate_rgb(self, button):
        for _ in range(10):  # Change colors 10 times
            button.config(bg=random.choice(['red', 'green', 'blue', 'yellow', 'purple', 'cyan']))
            self.master.update()
            time.sleep(0.1)

    def animate_tile_break(self, button):
        for _ in range(3):
            button.config(bg='white')
            self.master.update()
            time.sleep(0.1)
        button.config(text='', bg='white')

    def update_board_color(self):
        if self.current_player == self.player_types['X_O'].get():  # Player 1
            self.board_frame.config(bg='blue')
        else:  # Player 2
            self.board_frame.config(bg='red')

    def reset_board_color(self):
        self.board_frame.config(bg='gray')

    def ai_move(self):
        difficulty = self.player_types['P2'].get()
        ai_player = 2 if self.current_player == 'O' else 1
        self.ai.player = ai_player
        
        if difficulty == 'Easy':
            self.ai.level = 0
        elif difficulty == 'Medium':
            self.ai.level = 1
        elif difficulty == 'Hard':
            self.ai.level = 2
        else:  # Unbeatable
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

    def reset_game(self):
        self.board = Board()
        for button in self.buttons:
            button.config(text='', fg='black', bg='SystemButtonFace')
        self.game_active = True
        self.current_player = 'X'
        self.current_player_label.config(text="Current Player: X")
        self.update_board_color()
        if self.player_types['P2'].get() != 'Human' and self.current_player != self.player_types['X_O'].get():
            self.master.after(500, self.ai_move)

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

    def minimax(self, board, maximizing):
        case = board.final_state()

        if case == 1:
            return 1, None
        if case == 2:
            return -1, None
        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    def eval(self, main_board):
        if self.level == 0:
            # random choice
            eval = 'random'
            move = self.rnd(main_board)
        else:
            # minimax algo choice
            eval, move = self.minimax(main_board, False)

        print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')

        return move

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()