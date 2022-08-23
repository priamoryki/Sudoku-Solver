import _thread
import threading
from contextlib import contextmanager
from os import listdir
from SudokuSolver import dfs_solution, default_solution, mixed_solution, BOARD_TYPE


class TimeoutException(Exception):
    pass


@contextmanager
def time_limit(seconds):
    timer = threading.Timer(seconds, lambda: _thread.interrupt_main())
    timer.start()
    try:
        yield
    except KeyboardInterrupt:
        raise TimeoutException("Timed out!")
    finally:
        timer.cancel()


def print_header(name, amount=50):
    print('-' * amount, ' ' * ((amount - len(name)) // 2) + name, '-' * amount, sep='\n')


def read_board(file) -> BOARD_TYPE:
    with open(file, 'r') as inp:
        n = int(inp.readline())
        return [list(map(int, inp.readline().split())) for _ in range(n ** 2)]


def run_tests(realization=default_solution):
    for file in listdir('tests/sudokus'):
        if file in ['s15a.txt', 's15c.txt']:
            continue
        board = read_board('tests/sudokus/' + file)
        try:
            with time_limit(2):
                result = realization(board)
        except TimeoutException:
            print_header(f"Timed out on test {file}")
            return
        expected = read_board('tests/solutions/' + file)
        if result != expected:
            print_header(f"Wrong answer on test {file}\nCorrect answer: {expected}\nYour answer: {result}")
            return
        else:
            print(f"Test {file} result: OK")
    print_header("ALL TESTS PASSED")


if __name__ == '__main__':
    print_header("TESTS START")
    run_tests()
