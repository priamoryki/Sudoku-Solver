"""SudokuSolver.py"""

__author__ = "Lymar Pavel"

from typing import *
from math import sqrt
from copy import deepcopy

BOARD_TYPE = List[List[int]]
DEBUG = False


def read_board(n) -> BOARD_TYPE:
    board = []
    for i in range(n ** 2):
        board.append(list(map(int, input().split())))
    return board


def print_board(board: BOARD_TYPE):
    print('RESULTING BOARD:')
    for i in board:
        print(*i)


def default_solution(board: BOARD_TYPE) -> BOARD_TYPE:
    """
    Smart and fast solution.
    """
    n = int(sqrt(len(board)))
    board = deepcopy(board)
    posboard = [[{*range(1, n ** 2 + 1)} if board[i][j] == 0 else set() for j in range(n ** 2)] for i in range(n ** 2)]

    def num_of_empty_cells() -> int:
        res = 0
        for i in board:
            res += i.count(0)
        return res

    def solve():
        iters_without_update = 0
        while num_of_empty_cells() != 0:
            if iters_without_update > (2 * n) ** 4:
                break
            for i in range(n ** 2):
                for j in range(n ** 2):
                    if board[i][j] == 0:
                        default_check(i, j)
                        advanced_check(i, j)
                        fill(i, j)
                        if board[i][j] == 0:
                            iters_without_update += 1
        if DEBUG:
            print_board(posboard)

    def update_posboard(i, j, *values) -> None:
        for value in values:
            try:
                posboard[i][j].remove(value)
            except KeyError:
                pass

    def get_shifts(v) -> List[int]:
        result = [*range(1, n)]
        shift = v % n + 1
        for i in range(len(result)):
            if result[i] == shift:
                shift -= 1
            result[i] -= shift
        return result

    def get_cell_value(cell: Tuple[int, int]) -> int:
        return board[cell[0]][cell[1]]

    def get_row_cells(i, j) -> List[Tuple[int, int]]:
        return [(new_i, j) for new_i in range(n ** 2) if new_i != i]

    def get_column_cells(i, j) -> List[Tuple[int, int]]:
        return [(i, new_j) for new_j in range(n ** 2) if new_j != j]

    def get_box_cells(i, j) -> List[Tuple[int, int]]:
        i_shifts, j_shifts = [0, *get_shifts(i)], [0, *get_shifts(j)]
        cells = [
            (i + i_shift, j + j_shift)
            for i_shift in i_shifts
            for j_shift in j_shifts
            if not (i_shift == 0 and j_shift == 0)
        ]
        return cells

    def default_check(i, j) -> None:
        for cell in get_row_cells(i, j):
            update_posboard(i, j, get_cell_value(cell))

        for cell in get_column_cells(i, j):
            update_posboard(i, j, get_cell_value(cell))

        for cell in get_box_cells(i, j):
            update_posboard(i, j, get_cell_value(cell))

    def is_only_option_in_list(value, cells) -> bool:
        return not any(value in posboard[cell[0]][cell[1]] for cell in cells)

    def linked_cells(i, j, value, cells) -> None:
        success = [cell for cell in cells if value in posboard[cell[0]][cell[1]]]
        if len(success) == 1:
            new_i, new_j = success.pop()
            for new_value in posboard[i][j].intersection(posboard[new_i][new_j]):
                if new_value != value:
                    success = [cell for cell in cells if new_value in posboard[cell[0]][cell[1]]]
                    if len(success) == 1:
                        posboard[i][j], posboard[new_i][new_j] = {value, new_value}, {value, new_value}
                        return

    def same_pair(i, j, cells) -> None:
        for cell in cells:
            if posboard[i][j] == posboard[cell[0]][cell[1]]:
                for new_cell in cells:
                    if new_cell != cell:
                        update_posboard(*new_cell, *posboard[i][j])

    def advanced_check(i, j) -> None:
        for value in posboard[i][j]:
            # check if value is the only option for this column
            if is_only_option_in_list(value, get_row_cells(i, j)):
                posboard[i][j] = {value}

            # check if value is the only option for this row
            if is_only_option_in_list(value, get_column_cells(i, j)):
                posboard[i][j] = {value}

            # check if value is the only option for this box
            if is_only_option_in_list(value, get_box_cells(i, j)):
                posboard[i][j] = {value}

            # check if value is only possible in current row for this box
            i_shifts, j_shifts = get_shifts(i), [0, *get_shifts(j)]
            cells = [(i + i_shift, j + j_shift) for i_shift in i_shifts for j_shift in j_shifts]
            if is_only_option_in_list(value, cells):
                for new_j in range(n ** 2):
                    if (new_j - j) not in j_shifts:
                        update_posboard(i, new_j, value)

            # check if value is only possible in current column for this box
            i_shifts, j_shifts = [0, *get_shifts(i)], get_shifts(j)
            cells = [(i + i_shift, j + j_shift) for i_shift in i_shifts for j_shift in j_shifts]
            if is_only_option_in_list(value, cells):
                for new_i in range(n ** 2):
                    if (new_i - i) not in i_shifts:
                        update_posboard(new_i, j, value)

            # check if value is only possible in this box for current row
            i_shifts, j_shifts = get_shifts(i), [0, *get_shifts(j)]
            cells = [(i, new_j) for new_j in range(n ** 2) if (new_j - j) not in j_shifts]
            if is_only_option_in_list(value, cells):
                for i_shift in i_shifts:
                    for j_shift in j_shifts:
                        update_posboard(i + i_shift, j + j_shift, value)

            # check if value is only possible in this box for current column
            i_shifts, j_shifts = [0, *get_shifts(i)], get_shifts(j)
            cells = [(new_i, j) for new_i in range(n ** 2) if (new_i - i) not in i_shifts]
            if is_only_option_in_list(value, cells):
                for i_shift in i_shifts:
                    for j_shift in j_shifts:
                        update_posboard(i + i_shift, j + j_shift, value)

            # linked cells
            if len(posboard[i][j]) > 2:
                linked_cells(i, j, value, get_row_cells(i, j))
                linked_cells(i, j, value, get_column_cells(i, j))
                linked_cells(i, j, value, get_box_cells(i, j))

            if len(posboard[i][j]) == 2:
                same_pair(i, j, get_row_cells(i, j))
                same_pair(i, j, get_column_cells(i, j))
                same_pair(i, j, get_box_cells(i, j))

    def fill(i, j) -> None:
        if len(posboard[i][j]) == 1:
            board[i][j] = posboard[i][j].pop()
            if DEBUG:
                print(i, j, board[i][j])
                print(num_of_empty_cells())

    solve()
    return board


