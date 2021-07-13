"""SudokuSolver.py"""

__author__ = "Lymar Pavel"

from math import sqrt
from copy import deepcopy


def read_board(n):
    board = []
    for i in range(n ** 2):
        board.append(list(map(int, input().split())))
    return board


def print_board(board):
    print('RESULTING BOARD:')
    for i in board:
        print(*i)


def default_solution(board):
    """
    Smart and fast solution.
    Bad with evil tests (so far).
    """
    n = int(sqrt(len(board)))
    board = deepcopy(board)
    posboard = [[[*range(1, n ** 2 + 1)] if board[i][j] == 0 else [] for j in range(n ** 2)] for i in range(n ** 2)]

    def num_of_empty_sells():
        res = 0
        for i in board:
            res += i.count(0)
        return res

    def solve():
        iters_without_update = 0
        while (num_of_empty_sells() != 0):
            if (iters_without_update > 2 * n ** 4):
                break
            for i in range(n ** 2):
                for j in range(n ** 2):
                    if (board[i][j] == 0):
                        default_check(i, j)
                        advanced_check(i, j)
                        fill(i, j)
                        if (board[i][j] == 0):
                            iters_without_update += 1

    def update_posboard(i, j, value):
        try:
            posboard[i][j].remove(value)
        except (ValueError):
            pass

    def get_shifts(v):
        result = [*range(1, n)]
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

            is_change = True
            i_shifts, j_shifts = get_shifts(i), [0, *get_shifts(j)]
            for i_shift in i_shifts:
                for j_shift in j_shifts:
                    if (value in posboard[i + i_shift][j + j_shift]):
                        is_change = False

            if (is_change):
                for new_j in range(n ** 2):
                    if ((new_j - j) not in j_shifts):
                        update_posboard(i, new_j, value)

            is_change = True
            i_shifts, j_shifts = [0, *get_shifts(i)], get_shifts(j)
            for i_shift in i_shifts:
                for j_shift in j_shifts:
                    if (value in posboard[i + i_shift][j + j_shift]):
                        is_change = False

            if (is_change):
                for new_i in range(n ** 2):
                    if ((new_i - i) not in i_shifts):
                        update_posboard(new_i, j, value)

    def fill(i, j):
        if (len(posboard[i][j]) == 1):
            board[i][j] = posboard[i][j].pop()
            # print_board(board)
            # print_board(posboard)
            # print(i, j, board[i][j])
            # print(num_of_empty_sells())

    solve()
    return board


def dfs_solution(board):
    """Slow, but better with evil tests (so far)"""
    n = int(sqrt(len(board)))
    board = deepcopy(board)
    row_constrain = [[0] * (n ** 2) for _ in range(n ** 2)]
    col_constrain = [[0] * (n ** 2) for _ in range(n ** 2)]
    box_constrain = [[0] * (n ** 2) for _ in range(n ** 2)]

    def solve():
        for i in range(n ** 2):
            for j in range(n ** 2):
                if (board[i][j] == 0):
                    continue
                box, tmp = i // n * n + j // n, board[i][j] - 1
                row_constrain[i][tmp], col_constrain[j][tmp], box_constrain[box][tmp] = 1, 1, 1
        dfs(0, 0)

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
            board[r][c] = i + 1
            if (dfs(next_r, next_c)):
                return True
            board[r][c] = 0
            row_constrain[r][i], col_constrain[c][i], box_constrain[box][i] = 0, 0, 0

    solve()
    return board


def mixed_solution(board):
    return dfs_solution(default_solution(board))


if (__name__ == '__main__'):
    n = int(input().split()[0])
    board = read_board(n)

    print_board(mixed_solution(board))
