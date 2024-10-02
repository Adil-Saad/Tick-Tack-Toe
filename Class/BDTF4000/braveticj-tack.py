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

        self.stats = {
            'X': {'wins': 0, 'losses': 0, 'draws': 0},
            'O': {'wins': 0, 'losses': 0, 'draws': 0},
            'cats': 0
        }

        # Initialize pygame for sound
        pygame.mixer.init()
        self.move_sound = pygame.mixer.Sound("move.wav")
        self.win_sound = pygame.mixer.Sound("win.wav")
        self.draw_sound = pygame.mixer.Sound("draw.wav")

        self.create_widgets()

    def center_window(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        position_x = (screen_width // 2) - (self.window_width // 2)
        position_y = (screen_height // 2) - (self.window_height // 2)
        self.master.geometry(f"{self.window_width}x{self.window_height}+{position_x}+{position_y}")

    def create_widgets(self):
        # Game board
        self.board_frame = tk.Frame(self.master, bg='cyan')
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

        players = ['X', 'O']
        self.player_types = {}
        for player in players:
            tk.Label(self.player_frame, text=f"Player {player}:", 
                     font=('Courier', 12), fg='yellow', bg='black').grid(row=players.index(player), column=0, padx=5)
            self.player_types[player] = ttk.Combobox(self.player_frame, 
                values=['Human', 'Novice', 'Intermediate', 'Experienced', 'Expert'], 
                state='readonly', width=15, font=('comic sans ms', 10))
            self.player_types[player].set('Human')
            self.player_types[player].grid(row=players.index(player), column=1, padx=5)

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
            self.reset_board()
            return

        if self.board[index] == '':
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player, fg='green' if self.current_player == 'X' else 'red')
            self.animate_move(self.buttons[index])
            self.move_sound.play()
            
            if self.check_win():
                self.win_sound.play()
                self.animate_win()
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.update_stats(self.current_player)
                self.game_active = False
            elif '' not in self.board:
                self.draw_sound.play()
                messagebox.showinfo("Game Over", "It's a draw!")
                self.update_stats('cat')
                self.game_active = False
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.current_player_label.config(text=f"Current Player: {self.current_player}")
                if self.player_types[self.current_player].get() != 'Human':
                    self.master.after(500, self.ai_move)

    def animate_move(self, button):
        original_color = button.cget("background")
        button.config(bg='yellow')
        self.master.after(200, lambda: button.config(bg=original_color))

    def animate_win(self):
        for i in range(5):  # Flash 5 times
            for button in self.buttons:
                button.config(bg='gold')
            self.master.update()
            time.sleep(0.1)
            for button in self.buttons:
                button.config(bg='SystemButtonFace')
            self.master.update()
            time.sleep(0.1)

    def ai_move(self):
        empty_cells = [i for i, cell in enumerate(self.board) if cell == '']
        if empty_cells:
            self.make_move(random.choice(empty_cells))

    def check_win(self):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        return any(all(self.board[i] == self.current_player for i in condition) for condition in win_conditions)

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
            self.stats_table.item(self.stats_table.get_children()[['X', 'O'].index(player)], 
                                  values=(player, self.stats[player]['wins'], 
                                          self.stats[player]['losses'], 
                                          self.stats[player]['draws']))
        
        self.stats_table.item(self.stats_table.get_children()[2], 
                              values=('Cats', self.stats['cats'], '-', '-'))

    def update_scoreboard(self):
        self.scoreboard.config(text=f"X: {self.stats['X']['wins']}  O: {self.stats['O']['wins']}")

    def reset_board(self):
        self.board = [''] * 9
        for button in self.buttons:
            button.config(text='')
        self.game_active = True
        self.current_player = 'X'
        self.current_player_label.config(text="Current Player: X")

    def reset_game(self):
        self.reset_board()
        self.stats = {
            'X': {'wins': 0, 'losses': 0, 'draws': 0},
            'O': {'wins': 0, 'losses': 0, 'draws': 0},
            'cats': 0
        }
        self.update_stats_display()
        self.update_scoreboard()
        messagebox.showinfo("New Game", "The game has been reset. All scores are back to zero.")

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()