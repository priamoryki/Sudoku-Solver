"""SudokuSolver.py"""

__author__ = "Lymar Pavel"


def print_board(board):
    print('RESULTING BOARD:')
    for i in board:
        print(*i)


'''
Smart and fast solution
Bad with evil tests (so far)
'''


def default_solution(n):
    board = []
    posboard = [[[k for k in range(1, n ** 2 + 1)] for _ in range(n ** 2)] for _ in range(n ** 2)]

    def num_of_empty_sells():
        res = 0
        for i in board:
            res += i.count(0)
        return res

    def solve():
        read_board()
        while (num_of_empty_sells() != 0):
            for i in range(n ** 2):
                for j in range(n ** 2):
                    if (board[i][j] == 0):
                        default_check(i, j)
                        advanced_check(i, j)
                        fill(i, j)

    def read_board():
        for i in range(n ** 2):
            board.append(list(map(int, input().split())))
            for j in range(n ** 2):
                if (board[i][j] != 0):
                    posboard[i][j] = []

    def update_posboard(i, j, value):
        try:
            posboard[i][j].remove(value)
        except (Exception):
            pass

    def get_shifts(v):
        result = [i for i in range(1, n)]
        shift = v % n + 1
        for i in range(len(result)):
            if (result[i] == shift):
                shift -= 1
            result[i] -= shift
        return result

    def default_check(i, j):
        for new_i in range(n ** 2):
            update_posboard(i, j, board[new_i][j])

        for new_j in range(n ** 2):
            update_posboard(i, j, board[i][new_j])

        i_shifts, j_shifts = get_shifts(i), get_shifts(j)

        for i_shift in i_shifts:
            for j_shift in j_shifts:
                update_posboard(i, j, board[i + i_shift][j + j_shift])

    def advanced_check(i, j):
        for value in posboard[i][j]:
            is_change = True
            for new_i in range(n ** 2):
                if (new_i != i and value in posboard[new_i][j]):
                    is_change = False

            if (is_change):
                posboard[i][j] = [value]

            is_change = True
            for new_j in range(n ** 2):
                if (new_j != j and value in posboard[i][new_j]):
                    is_change = False

            if (is_change):
                posboard[i][j] = [value]

            is_change = True
            i_shifts, j_shifts = [0, *get_shifts(i)], [0, *get_shifts(j)]
            for i_shift in i_shifts:
                for j_shift in j_shifts:
                    if (not (i_shift == 0 and j_shift == 0) and value in posboard[i + i_shift][j + j_shift]):
                        is_change = False

            if (is_change):
                posboard[i][j] = [value]

    def fill(i, j):
        if (len(posboard[i][j]) == 1):
            board[i][j] = posboard[i][j].pop()
            # print_board(board)
            # print(i, j, board[i][j])
            # print(num_of_empty_sells())

    solve()
    return board


'''
Slow, but better with evil tests (so far)
'''


def dfs_solution(n):
    board = []
    row_constrain = [[0] * (n ** 2) for i in range(n ** 2)]
    col_constrain = [[0] * (n ** 2) for i in range(n ** 2)]
    box_constrain = [[0] * (n ** 2) for i in range(n ** 2)]

    def solve():
        read_board()
        for i in range(n ** 2):
            for j in range(n ** 2):
                if (board[i][j] == 0):
                    continue
                box = i // n * n + j // n
                tmp = int(board[i][j]) - 1
                row_constrain[i][tmp], col_constrain[j][tmp], box_constrain[box][tmp] = 1, 1, 1
        dfs(0, 0)

    def read_board():
        for i in range(n ** 2):
            board.append(list(map(int, input().split())))

    def dfs(r, c):
        if (r == n ** 2):
            return True
        next_r, next_c = (r, c + 1) if c != n ** 2 - 1 else (r + 1, 0)
        if (board[r][c] != 0):
            return dfs(next_r, next_c)

        box = r // n * n + c // n
        for i in range(n ** 2):
            if (row_constrain[r][i] or col_constrain[c][i] or box_constrain[box][i]):
                continue
            row_constrain[r][i], col_constrain[c][i], box_constrain[box][i] = 1, 1, 1
            board[r][c] = str(i + 1)
            if (dfs(next_r, next_c)):
                return True
            board[r][c] = 0
            row_constrain[r][i], col_constrain[c][i], box_constrain[box][i] = 0, 0, 0

    solve()
    return board


