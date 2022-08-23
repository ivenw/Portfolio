from abc import ABC
from dataclasses import dataclass
import random
import curses, time
from enum import Enum
from typing import Tuple


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class Entity(ABC):
    def __init__(self, x_pos, y_pos):
        self.value: int | str | None
        self.x_pos = x_pos
        self.y_pos = y_pos
    
class Number(Entity):
    def __init__(self, x_pos, y_pos):
        self.value = random.randint(1, 9)
        self.x_pos = x_pos
        self.y_pos = y_pos

class Empty(Entity):
    def __init__(self, x_pos, y_pos) :
        self.value = None
        self.x_pos = x_pos
        self.y_pos = y_pos

class Player(Entity):
    def __init__(self, x_pos, y_pos):
        self.value = "@"
        self.x_pos = x_pos
        self.y_pos = y_pos

        
class Board:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.map: list[list[Entity]] = [[Number(width, height) for _ in range(width)] for _ in range(height)]

    def __repr__(self):
        buffer = f"{self.width=}, {self.height=}"
        for line in self.map:
            buffer += "\n"
            for tile in line:
                if not tile.value:
                    buffer += f"  "
                buffer += f"{tile.value} "
        return buffer

    def get_entity(self, x_pos: int, y_pos: int) -> Entity:
        return self.map[y_pos][x_pos]


    def update(self, entity: Entity):
        self.map[entity.y_pos][entity.x_pos] = entity


def new_player(board: Board) -> Player:
    x_pos, y_pos = (
        random.randrange(0, board.width), 
        random.randrange(0, board.height)
    )
    player = Player(x_pos, y_pos)
    board.update(player)
    return player


def valid_move_in_direction(board: Board, player: Player, direction: Direction) -> tuple[bool, tuple[int, int]]:
    player_pos = (player.x_pos, player.y_pos)
    x_dir, y_dir = tuple_pairwise_add(player_pos, direction.value)

    if any((x_dir < 0, y_dir <0, x_dir > board.width - 1, y_dir > board.height - 1)):
        return False, (0, 0)
    
    step_length = board.get_entity(x_dir, y_dir).value

    if not isinstance(step_length, int):
        return False, (0, 0)
    
    x_dest, y_dest = tuple_pairwise_add(player_pos, tuple_mult_by(direction.value, step_length))

    if any((x_dest < 0, y_dest <0, x_dest > board.width - 1, y_dest > board.height - 1)):
        return False, (0, 0)

    return True, (x_dest, y_dest)


def any_valid_move(board: Board, player: Player) -> bool:
    return any(valid_move_in_direction(board, player, direction) for direction in Direction)


def move_player(board: Board, player: Player, direction: Direction):
    move_test = valid_move_in_direction(board, player, direction)
    if move_test[0]:
        board.update(Empty(player.x_pos, player.y_pos))
        player.x_pos, player.y_pos = move_test[1]
        board.update(player)


def tuple_pairwise_add(t1: tuple, t2: tuple, /) -> tuple:
    return tuple(sum(t) for t in zip(t1, t2))


def tuple_mult_by(t1: tuple, x: int | float, /) -> tuple:
    return tuple(t * x for t in t1)


board = Board(16, 8)
player = new_player(board)
move_player(board, player, Direction.UP)
print(board)


# def draw_window(win, board: list, score: float):
#     '''Draw the window with the current board state'''

#     win.clear()
#     for i in board:
#         win.addch('\n')
#         for j in i:
#             if isinstance(j, str):
#                 win.addstr(f"{j} ")
#             else:
#                 win.addstr(f"{j} ", curses.color_pair(j+2))
#     win.addstr('\n\n')
#     win.addstr(f"Cleared: {score:.2f}%")
#     win.refresh()


# def rotate_matrix(m: list) -> list:
#     '''Rotate matrix in counter clockwise direction'''

#     return [[m[j][i] for j in range(len(m))] for i in range(len(m[0])-1,-1,-1)]


# def rotate_board(board: list, direct: int) -> tuple:
#     '''Rotate the board to match direction.
#     Return the new board and player position with transposed coordinates.'''

