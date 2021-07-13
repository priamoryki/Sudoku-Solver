from os import listdir
from SudokuSolver import dfs_solution, default_solution, mixed_solution


def read_board(file):
    with open(file, 'r') as inp:
        n = int(inp.readline())
        return [list(map(int, inp.readline().split())) for _ in range(n ** 2)]


def run_tests(realization=mixed_solution):
    for file in listdir('tests/sudokus'):
        '''if (file in ['EVIL1.txt', 'EVIL2.txt', 's04b.txt', 's05a.txt', 's05b.txt', 's05c.txt', 's12a.txt', 
        's12b.txt', 's12c.txt', 's15a.txt', 's15b.txt', 's15c.txt', 's16.txt']):
            continue'''
        board = read_board('tests/sudokus/' + file)
        result = realization(board)
        expected = read_board('tests/solutions/' + file)
        if (result != expected):
            print('--------------------------------------------------')
            print(f"Wrong answer on test {file}\nCorrect answer: {expected}\nYour answer: {result}")
            print('--------------------------------------------------')
            return
        else:
            print(f"Test {file} result: OK")
    print('\n--------------------------------------------------\n                 ALL TESTS PASSED'
          '\n--------------------------------------------------\n')


if (__name__ == '__main__'):
    print('--------------------------------------------------\n                   TESTS START'
          '\n--------------------------------------------------\n')
    run_tests()
