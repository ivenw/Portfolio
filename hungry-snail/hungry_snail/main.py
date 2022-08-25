import random
import curses, time
from enum import Enum
import numpy as np
from typing import Protocol, cast

BOARD_WIDTH = 36
BOARD_HEIGHT = 15

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class Entity(Protocol):
    def __init__(self, x_pos: int, y_pos: int):
        self.value: int | str | None
        self.x_pos: int
        self.y_pos: int


class Number(Entity):
    def __init__(self, x_pos, y_pos):
        self.value = random.randint(1, 9)
        self.x_pos = x_pos
        self.y_pos = y_pos


class Empty(Entity):
    def __init__(self, x_pos, y_pos):
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
        self.map: list[list[Entity]] = [
            [Number(width, height) for _ in range(width)] for _ in range(height)
        ]

    def __repr__(self):
        buffer = f"{self.width=}, {self.height=}"
        for line in self.map:
            buffer += "\n"
            for tile in line:
                if not tile.value:
                    buffer += f"  "
                else:
                    buffer += f"{tile.value} "
        return buffer

    def get_entity(self, x_pos: int, y_pos: int) -> Entity:
        return self.map[y_pos][x_pos]

    def update(self, entity: Entity):
        self.map[entity.y_pos][entity.x_pos] = entity


class Window:
    def __init__(self, win_width: int, win_height: int):
        parent = curses.initscr()
        curses.noecho()
        curses.curs_set(False)
        curses.start_color()
        curses.use_default_colors()

        _, max_w = parent.getmaxyx()
        self.win_h = win_height + 3
        self.win_w = win_width * 2 + 2
        center_x = int(max_w / 2) - int(self.win_w / 2)

        self.win = curses.newwin(self.win_h, self.win_w, 2, center_x)
        self.win.keypad(True)
        self.win.nodelay(False)
        for i in range(11):
            curses.init_pair(i + 1, i, -1)

    def draw_board(self, board: Board, score: float):
        self.win.clear()
        for row in board.map:
            self.win.addch("\n")
            for entity in row:
                if isinstance(entity, Player):
                    self.win.addstr(f"{entity.value} ")
                elif isinstance(entity, Number):
                    self.win.addstr(
                        f"{entity.value} ",
                        curses.color_pair(cast(int, entity.value) + 2),
                    )
                elif isinstance(entity, Empty):
                    self.win.addstr("  ")
        self.win.addstr("\n\n")
        self.win.addstr(f"Cleared: {score:.2f}%")
        self.win.refresh()

    def draw_emtpy_board(self, board: Board, score):
        self.win.clear()
        for row in board.map:
            self.win.addch("\n")
            for entity in row:
                if isinstance(entity, Player):
                    self.win.addstr(f"{entity.value} ")
                else:
                    self.win.addstr("  ")
        self.win.addstr("\n\n")
        self.win.addstr(f"Cleared: {score:.2f}%")
        self.win.refresh()

    def flash(self, board: Board):
        for _ in range(2):
            self.draw_board(board, 0)
            time.sleep(0.7)
            self.draw_emtpy_board(board, 0)
            time.sleep(0.7)
            

    def game_over(self):
        self.win.addstr(self.win_h-1, int(self.win_w/2 - 5), "Game Over")
        self.win.refresh()
        time.sleep(2)
        self.win.addstr(self.win_h-1, int(self.win_w - 26), "Wanna play again? (y/n)")
        self.win.refresh()
        time.sleep(2)

        key = -1
        while key not in (110, 121):
            key = self.win.getch()
            if key == 110: # ascii key for n key
                break
            if key == 121: # ascii key for y key
                continue


def new_player(board: Board) -> Player:
    x_pos, y_pos = (random.randrange(0, board.width), random.randrange(0, board.height))
    player = Player(x_pos, y_pos)
    board.update(player)
    return player


def valid_move_in_direction(board: Board, player: Player, direction: Direction) -> bool:
    player_pos = np.array([player.x_pos, player.y_pos])
    dir_coors = np.array(direction.value)
    x_dir, y_dir = player_pos + dir_coors

    if any((x_dir < 0, y_dir < 0, x_dir > board.width - 1, y_dir > board.height - 1)):
        return False

    step_length = board.get_entity(x_dir, y_dir).value

    if not isinstance(step_length, int):
        return False

    x_dest, y_dest = player_pos + dir_coors * step_length

    if any(
        (x_dest < 0, y_dest < 0, x_dest > board.width - 1, y_dest > board.height - 1)
    ):
        return False

    return True


def any_valid_move(board: Board, player: Player) -> bool:
    return any(
        valid_move_in_direction(board, player, direction) for direction in Direction
    )


def move_player(board: Board, player: Player, direction: Direction):
    player_pos = np.array((player.x_pos, player.y_pos))
    direction_coord = np.array(direction.value)

    if valid_move_in_direction(board, player, direction):
        step_length = cast(int, board.get_entity(*(player_pos + direction_coord)).value)
        player_end_pos = player_pos + direction_coord * step_length

        for i in range(step_length + 1):
            x_pos, y_pos = player_pos + direction_coord * (step_length - i)
            board.update(Empty(x_pos, y_pos))

        player.x_pos, player.y_pos = player_end_pos
        board.update(player)


def player_input(window: Window, board: Board, player: Player) -> Direction:
    wasd = ("w", "a", "s", "d")
    direction = None

    # while not direction:
    while not direction or not valid_move_in_direction(board, player, direction):
        key = ""
        while key not in wasd:
            key = window.win.getkey().lower()
            match key:
                case "w":
                    
                    direction = Direction.UP
                case "s":
                    direction = Direction.DOWN
                case "a":
                    direction = Direction.LEFT
                case "d":
                    direction = Direction.RIGHT
    return direction

def get_score(board: Board) -> float:
    '''Calculates the score as percentage of cleared board'''

    total = len(board.map) * len(board.map[0])
    empty = 0
    for row in board.map:
        for entity in row:
            if isinstance(entity, Empty):
                empty += 1

    score = empty / total * 100

    return score


def main():
    window = Window(BOARD_WIDTH, BOARD_HEIGHT)
    board = Board(BOARD_WIDTH, BOARD_HEIGHT)
    player = new_player(board)
    window.flash(board)

    while any_valid_move(board, player) is True:
        score = get_score(board)
        window.draw_board(board, score)
        direction = player_input(window, board, player)
        move_player(board, player, direction)


    window.game_over()

    curses.endwin()

if __name__ == "__main__":
    main()
