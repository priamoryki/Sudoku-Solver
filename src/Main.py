from SudokuSolver import dfs_solution, default_solution, mixed_solution, BOARD_TYPE
from tkinter import Tk, Label, StringVar, Button, Entry, Canvas, BOTH

n = 3
root_width, root_height = 120 + 50 * (n ** 2) - 20, 90 + 50 * (n ** 2) - 20

root = Tk()
canvas = Canvas(root)
root.title("Sudoku Solver")
width, height = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry(f"{root_width}x{root_height}+{(width - root_width) // 2}+{(height - root_height) // 2}")
root.resizable(False, False)

text_var = [[StringVar() for _ in range(n ** 2)] for _ in range(n ** 2)]
table = [[Entry() for _ in range(n ** 2)] for _ in range(n ** 2)]


def get_matrix():
    matrix = [[text_var[i][j].get() for j in range(n ** 2)] for i in range(n ** 2)]
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            try:
                matrix[i][j] = int(matrix[i][j])
            except ValueError:
                matrix[i][j] = 0
            if not (0 <= matrix[i][j] <= n ** 2):
                matrix[i][j] = 0
    result = mixed_solution(matrix)
    canvas.delete("all")
    create_resulting_window(mixed_solution(result))


def create_separating_lines():
    for x in range(60 + 50 * n - 10, root_width - 60, 50 * n):
        canvas.create_line(x, 45, x, root_width - 75)
    for y in range(45 + 50 * n - 10, root_height - 75, 50 * n):
        canvas.create_line(60, y, root_height - 30, y)


def create_starting_window():
    create_separating_lines()

    canvas.create_window(root_width // 2, 20, width=100, window=Label(text='Enter the board'))

    y2 = 0
    for i in range(n ** 2):
        x2 = 0
        for j in range(n ** 2):
            table[i][j] = Entry(canvas, textvariable=text_var[i][j])
            canvas.create_window(75 + x2, 60 + y2, width=30, height=30, window=table[i][j])
            x2 += 50
        y2 += 50

    canvas.create_window(root_width // 2, root_height - 25, width=100, window=Button(text='Submit', command=get_matrix))
    canvas.pack(fill=BOTH, expand=1)


def create_resulting_window(result: BOARD_TYPE):
    create_separating_lines()

    y2 = 0
    for i in range(n ** 2):
        x2 = 0
        for j in range(n ** 2):
            canvas.create_window(75 + x2, 60 + y2, width=40, height=40,
                                 window=Button(text=result[i][j], bg="green", font=1))
            x2 += 50
        y2 += 50

    canvas.pack(fill=BOTH, expand=1)


create_starting_window()
root.mainloop()
