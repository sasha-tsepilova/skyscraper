'''
Github url:
https://github.com/sasha-tsepilova/skyscraper
This module checks correctness of the given board
(game skyscrapers)
'''
def read_input(path: str):
    """
    Read game board file from path.
    Return list of str.

    >>> read_input("check.txt")
    ['***21**', '452453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***']
    """
    reading = open(path, 'r')
    lines = reading.readlines()
    for index, line in enumerate(lines):
        line = line.rstrip('\n')
        lines[index] = line

    return lines


def left_to_right_check(input_line: str, pivot: int):
    """
    Check row-wise visibility from left to right.
    Return True if number of building from the left-most hint is visible looking to the right,
    False otherwise.

    input_line - representing board row.
    pivot - number on the left-most hint of the input_line.

    >>> left_to_right_check("412453*", 4)
    True
    >>> left_to_right_check("452453*", 4)
    False
    """
    without_hints = input_line[1:-1]
    curent_visible = 0
    all_visible = 0

    for height in without_hints:
        if int(height) > curent_visible:
            all_visible += 1
            curent_visible = int(height)

    return all_visible == pivot


def check_not_finished_board(board: list):
    """
    Check if skyscraper board is not finished, i.e., '?' present on the game board.

    Return True if finished, False otherwise.

    >>> check_not_finished_board(['***21**', '4?????*', '4?????*', '*?????5', '*?????*', '*?????*'\
, '*2*1***'])
    False
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*'\
, '*2*1***'])
    True
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*5?3215', '*35214*', '*41532*'\
, '*2*1***'])
    False
    """
    for row in board:
        if '?' in row:
            return False

    return True


def check_uniqueness_in_rows(board: list):
    """
    Check buildings of unique height in each row.

    Return True if buildings in a row have unique length, False otherwise.

    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*'\
, '*2*1***'])
    True
    >>> check_uniqueness_in_rows(['***21**', '452453*', '423145*', '*543215', '*35214*', '*41532*'\
, '*2*1***'])
    False
    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*553215', '*35214*', '*41532*'\
, '*2*1***'])
    False
    """
    for index, row in enumerate(board):

        if index not in (0, len(board) - 1):
            without_hints = row[1:-1]
            row_single = set(without_hints)

            if len(without_hints) != len(row_single):
                return False

    return True


def check_horizontal_visibility(board: list):
    """
    Check row-wise visibility (left-right and vice versa)

    Return True if all horizontal hints are satisfiable,
     i.e., for line 412453* , hint is 4, and 1245 are the four buildings
      that could be observed from the hint looking to the right.

    >>> check_horizontal_visibility(['***21**', '412453*', '423145*', '*543215', '*35214*'\
, '*41532*', '*2*1***'])
    True
    >>> check_horizontal_visibility(['***21**', '452453*', '423145*', '*543215', '*35214*'\
, '*41532*', '*2*1***'])
    False
    >>> check_horizontal_visibility(['***21**', '452413*', '423145*', '*543215', '*35214*'\
, '*41532*', '*2*1***'])
    False
    """
    for index, row in enumerate(board):
        if index not in (0, len(board) - 1):

            if row[0] != '*':
                pivot = int(row[0])
                if not left_to_right_check(row, pivot):
                    return False

            if row[-1] != '*':
                pivot = int(row[-1])
                if not left_to_right_check(row[::-1], pivot):
                    return False
    return True



def check_columns(board: list):
    """
    Check column-wise compliance of the board for uniqueness (buildings of unique height) and
    visibility (top-bottom and vice versa).

    Same as for horizontal cases, but aggregated in one function for vertical case, i.e. columns.

    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*',\
 '*2*1***'])
    True
    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41232*',\
 '*2*1***'])
    False
    >>> check_columns(['***21**', '412553*', '423145*', '*543215', '*35214*', '*41532*',\
 '*2*1***'])
    False
    """
    length = len(board)
    turned_board = [''] * length

    for i in range(length):
        for j in range(length):
            turned_board[j] += board[i][j]

    if not check_uniqueness_in_rows(turned_board):
        return False

    return check_horizontal_visibility(turned_board)



def check_skyscrapers(input_path: str):
    """
    Main function to check the status of skyscraper game board.
    Return True if the board status is compliant with the rules,
    False otherwise.

    >>> check_skyscrapers("check.txt")
    True
    """
    board = read_input(input_path)

    if not check_not_finished_board(board) or not check_columns(board)\
        or not check_uniqueness_in_rows(board) or not check_horizontal_visibility(board):
        return False

    return True



if __name__ == "__main__":
    print(check_skyscrapers("skyscrapers/check.txt"))