#     board_t = board.copy()

#     for i in range(direct): # rotate board n times to match direction
#         board_t = rotate_matrix(board_t)
#     for i,j in enumerate(board_t): # update player position by searching for player
#         try:
#             j.index("@")
#             pos_t = tuple((i,j.index("@")))
#             break
#         except:
#             pass

#     return board_t, pos_t


# def valid_path_in_dir(board: list, pos: tuple, direct: int) -> bool:
#     '''Checks if the path in given direction from player position is valid.
#     0: right, 1: down, 2: left, 3: up'''

#     board_t, pos_t = rotate_board(board, direct)
#     y, x = pos_t

#     try:
#         step_length = int(board_t[y][x+1]) # checks if adjacant field is a num
#         if step_length + x >= len(board_t[0]): # checks if path is oob
#             return False
#         elif not all(isinstance(board_t[y][x+i], int) for i in range(1, step_length+1)):
#             return False
#         else:
#             return True
#     except:
#         return False # if adjacent not int


# def player_input(win, board: list, pos: tuple) -> int:
#     '''Asks player for input. Checks if chosen direction is valid.'''

#     wasd = ('D', 'S', 'A', 'W')
#     key = ""
#     direct = -1

#     while direct == -1 or not valid_path_in_dir(board, pos, direct):
#         key = ""
#         while key not in ['W','A','S','D']:
#             key = win.getkey().upper()
#         direct = wasd.index(key)

#     return direct


# def player_move(board: list, pos: tuple, direct: int) -> list:
#     '''Move the player in the given direction.'''

#     board_t, pos_t = rotate_board(board, direct)
#     y, x = pos_t
#     step_length = board_t[y][x+1]
#     for i in range(step_length):
#         board_t[y][x+i] = " "
#     board_t[y][x+step_length] = "@" # update board with new player position
#     board_t, jkasdf = rotate_board(board_t, 4-direct) # rotate the board back to og orientation
#     return board_t


# def get_score(board: list) -> float:
#     '''Calculates the score as percentage of cleared board'''

#     total = len(board) * len(board[0])
#     empty = 0
#     for i in board:
#         empty += i.count(" ")

#     score = empty / total * 100

#     return score


# def main():

#     b_heigth = 15
#     b_width = 36

#     parent = curses.initscr()
#     curses.noecho()
#     curses.start_color()
#     curses.use_default_colors()
#     max_h, max_w = parent.getmaxyx()
#     win_h = b_heigth+3
#     win_w = b_width*2+2
#     center_x = int(max_w/2) - int(win_w/2)

#     for i in range(11):
#         curses.init_pair(i + 1, i, -1)

#     win = curses.newwin(win_h, win_w, 2, center_x)
#     win.keypad(True)
#     win.nodelay(False)
#     curses.curs_set(False)

#     while True:
#         board = init_board(b_width, b_heigth)
#         pos = init_player(board)

#         # help player orient
#         board_present = [[" " for i in range(b_width)] for j in range(b_heigth)]
#         board_present[pos[0]][pos[1]] = "@"
#         for i in range(2):
#             draw_window(win, board, 0)
#             time.sleep(0.7)
#             draw_window(win, board_present, 0)
#             time.sleep(0.7)

#         while True:
#             score = get_score(board)
#             draw_window(win, board, score)
#             if not any_valid_path(board, pos):
#                 break
#             direct = player_input(win, board, pos)
#             board = player_move(board, pos, direct)

#         win.addstr(win_h-1, int(win_w/2 - 5), "Game Over")
#         win.refresh()
#         time.sleep(2)
#         win.addstr(win_h-1, int(win_w - 26), "Wanna play again? (y/n)")
#         win.refresh()
#         time.sleep(2)

#         key = -1
#         while key not in (110, 121):
#             key = win.getch()
#         if key == 110: # ascii key for n key
#             break
#         if key == 121: # ascii key for y key
#             continue

#     curses.endwin()

# if __name__ == "__main__":
#     main()
