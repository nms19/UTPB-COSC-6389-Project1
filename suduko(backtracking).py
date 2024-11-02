import random
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import time


class Sudoku:
    def __init__(self):
        self.puzzle = np.zeros((9, 9), dtype=int)
        self.solution = None
        self.attempts = 0
        self.backtracks = 0

    def generate(self, difficulty):
        self.solution = np.zeros((9, 9), dtype=int)
        self._fill_diagonal()
        self._solve_silently()

        self.puzzle = self.solution.copy()
        squares_to_remove = 40 + difficulty * 10
        while squares_to_remove > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.puzzle[row][col] != 0:
                self.puzzle[row][col] = 0
                squares_to_remove -= 1

    def clear(self):
        self.puzzle = np.zeros((9, 9), dtype=int)
        self.solution = None
        self.attempts = 0
        self.backtracks = 0

    def _fill_diagonal(self):
        for i in range(0, 9, 3):
            self._fill_box(i, i)

    def _fill_box(self, row, col):
        num = list(range(1, 10))
        random.shuffle(num)
        index = 0
        for i in range(3):
            for j in range(3):
                self.solution[row + i][col + j] = num[index]
                index += 1

    def _solve_silently(self):
        find = self._find_empty()
        if not find:
            return True
        row, col = find

        for num in range(1, 10):
            if self._is_valid(num, (row, col)):
                self.solution[row][col] = num
                if self._solve_silently():
                    return True
                self.solution[row][col] = 0
        return False

    def solve_with_logging(self):
        start_time = time.time()
        self.attempts = 0
        self.backtracks = 0
        print("Starting Sudoku solver...")
        print("Initial puzzle:")
        self._print_board(self.solution)
        solved = self._backtrack_solve()
        end_time = time.time()

        elapsed_time = end_time - start_time
        print("\nSolving complete!")
        print(f"Solution {'found' if solved else 'not found'}.")
        print(f"Total attempts: {self.attempts}")
        print(f"Total backtracks: {self.backtracks}")
        print(f"Time taken: {elapsed_time:.4f} seconds")
        if solved:
            print("\nFinal solution:")
            self._print_board(self.solution)
        return solved

    def _backtrack_solve(self):
        find = self._find_empty()
        if not find:
            return True
        row, col = find

        for num in range(1, 10):
            self.attempts += 1
            print(f"\nAttempt #{self.attempts}: Trying {num} at position ({row}, {col})")

            if self._is_valid(num, (row, col)):
                self.solution[row][col] = num
                print(f"Placed {num} at ({row}, {col})")
                self._print_board(self.solution)

                if self._backtrack_solve():
                    return True

                self.backtracks += 1
                print(f"\nBacktrack #{self.backtracks}: Removing {num} from ({row}, {col})")
                self.solution[row][col] = 0

        return False

    def _find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.solution[i][j] == 0:
                    return (i, j)
        return None

    def _is_valid(self, num, pos):
        # Checking the row for the puzzle
        for i in range(9):
            if self.solution[pos[0]][i] == num and pos[1] != i:
                return False
        # Checking the column for puzzle
        for i in range(9):
            if self.solution[i][pos[1]] == num and pos[0] != i:
                return False
        # Checkin the puzzle 3x3 box
        box_x = pos[1] // 3
        box_y = pos[0] // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if self.solution[i][j] == num and (i, j) != pos:
                    return False
        return True

    def _print_board(self, board):
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - - -")
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    print("|", end=" ")
                if j == 8:
                    print(board[i][j])
                else:
                    print(str(board[i][j]) + " ", end="")


class SudokuUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku Solver")
        self.geometry("400x600")
        self.sudoku = Sudoku()
        self.entries = []
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(padx=10, pady=10)

        for i in range(9):
            row_entries = []
            for j in range(9):
                entry = ttk.Entry(frame, width=2, font=('Arial', 20, 'bold'), justify='center')
                entry.grid(row=i, column=j, padx=2, pady=2)
                row_entries.append(entry)
            self.entries.append(row_entries)

        ttk.Button(self, text="Generate Puzzle", command=self.generate_puzzle).pack(pady=5)
        ttk.Button(self, text="Solve with Backtracking", command=self.solve_backtracking).pack(pady=5)
        ttk.Button(self, text="Clear Puzzle", command=self.clear_puzzle).pack(pady=5)

    def generate_puzzle(self):
        difficulty = random.randint(0, 3)
        self.sudoku.generate(difficulty)
        self.display_puzzle(self.sudoku.puzzle)
        print("New puzzle generated.")

    def display_puzzle(self, puzzle):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                if puzzle[i][j] != 0:
                    self.entries[i][j].insert(0, str(puzzle[i][j]))

    def solve_backtracking(self):
        # Updating Sudoku object with input from me
        for i in range(9):
            for j in range(9):
                value = self.entries[i][j].get()
                self.sudoku.puzzle[i][j] = int(value) if value.isdigit() else 0

        print("Starting to solve the Sudoku puzzle...")
        self.sudoku.solution = np.copy(self.sudoku.puzzle)
        if self.sudoku.solve_with_logging():
            self.display_puzzle(self.sudoku.solution)
            print("Sudoku puzzle solved successfully!")
        else:
            messagebox.showerror("Error", "No solution exists.")

    def clear_puzzle(self):
        self.sudoku.clear()
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
        print("Puzzle cleared.")


if __name__ == "__main__":
    app = SudokuUI()
    app.mainloop()