'''
2x2:
    3 4 1 0
    0 2 0 0
    0 0 2 0
    0 1 4 3

    0 4 0 0
    0 0 0 3
    2 0 0 0
    0 0 1 0

3x3:
    EASY TEST
    0 0 4 0 8 0 3 0 0
    0 0 0 0 0 3 0 4 2
    8 0 0 4 0 5 9 0 7
    3 0 2 0 7 0 5 0 8
    0 5 0 0 0 0 0 7 0
    6 0 8 0 9 0 2 0 1
    4 0 6 2 0 7 0 0 9
    5 2 0 9 0 0 0 0 0
    0 0 7 0 1 0 4 0 0

    MEDIUM TEST
    0 0 0 0 9 7 0 0 6
    5 0 0 2 0 0 1 0 4
    3 0 0 0 0 1 0 7 0
    0 9 3 8 0 5 0 0 7
    0 0 0 0 1 0 0 0 0
    4 0 0 7 0 6 5 9 0
    0 4 0 1 0 0 0 0 9
    8 0 2 0 0 9 0 0 1
    9 0 0 6 4 0 0 0 0

    HARD TEST
    0 8 0 0 9 4 0 0 0
    0 0 9 1 7 0 0 0 0
    4 0 1 0 0 0 0 0 3
    0 0 8 0 0 0 0 2 0
    5 0 0 9 1 3 0 0 8
    0 9 0 0 0 0 4 0 0
    3 0 0 0 0 0 8 0 6
    0 0 0 0 5 8 2 0 0
    0 0 0 2 3 0 0 4 0

    EVIL TEST
    0 0 5 2 8 0 0 0 0
    0 0 0 0 0 4 1 0 0
    0 0 9 0 0 0 4 0 3
    9 0 0 7 0 0 0 6 0
    0 8 0 0 1 0 0 4 0
    0 5 0 0 0 9 0 0 1
    4 0 6 0 0 0 2 0 0
    0 0 7 4 0 0 0 0 0
    0 0 0 0 2 5 6 0 0

4x4:
    13 0  0  7  0  0  0  0  0  5  14 2  0  0  9  0
    0  14 0  0  5  15 0  0  9  8  7  0  13 4  0  0
    0  15 0  2  6  0  12 4  11 0  16 10 0  0  0  0
    12 0  0  16 1  0  0  0  6  0  0  0  0  10 0  0
    0  0  2  0  0  16 0  0  0  0  0  8  3  1  0  4
    0  5  11 0  0  6  2  3  0  0  0  0  0  0  0  0
    0  0  0  15 0  10 11 0  5  12 0  1  0  7  0  8
    0  0  0  4  8  7  0  0  0  3  0  0  0  5  15 0
    6  0  0  0  0  0  10 0  0  0  0  0  9  0  13 7
    0  0  1  0  0  0  0  0  0  0  4  0  0  8  11 16
    0  11 8  13 15 0  14 0  10 2  0  0  0  0  5  0
    0  0  3  0  0  0  9  6  0  0  0  0  0  15 12 0
    9  0  0  0  0  0  0  1  0  4  0  14 0  3  0  0
    3  0  0  0  13 0  0  14 7  0  11 0  0  0  6  0
    5  0  0  0  7  0  0  16 12 0  13 0  1  0  0  0
    0  0  0  0  0  0  3  11 0  15 0  0  0  0  14 2
'''

print_board(default_solution(4))

print_board(dfs_solution(4))
