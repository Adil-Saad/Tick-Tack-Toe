import tkinter as tk
from tkinter import *
from functools import partial
from tkinter import messagebox

# Global sign variable to switch turns
sign = 0

# Create an empty 3x3 board
global board
board = [[" " for x in range(3)] for y in range(3)]

# Function to check if there's a winner
def winner(b, l):
    return ((b[0][0] == l and b[0][1] == l and b[0][2] == l) or
            (b[1][0] == l and b[1][1] == l and b[1][2] == l) or
            (b[2][0] == l and b[2][1] == l and b[2][2] == l) or
            (b[0][0] == l and b[1][0] == l and b[2][0] == l) or
            (b[0][1] == l and b[1][1] == l and b[2][1] == l) or
            (b[0][2] == l and b[1][2] == l and b[2][2] == l) or
            (b[0][0] == l and b[1][1] == l and b[2][2] == l) or
            (b[0][2] == l and b[1][1] == l and b[2][0] == l))

# Check if the board is full (i.e., draw)
def isfull():
    return all([all(row != ' ' for row in i) for i in board])

# Function to reset the board for a new game
def reset_board():
    global board, sign
    sign = 0
    board = [[" " for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            button[i][j].config(text=" ", state=NORMAL)

# Handle the event of a button being clicked (for 2 players)
def get_text(i, j, gb, l1, l2):
    global sign
    if board[i][j] == ' ':
        board[i][j] = "X" if sign % 2 == 0 else "O"
        button[i][j].config(text=board[i][j], state=DISABLED)
        sign += 1
        # Switch player turn indicators
        l1.config(state=DISABLED if sign % 2 != 0 else ACTIVE)
        l2.config(state=DISABLED if sign % 2 == 0 else ACTIVE)

    # Check for a winner or draw
    if winner(board, "X"):
        messagebox.showinfo("Winner", "Player 1 (X) won!")
        reset_board()
    elif winner(board, "O"):
        messagebox.showinfo("Winner", "Player 2 (O) won!")
        reset_board()
    elif isfull():
        messagebox.showinfo("Tie Game", "It's a tie!")
        reset_board()

# Function to create the game board for two players
def gameboard_pl(game_board, l1, l2):
    global button
    button = []
    for i in range(3):
        row = []
        for j in range(3):
            get_t = partial(get_text, i, j, game_board, l1, l2)
            btn = Button(game_board, bd=5, command=get_t, height=4, width=8)
            btn.grid(row=i+3, column=j)
            row.append(btn)
        button.append(row)

# Function to reset the game board and states
def reset_game(game_board):
    game_board.destroy()
    play()

# Function to handle the menu for playing against another player
def withplayer(game_board):
    game_board.destroy()
    game_board = Tk()
    game_board.title("Tic Tac Toe - 2 Players")

    l1 = Button(game_board, text="Player 1: X", width=10, state=ACTIVE)
    l1.grid(row=1, column=1)
    l2 = Button(game_board, text="Player 2: O", width=10, state=DISABLED)
    l2.grid(row=2, column=1)
    
    gameboard_pl(game_board, l1, l2)
    
    # Add reset button to reset the game
    reset_btn = Button(game_board, text="Reset Game", command=lambda: reset_board(), height=2, width=15)
    reset_btn.grid(row=6, column=1)

    # Make window appear at the center of the screen
    game_board.update_idletasks()
    width = game_board.winfo_width()
    height = game_board.winfo_height()
    x = (game_board.winfo_screenwidth() // 2) - (width // 2)
    y = (game_board.winfo_screenheight() // 2) - (height // 2)
    game_board.geometry(f'{width}x{height}+{x}+{y}')

    game_board.mainloop()

# Main menu function
def play():
    menu = Tk()
    menu.geometry("300x300")  # Slightly bigger window
    menu.title("Tic Tac Toe")

    # Button to play with another player
    wpl = partial(withplayer, menu)

    head = Button(menu, text="---Tic-Tac-Toe---",
                  activeforeground='red', activebackground="yellow", bg="red", fg="yellow", width=500, font='summer', bd=5)

    B2 = Button(menu, text="Multi Player", command=wpl,
                activeforeground='red', activebackground="yellow", bg="red", fg="yellow", width=500, font='summer', bd=5)

    B3 = Button(menu, text="Exit", command=menu.quit,
                activeforeground='red', activebackground="yellow", bg="red", fg="yellow", width=500, font='summer', bd=5)
    
    head.pack(side='top')
    B2.pack(side='top')
    B3.pack(side='top')

    # Make window appear at the center of the screen
    menu.update_idletasks()
    width = menu.winfo_width()
    height = menu.winfo_height()
    x = (menu.winfo_screenwidth() // 2) - (width // 2)
    y = (menu.winfo_screenheight() // 2) - (height // 2)
    menu.geometry(f'{width}x{height}+{x}+{y}')

    menu.mainloop()

# Run the game
if __name__ == '__main__':
    play()
