from enum import Enum
from typing import cast

import numpy as np

from board import Board, Empty, Number


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class Player:
    def __init__(self, x_pos, y_pos):
        self.value = "@"
        self.x_pos = x_pos
        self.y_pos = y_pos

    def _valid_move_in_direction(self, board: Board, direction: Direction) -> bool:
        player_pos = np.array([self.x_pos, self.y_pos])
        dir_coors = np.array(direction.value)
        x_neighbour, y_neighbour = player_pos + dir_coors

        # check if the coordinates of the neighbour set by the direction is out of bounds
        if any(
            (
                x_neighbour < 0,
                y_neighbour < 0,
                x_neighbour > board.width - 1,
                y_neighbour > board.height - 1,
            )
        ):
            return False

        neighbour = board.get_entity(x_neighbour, y_neighbour)
        step_length = cast(int, neighbour.value)

        # check if the neighbour ir a Number
        if not isinstance(neighbour, Number):
            return False

        x_dest, y_dest = player_pos + dir_coors * step_length

        # check if the final destination is out of bounds
        if any(
            (
                x_dest < 0,
                y_dest < 0,
                x_dest > board.width - 1,
                y_dest > board.height - 1,
            )
        ):
            return False

        # check if any field along the way to the final destination is an empty field
        for i in range(1, step_length + 1):
            x_step, y_step = x_dest, y_dest = player_pos + dir_coors * i
            if isinstance(board.get_entity(x_step, y_step), Empty):
                return False

        return True

    def has_valid_move(self, board: Board) -> bool:
        return any(
            self._valid_move_in_direction(board, direction) for direction in Direction
        )

    def move(self, board: Board, direction: Direction):
        player_pos = np.array((self.x_pos, self.y_pos))
        direction_coord = np.array(direction.value)

        if self._valid_move_in_direction(board, direction):
            step_length = cast(
                int, board.get_entity(*(player_pos + direction_coord)).value
            )
            player_end_pos = player_pos + direction_coord * step_length
            for i in range(step_length + 1):
                x_pos, y_pos = player_pos + direction_coord * (step_length - i)
                board.update(Empty(x_pos, y_pos))

            self.x_pos, self.y_pos = player_end_pos
            board.update(self)
