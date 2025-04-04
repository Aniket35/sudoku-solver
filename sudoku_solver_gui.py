import tkinter as tk
from tkinter import messagebox
import random

N = 9

# ========== Solver Logic (Backtracking) ==========
def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[box_row + i][box_col + j] == num:
                return False
    return True

def solve_board(board):
    for row in range(N):
        for col in range(N):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_board(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def fill_diagonal_boxes(board):
    for i in range(0, N, 3):
        fill_box(board, i, i)

def fill_box(board, row, col):
    nums = list(range(1, 10))
    random.shuffle(nums)
    for i in range(3):
        for j in range(3):
            board[row + i][col + j] = nums.pop()

def generate_full_board():
    board = [[0] * N for _ in range(N)]
    fill_diagonal_boxes(board)
    solve_board(board)
    return board

def remove_numbers(board, holes=40):
    removed = 0
    while removed < holes:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if board[row][col] != 0:
            board[row][col] = 0
            removed += 1

# ========== GUI Logic ==========
class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.entries = [[None for _ in range(N)] for _ in range(N)]
        self.board = [[0 for _ in range(N)] for _ in range(N)]
        self.create_grid()
        self.generate_puzzle()

        solve_btn = tk.Button(root, text="Solve", command=self.solve)
        solve_btn.grid(row=10, column=0, columnspan=9, pady=10)

    def create_grid(self):
        for row in range(N):
            for col in range(N):
                entry = tk.Entry(self.root, width=2, font=('Arial', 18), justify='center')
                entry.grid(row=row, column=col, padx=2, pady=2)
                self.entries[row][col] = entry

    def generate_puzzle(self):
        self.board = generate_full_board()
        puzzle = [row[:] for row in self.board]
        remove_numbers(puzzle, holes=40)

        for row in range(N):
            for col in range(N):
                val = puzzle[row][col]
                entry = self.entries[row][col]
                if val != 0:
                    entry.insert(0, str(val))
                    entry.config(state='disabled', disabledforeground='black')
                else:
                    entry.delete(0, tk.END)
                    entry.config(state='normal')

    def read_board(self):
        for row in range(N):
            for col in range(N):
                val = self.entries[row][col].get()
                self.board[row][col] = int(val) if val.isdigit() else 0

    def solve(self):
        self.read_board()
        if solve_board(self.board):
            for row in range(N):
                for col in range(N):
                    self.entries[row][col].delete(0, tk.END)
                    self.entries[row][col].insert(0, str(self.board[row][col]))
                    self.entries[row][col].config(disabledforeground='blue')
        else:
            messagebox.showerror("Error", "No solution found.")

# ========== Launch App ==========
if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()

