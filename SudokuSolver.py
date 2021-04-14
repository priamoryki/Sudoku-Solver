board = []
posboard = []
for i in range(9):
    posboard.append([])
    for j in range(9):
        posboard[i].append([1, 2, 3, 4, 5, 6, 7, 8, 9])


def num_of_empty_sells():
    res = 0
    for i in board:
        res += i.count(0)
    return res


def solve():
    read_board()
    while (num_of_empty_sells() != 0):
        for i in range(9):
            for j in range(9):
                if (board[i][j] == 0):
                    default_check(i, j)
                    advanced_check(i, j)
                    fill(i, j)
    print_board()


def read_board():
    for i in range(9):
        board.append(list(map(int, input().split())))
        for j in range(9):
            if (board[i][j] != 0):
                posboard[i][j] = []


def print_board():
    print('RESULTING BOARD:')
    for i in board:
        for j in i:
            print(j, end=' ')
        print()


def update_posboard(i, j, value):
    try:
        posboard[i][j].remove(value)
    except (Exception):
        pass


def get_shifts(v):
    block_size = 3
    result = [i for i in range(1, block_size)]
    shift = v % block_size + 1
    for i in range(len(result)):
        if (result[i] == shift):
            shift -= 1
        result[i] -= shift
    return result


def default_check(i, j):
    for new_i in range(9):
        update_posboard(i, j, board[new_i][j])

    for new_j in range(9):
        update_posboard(i, j, board[i][new_j])

    i_shifts, j_shifts = get_shifts(i), get_shifts(j)

    for i_shift in i_shifts:
        for j_shift in j_shifts:
            update_posboard(i, j, board[i + i_shift][j + j_shift])


def advanced_check(i, j):
    for value in posboard[i][j]:
        is_change = True
        for new_i in range(9):
            if (new_i != i and value in posboard[new_i][j]):
                is_change = False

        if (is_change):
            posboard[i][j] = [value]

        is_change = True
        for new_j in range(9):
            if (new_j != j and value in posboard[i][new_j]):
                is_change = False

        if (is_change):
            posboard[i][j] = [value]

        is_change = True
        i_shifts, j_shifts = get_shifts(i), get_shifts(j)
        i_shifts.append(0)
        j_shifts.append(0)
        for i_shift in i_shifts:
            for j_shift in j_shifts:
                if (not (i_shift == 0 and j_shift == 0) and value in posboard[i + i_shift][j + j_shift]):
                    is_change = False

        if (is_change):
            posboard[i][j] = [value]


def fill(i, j):
    if (len(posboard[i][j]) == 1):
        board[i][j] = posboard[i][j][0]
        posboard[i][j] = []
        # print_board()
        # print(i, j, board[i][j])
        # print(num_of_empty_sells())


'''
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
'''


solve()