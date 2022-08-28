import random

from board import Board
from player import Player


class GameState:
    def __init__(self, board: Board):
        self.board: Board = board
        self.player: Player = self._new_player()
        self.player_has_valid_move: bool = self.player.has_valid_move(self.board)

    @property
    def score(self) -> float:
        """Calculates the score as percentage of cleared board"""
        total = self.board.width * self.board.height
        empty = self.board.number_of_empty_fields
        score = empty / total * 100
        return score

    def update(self, player_direction_input):
        self.player_has_valid_move = self.player.has_valid_move(self.board)
        self.player.move(self.board, player_direction_input)

    def _new_player(self) -> Player:
        x_pos, y_pos = (
            random.randrange(0, self.board.width),
            random.randrange(0, self.board.height),
        )
        player = Player(x_pos, y_pos)
        self.board.update(player)
        return player