def dfs_solution(board: BOARD_TYPE) -> BOARD_TYPE:
    """
    Slow, but better with evil tests
    """
    n = int(sqrt(len(board)))
    board = deepcopy(board)
    row_constrain = [[0] * (n ** 2) for _ in range(n ** 2)]
    col_constrain = [[0] * (n ** 2) for _ in range(n ** 2)]
    box_constrain = [[0] * (n ** 2) for _ in range(n ** 2)]

    def solve():
        for i in range(n ** 2):
            for j in range(n ** 2):
                if board[i][j] == 0:
                    continue
                box, tmp = i // n * n + j // n, board[i][j] - 1
                row_constrain[i][tmp], col_constrain[j][tmp], box_constrain[box][tmp] = 1, 1, 1
        dfs(0, 0)

    def dfs(r, c) -> bool:
        if r == n ** 2:
            return True
        next_r, next_c = (r, c + 1) if c != n ** 2 - 1 else (r + 1, 0)
        if board[r][c] != 0:
            return dfs(next_r, next_c)

        box = r // n * n + c // n
        for i in range(n ** 2):
            if row_constrain[r][i] or col_constrain[c][i] or box_constrain[box][i]:
                continue
            row_constrain[r][i], col_constrain[c][i], box_constrain[box][i] = 1, 1, 1
            board[r][c] = i + 1
            if dfs(next_r, next_c):
                return True
            board[r][c] = 0
            row_constrain[r][i], col_constrain[c][i], box_constrain[box][i] = 0, 0, 0

    solve()
    return board


def mixed_solution(board: BOARD_TYPE) -> BOARD_TYPE:
    return dfs_solution(default_solution(board))


if __name__ == '__main__':
    n = int(input().split()[0])
    board = read_board(n)

    print_board(mixed_solution(board))
