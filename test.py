import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import pygame

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
        self.board = [''] * 9
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
            values=['Human', 'Novice', 'Intermediate', 'Experienced', 'Expert'], 
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
            self.reset_board()
            return

        if self.board[index] == '':
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player, fg='green' if self.current_player == 'X' else 'red')
            self.animate_move(self.buttons[index])
            if self.move_sound:
                self.move_sound.play()
            
            if self.check_win():
                if self.win_sound:
                    self.win_sound.play()
                self.animate_win(self.winning_combo)  # Animate win combo
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.update_stats(self.current_player)
                self.game_active = False
            elif '' not in self.board:
                if self.draw_sound:
                    self.draw_sound.play()
                messagebox.showinfo("Game Over", "It's a draw!")
                self.update_stats('cat')
                self.reset_board_color()  # Reset board color on draw
                self.game_active = False
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                print(f"Current player changed to: {self.current_player}")
                self.current_player_label.config(text=f"Current Player: {self.current_player}")
                self.update_board_color()  # Change board color based on turn
                if self.player_types['P2'].get() != 'Human' and self.current_player != self.player_types['X_O'].get():
                    self.master.after(500, self.ai_move)

    def animate_move(self, button):
        original_color = button.cget("background")
        button.config(bg='yellow')
        self.master.after(200, lambda: button.config(bg=original_color))

    def animate_win(self, winning_combo):
        for tile in winning_combo:
            self.animate_rgb(self.buttons[tile])

        for i in range(9):
            if i not in winning_combo:
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
        ai_level = self.player_types['P2'].get()
        print(f"AI level: {ai_level}")
        if ai_level == 'Novice':
            move = self.novice_ai()
        elif ai_level == 'Intermediate':
            move = self.intermediate_ai()
        elif ai_level == 'Experienced':
            move = self.experienced_ai()
        else:  # Expert
            move = self.expert_ai()

        if move is not None:
            print(f"AI chose move: {move}")
            self.make_move(move)
        else:
            print("AI could not find a valid move.")

    def novice_ai(self):
        empty_cells = [i for i, cell in enumerate(self.board) if cell == '']
        return random.choice(empty_cells) if empty_cells else None

    def intermediate_ai(self):
        # Check for winning move
        for i in range(9):
            if self.board[i] == '':
                self.board[i] = self.current_player
                if self.check_win():
                    self.board[i] = ''
                    return i
                self.board[i] = ''
        
        # Check for blocking opponent's winning move
        opponent = 'O' if self.current_player == 'X' else 'X'
        for i in range(9):
            if self.board[i] == '':
                self.board[i] = opponent
                if self.check_win():
                    self.board[i] = ''
                    return i
                self.board[i] = ''
        
        # Otherwise, make a random move
        return self.novice_ai()

    def experienced_ai(self):
        # First, try to win
        winning_move = self.find_winning_move(self.current_player)
        if winning_move is not None:
            return winning_move
        
        # If can't win, block opponent
        opponent = 'O' if self.current_player == 'X' else 'X'
        blocking_move = self.find_winning_move(opponent)
        if blocking_move is not None:
            return blocking_move
        
        # If center is empty, take it
        if self.board[4] == '':
            return 4
        
        # Try to create a fork
        fork_move = self.find_fork_move(self.current_player)
        if fork_move is not None:
            return fork_move
        
        # Block opponent's fork
        opponent_fork_move = self.find_fork_move(opponent)
        if opponent_fork_move is not None:
            return opponent_fork_move
        
        # Take corners if available
        corners = [0, 2, 6, 8]
        empty_corners = [corner for corner in corners if self.board[corner] == '']
        if empty_corners:
            return random.choice(empty_corners)
        
        # Take any edge
        edges = [1, 3, 5, 7]
        empty_edges = [edge for edge in edges if self.board[edge] == '']
        if empty_edges:
            return random.choice(empty_edges)
        
        # This should never happen in a normal game
        return self.novice_ai()

    def expert_ai(self):
        # The expert AI is unbeatable. It uses the minimax algorithm with alpha-beta pruning.
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')

        for i in range(9):
            if self.board[i] == '':
                self.board[i] = self.current_player
                score = self.minimax(0, False, alpha, beta)
                self.board[i] = ''  # Undo the move
                if score > best_score:
                    best_score = score
                    best_move = i
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break

        return best_move

    def minimax(self, depth, is_maximizing, alpha, beta):
        if self.check_win():
            return 1 if not is_maximizing else -1
        elif '' not in self.board:  # It's a draw
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(9):
                if self.board[i] == '':
                    self.board[i] = self.current_player
                    score = self.minimax(depth + 1, False, alpha, beta)
                    self.board[i] = ''  # Undo the move
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break  # Alpha-beta pruning
            return best_score
        else:
            best_score = float('inf')
            opponent = 'O' if self.current_player == 'X' else 'X'
            for i in range(9):
                if self.board[i] == '':
                    self.board[i] = opponent
                    score = self.minimax(depth + 1, True, alpha, beta)
                    self.board[i] = ''  # Undo the move
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break  # Alpha-beta pruning
            return best_score

    def find_winning_move(self, player):
        for i in range(9):
            if self.board[i] == '':
                self.board[i] = player
                if self.check_win():
                    self.board[i] = ''
                    return i
                self.board[i] = ''
        return None

    def find_fork_move(self, player):
        for i in range(9):
            if self.board[i] == '':
                self.board[i] = player
                if self.count_winning_moves(player) >= 2:
                    self.board[i] = ''
                    return i
                self.board[i] = ''
        return None

    def count_winning_moves(self, player):
        count = 0
        for i in range(9):
            if self.board[i] == '':
                self.board[i] = player
                if self.check_win():
                    count += 1
                self.board[i] = ''
        return count

    def check_win(self):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        for condition in win_conditions:
            if all(self.board[i] == self.current_player for i in condition):
                self.winning_combo = condition
                return True
        return False

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
        self.board = [''] * 9
        for button in self.buttons:
            button.config(text='', fg='black', bg='SystemButtonFace')
        self.game_active = True
        self.current_player = 'X'
        self.current_player_label.config(text="Current Player: X")
        self.update_board_color()

    def reset_game(self):
        self.reset_board()
        if self.player_types['P2'].get() != 'Human' and self.current_player != self.player_types['X_O'].get():
            self.master.after(500, self.ai_move)

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()