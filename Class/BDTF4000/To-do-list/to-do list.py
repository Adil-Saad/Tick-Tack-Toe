import tkinter as tk
from tkinter import messagebox
import os

# Define the file where tasks will be stored
TASKS_FILE = "tasks.txt"

# Function to load tasks from the file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            tasks = [line.strip() for line in file.readlines()]
    else:
        tasks = []
    return tasks

# Function to save tasks to the file
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        for task in tasks:
            file.write(task + "\n")

# Function to add a task
def add_task():
    task = entry_task.get().strip()
    if task:
        listbox_tasks.insert(tk.END, task)
        tasks.append(task)
        save_tasks(tasks)
        entry_task.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Task cannot be empty")

# Function to remove a task
def remove_task():
    try:
        task_index = listbox_tasks.curselection()[0]
        task_to_remove = listbox_tasks.get(task_index)
        listbox_tasks.delete(task_index)
        tasks.remove(task_to_remove)
        save_tasks(tasks)
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to remove")

# Initialize tasks from the file
tasks = load_tasks()

# Create the main window
root = tk.Tk()
root.title("To-Do List")
root.geometry("450x450")
root.configure(bg="#ffffff")
window_width = 500
window_height = 450

# Get the screen's width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the position to center the window
position_x = (screen_width // 2) - (window_width // 2)
position_y = (screen_height // 2) - (window_height // 2)

# Set the geometry of the window
root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

# Create and place the title label
label_title = tk.Label(root, text="My To-Do List", font=("comic sans ms", 18, "bold"), bg="#f0f8ff", fg="#b00b69")
label_title.pack(pady=10)

# Create and place the task entry field and add button
frame_input = tk.Frame(root, bg="#00e2fc")
frame_input.pack(pady=10)

entry_task = tk.Entry(frame_input, width=30, font=("comic sans ms", 12))
entry_task.pack(side=tk.LEFT, padx=10)

button_add_task = tk.Button(frame_input, text="Add Task", width=10, bg="#34c759", fg="white", font=("comic sans ms", 10, "bold"), command=add_task)
button_add_task.pack(side=tk.LEFT)

# Create and place the task list box
listbox_tasks = tk.Listbox(root, height=10, width=50, bg="#000000", fg="#58fc00",font=("comic sans ms", 12), selectbackground="#ffcccb")
listbox_tasks.pack(pady=10)

# Populate the listbox with the loaded tasks
for task in tasks:
    listbox_tasks.insert(tk.END, task)

# Create and place the remove task button
button_remove_task = tk.Button(root, text="Mark as Completed", width=15, bg="#ff3b30", fg="white", font=("comic sans ms", 10, "bold"), command=remove_task)
button_remove_task.pack(pady=10)

# Run the main loop
root.mainloop()
