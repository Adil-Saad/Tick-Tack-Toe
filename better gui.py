import tkinter as tk
from tkinter import ttk
import random
import math

class SpaceRetroTicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Space Retro Tic-Tac-Toe")
        self.master.geometry("600x700")
        self.master.configure(bg="black")

        self.canvas = tk.Canvas(self.master, width=600, height=700, bg="black", highlightthickness=0)
        self.canvas.pack()

        self.create_space_background()
        self.create_start_screen()

    def create_space_background(self):
        for _ in range(100):
            x = random.randint(0, 600)
            y = random.randint(0, 700)
            size = random.randint(1, 3)
            color = random.choice(["white", "#ADD8E6", "#FFB6C1"])
            self.canvas.create_oval(x, y, x + size, y + size, fill=color, outline="")

    def create_start_screen(self):
        self.title = self.canvas.create_text(300, 200, text="Space Retro\nTic-Tac-Toe", font=("Courier", 36, "bold"), fill="#00FFFF", justify="center")
        self.start_button = self.canvas.create_rectangle(200, 400, 400, 460, fill="#1E90FF", outline="#00FFFF")
        self.start_text = self.canvas.create_text(300, 430, text="START", font=("Courier", 24, "bold"), fill="white")

        # Bind both text and rectangle to one function
        self.canvas.tag_bind(self.start_button, "<Button-1>", self.start_game)
        self.canvas.tag_bind(self.start_text, "<Button-1>", self.start_game)

        self.animate_title()

    def animate_title(self):
        def oscillate(t):
            return math.sin(t * 0.1) * 10

        t = 0
        def animate():
            nonlocal t
            t += 1
            y_offset = oscillate(t)
            self.canvas.move(self.title, 0, y_offset - self.last_offset)
            self.last_offset = y_offset
            self.master.after(50, animate)

        self.last_offset = 0
        animate()

    def start_game(self, event):
        self.canvas.delete("all")
        self.create_space_background()
        self.create_mode_selection()

    def create_mode_selection(self):
        self.canvas.create_text(300, 200, text="Select Game Mode", font=("Courier", 30, "bold"), fill="#00FFFF")
        
        # Single player option
        single_player = self.canvas.create_rectangle(100, 300, 300, 360, fill="#1E90FF", outline="#00FFFF")
        self.canvas.create_text(200, 330, text="Single Player", font=("Courier", 20), fill="white")
        
        # Multiplayer option
        multiplayer = self.canvas.create_rectangle(300, 300, 500, 360, fill="#1E90FF", outline="#00FFFF")
        self.canvas.create_text(400, 330, text="Multiplayer", font=("Courier", 20), fill="white")

        # Bind mode selection to the game board start
        self.canvas.tag_bind(single_player, "<Button-1>", lambda e: self.start_game_board("single"))
        self.canvas.tag_bind(multiplayer, "<Button-1>", lambda e: self.start_game_board("multi"))

    def start_game_board(self, mode):
        self.mode = mode
        self.canvas.delete("all")
        self.create_space_background()
        self.create_game_board()

    def create_game_board(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"

        # Create game board
        for i in range(4):
            self.canvas.create_line(150 + i*100, 100, 150 + i*100, 400, fill="#00FFFF", width=2)
            self.canvas.create_line(150, 100 + i*100, 450, 100 + i*100, fill="#00FFFF", width=2)

        # Create clickable areas
        for i in range(3):
            for j in range(3):
                x1, y1 = 150 + j*100, 100 + i*100
                x2, y2 = x1 + 100, y1 + 100
                area = self.canvas.create_rectangle(x1, y1, x2, y2, fill="", outline="")
                # Correct the row and column capturing in the lambda
                self.canvas.tag_bind(area, "<Button-1>", lambda e, row=i, col=j: self.make_move(row, col))

        # Create turn indicator and reset button
        self.turn_indicator = self.canvas.create_text(300, 50, text="X's Turn", font=("Courier", 24), fill="#00FFFF")
        reset_button = self.canvas.create_rectangle(250, 450, 350, 500, fill="#1E90FF", outline="#00FFFF")
        self.canvas.create_text(300, 475, text="Reset", font=("Courier", 20), fill="white")
        self.canvas.tag_bind(reset_button, "<Button-1>", self.reset_game)

    def make_move(self, row, col):
        if self.board[row][col] == " ":
            self.board[row][col] = self.current_player
            self.animate_move(row, col)
            if self.check_winner():
                self.end_game(f"{self.current_player} wins!")
            elif self.is_board_full():
                self.end_game("It's a draw!")
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.canvas.itemconfig(self.turn_indicator, text=f"{self.current_player}'s Turn")
                
                # If in single player mode and it's AI's turn, trigger AI move
                if self.mode == "single" and self.current_player == "O":
                    self.master.after(1000, self.make_ai_move)

    def animate_move(self, row, col):
        x, y = 200 + col*100, 150 + row*100
        if self.current_player == "X":
            self.animate_x(x, y)
        else:
            self.animate_o(x, y)

    def animate_x(self, x, y):
        line1 = self.canvas.create_line(x-30, y-30, x-30, y-30, fill="#FF6347", width=3)
        line2 = self.canvas.create_line(x+30, y-30, x+30, y-30, fill="#FF6347", width=3)

        def animate(t):
            if t < 30:
                self.canvas.coords(line1, x-30, y-30, x-30+t*2, y-30+t*2)
                self.canvas.coords(line2, x+30, y-30, x+30-t*2, y-30+t*2)
                self.master.after(10, lambda: animate(t+1))

        animate(0)

    def animate_o(self, x, y):
        oval = self.canvas.create_arc(x-30, y-30, x+30, y+30, start=0, extent=0, outline="#4169E1", width=3, style="arc")

        def animate(t):
            if t <= 360:
                self.canvas.itemconfig(oval, extent=t)
                self.master.after(5, lambda: animate(t+10))

        animate(0)

    def make_ai_move(self):
        # AI randomly selects an empty cell
        empty_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == " "]
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.make_move(row, col)

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != " " or \
               self.board[0][i] == self.board[1][i] == self.board[2][i] != " ":
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " " or \
           self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            return True
        return False

    def is_board_full(self):
        return all(self.board[i][j] != " " for i in range(3) for j in range(3))

    def end_game(self, message):
        self.canvas.create_rectangle(100, 200, 500, 300, fill="black", outline="#00FFFF")
        self.canvas.create_text(300, 250, text=message, font=("Courier", 30, "bold"), fill="#00FFFF")

    def reset_game(self, event):
        self.canvas.delete("all")
        self.create_space_background()
        self.create_game_board()

if __name__ == "__main__":
    root = tk.Tk()
    game = SpaceRetroTicTacToe(root)
    root.mainloop()
