import random

# Size of the grid
N = 9

# Function to print the board
def print_board(board):
    for row in board:
        print(" ".join(str(num) if num != 0 else "." for num in row))

# Function to check if a number can be placed in a given position
def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

# Backtracking Sudoku Solver
def solve(board):
    for row in range(N):
        for col in range(N):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve(board):
                            return True
                        board[row][col] = 0
                return False
    return True

# Fill diagonal 3x3 boxes to help generate a full valid board
def fill_diagonal_boxes(board):
    for i in range(0, N, 3):
        fill_box(board, i, i)

def fill_box(board, row, col):
    nums = list(range(1, 10))
    random.shuffle(nums)
    for i in range(3):
        for j in range(3):
            board[row + i][col + j] = nums.pop()

# Generate a complete solved Sudoku board
def generate_full_board():
    board = [[0 for _ in range(N)] for _ in range(N)]
    fill_diagonal_boxes(board)
    solve(board)
    return board

# Remove numbers from the full board to create a puzzle
def remove_numbers(board, num_holes=40):
    attempts = num_holes
    while attempts > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if board[row][col] != 0:
            board[row][col] = 0
            attempts -= 1

# Main logic
if __name__ == "__main__":
    print("Generating Sudoku puzzle...\n")
    full_board = generate_full_board()
    puzzle = [row[:] for row in full_board]
    remove_numbers(puzzle, num_holes=40)

    print("Sudoku Puzzle:")
    print_board(puzzle)

    print("\nSolving...\n")
    solve(puzzle)

    print("Solved Sudoku:")
    print_board(puzzle)

