import random as rnd
import curses, time

debug = False

def init_board(x: int, y: int) -> list:
    '''Instatitate the board with dimensions x,y given.
    Returns array filled with random numbers'''

    return [[rnd.randint(1,9) for i in range(x)] for j in range(y)]


def init_player(board: list) -> tuple:
    '''Places the player at a random position in the board.
    Returns the position of the player as a tuple.'''

    y,x = (rnd.randrange(len(board)), rnd.randrange(len(board[0])))
    board[y][x] = "@"

    return (y,x)


def draw_window(win, board: list, score: float):
    '''Draw the window with the current board state'''

    win.clear()
    for i in board:
        win.addch('\n')
        for j in i:
            if isinstance(j, str):
                win.addstr(f"{j} ")
            else:
                win.addstr(f"{j} ", curses.color_pair(j+2))
    win.addstr('\n\n')
    win.addstr(f"Cleared: {score:.2f}%")
    win.refresh()


def rotate_matrix(m: list) -> list:
    '''Rotate matrix in counter clockwise direction'''

    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0])-1,-1,-1)]


def rotate_board(board: list, direct: int) -> tuple:
    '''Rotate the board to match direction.
    Return the new board and player position with transposed coordinates.'''

    board_t = board.copy()

    for i in range(direct): # rotate board n times to match direction
        board_t = rotate_matrix(board_t)
    for i,j in enumerate(board_t): # update player position by searching for player
        try:
            j.index("@")
            pos_t = tuple((i,j.index("@")))
            break
        except:
            pass

    return board_t, pos_t


def valid_path_in_dir(board: list, pos: tuple, direct: int) -> bool:
    '''Checks if the path in given direction from player position is valid.
    0: right, 1: down, 2: left, 3: up'''

    board_t, pos_t = rotate_board(board, direct)
    y, x = pos_t

    try:
        step_length = int(board_t[y][x+1]) # checks if adjacant field is a num
        if step_length + x >= len(board_t[0]): # checks if path is oob
            return False
        elif not all(isinstance(board_t[y][x+i], int) for i in range(1, step_length+1)):
            return False
        else:
            return True
    except:
        return False # if adjacent not int




def any_valid_path(board: list, pos: tuple) -> bool:
    '''Checks if there is a valid path at player position.
    Returns True if, else False.'''

    return any(valid_path_in_dir(board, pos, i) for i in range(4))


def player_input(win, board: list, pos: tuple) -> int:
    '''Asks player for input. Checks if chosen direction is valid.'''

    wasd = ('D', 'S', 'A', 'W')
    key = ""
    direct = -1

    while direct == -1 or not valid_path_in_dir(board, pos, direct):
        key = ""
        while key not in ['W','A','S','D']:
            key = win.getkey().upper()
        direct = wasd.index(key)

    return direct


def player_move(board: list, pos: tuple, direct: int) -> list:
    '''Move the player in the given direction.'''

    board_t, pos_t = rotate_board(board, direct)
    y, x = pos_t
    step_length = board_t[y][x+1]
    for i in range(step_length):
        board_t[y][x+i] = " "
    board_t[y][x+step_length] = "@" # update board with new player position
    board_t, jkasdf = rotate_board(board_t, 4-direct) # rotate the board back to og orientation
    return board_t


def get_score(board: list) -> float:
    '''Calculates the score as percentage of cleared board'''

    total = len(board) * len(board[0])
    empty = 0
    for i in board:
        empty += i.count(" ")

    score = empty / total * 100

    return score


def main():

    b_heigth = 15
    b_width = 36

    parent = curses.initscr()
    curses.noecho()
    curses.start_color()
    curses.use_default_colors()
    max_h, max_w = parent.getmaxyx()
    win_h = b_heigth+3
    win_w = b_width*2+2
    center_x = int(max_w/2) - int(win_w/2)

    for i in range(11):
        curses.init_pair(i + 1, i, -1)

    win = curses.newwin(win_h, win_w, 2, center_x)
    win.keypad(True)
    win.nodelay(False)
    curses.curs_set(False)

    while True:
        board = init_board(b_width, b_heigth)
        pos = init_player(board)

        # help player orient
        board_present = [[" " for i in range(b_width)] for j in range(b_heigth)]
        board_present[pos[0]][pos[1]] = "@"
        for i in range(2):
            draw_window(win, board, 0)
            time.sleep(0.7)
            draw_window(win, board_present, 0)
            time.sleep(0.7)

        while True:
            score = get_score(board)
            draw_window(win, board, score)
            if not any_valid_path(board, pos):
                break
            direct = player_input(win, board, pos)
            board = player_move(board, pos, direct)

        win.addstr(win_h-1, int(win_w/2 - 5), "Game Over")
        win.refresh()
        time.sleep(2)
        win.addstr(win_h-1, int(win_w - 26), "Wanna play again? (y/n)")
        win.refresh()
        time.sleep(2)

        key = -1
        while key not in (110, 121):
            key = win.getch()
        if key == 110: # ascii key for n key
            break
        if key == 121: # ascii key for y key
            continue

    curses.endwin()

if __name__ == "__main__":
    main()
