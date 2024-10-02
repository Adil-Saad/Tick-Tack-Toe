import tkinter as tk
from tkinter import messagebox

# Initialize the main application window
root = tk.Tk()
root.title("Tic-Tac-Toe")

# Variables to keep track of the game state
current_player = "X"
board = [["" for _ in range(3)] for _ in range(3)]

# Function to check for a win
def check_winner():
    # Check rows and columns for a win
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "":
            return board[0][i]
    
    # Check diagonals for a win
    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]
    
    # Check for a draw (no empty spaces left)
    if all(board[i][j] != "" for i in range(3) for j in range(3)):
        return "Draw"
    
    return None

# Function to handle button click
def button_click(row, col):
    global current_player
    if board[row][col] == "" and check_winner() is None:
        board[row][col] = current_player
        buttons[row][col].config(text=current_player, state=tk.DISABLED)
        
        # Check if the game has been won or drawn
        winner = check_winner()
        if winner:
            if winner == "Draw":
                messagebox.showinfo("Tic-Tac-Toe", "It's a Draw!")
            else:
                messagebox.showinfo("Tic-Tac-Toe", f"Player {winner} wins!")
            disable_buttons()
        else:
            # Switch to the other player
            current_player = "O" if current_player == "X" else "X"

# Function to disable all buttons when game ends
def disable_buttons():
    for row in buttons:
        for button in row:
            button.config(state=tk.DISABLED)

# Function to reset the game
def reset_game():
    global current_player, board
    current_player = "X"
    board = [["" for _ in range(3)] for _ in range(3)]
    
    for row in buttons:
        for button in row:
            button.config(text="", state=tk.NORMAL)

# Create the game grid using buttons
buttons = [[None for _ in range(3)] for _ in range(3)]

for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(root, text="", font=('normal', 40), width=5, height=2,
                                  command=lambda row=i, col=j: button_click(row, col))
        buttons[i][j].grid(row=i, column=j)

# Create a reset button
reset_button = tk.Button(root, text="Reset", font=('normal', 20), command=reset_game)
reset_button.grid(row=3, column=0, columnspan=3)

# Run the application
root.mainloop()
