import curses
import time
from typing import cast

from board import Board, Empty, Number
from player import Direction, Player


class Window:
    def __init__(self, win_width: int, win_height: int):
        # create parent window and set settings
        parent = curses.initscr()
        curses.noecho()
        curses.curs_set(False)
        curses.start_color()
        curses.use_default_colors()

        # create child windows
        _, max_w = parent.getmaxyx()
        self.win_h = win_height + 3
        self.win_w = win_width * 2 + 2
        center_x = int(max_w / 2) - int(self.win_w / 2)
        self.win = curses.newwin(self.win_h, self.win_w, 2, center_x)
        self.win.keypad(True)
        self.win.nodelay(False)
        for i in range(11):
            curses.init_pair(i + 1, i, -1)

    @staticmethod
    def close():
        curses.endwin()

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
            

    def draw_game_over(self):
        self.win.addstr(self.win_h-1, int(self.win_w/2 - 5), "Game Over")
        self.win.refresh()
        time.sleep(2)
        self.win.addstr(self.win_h-1, int(self.win_w - 26), "Wanna play again? (y/n)")
        self.win.refresh()
        time.sleep(2)

    def continue_playing(self) -> bool:
        key = ""
        while key not in ("y", "n"):
            key = self.win.getkey().lower()

        if key == "n":
            return False
        else:
            return True


    def get_player_input(self) -> Direction:
        wasd = ("w", "a", "s", "d")
        direction = None

        # while not direction:
        while not direction:
            key = ""
            while key not in wasd:
                key = self.win.getkey().lower()
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
