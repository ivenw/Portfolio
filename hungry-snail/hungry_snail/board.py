import random
from typing import Protocol


class Entity(Protocol):
    def __init__(self, x_pos: int, y_pos: int):
        self.value: int | str | None
        self.x_pos: int
        self.y_pos: int


class Number(Entity):
    def __init__(self, x_pos, y_pos):
        self.value = random.randint(1, 5)
        self.x_pos = x_pos
        self.y_pos = y_pos


class Empty(Entity):
    def __init__(self, x_pos, y_pos):
        self.value = None
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
        """
        Alows board.map to be printed to stdout for debugging.
        """
        buffer = f"{self.width=}, {self.height=}"

        for line in self.map:
            buffer += "\n"
            for tile in line:
                if not tile.value:
                    buffer += f"  "
                else:
                    buffer += f"{tile.value} "

        return buffer

    @property
    def number_of_empty_fields(self) -> int:
        return sum(isinstance(entity, Empty) for row in self.map for entity in row)

    def get_entity(self, x_pos: int, y_pos: int) -> Entity:
        return self.map[y_pos][x_pos]

    def update(self, entity: Entity):
        self.map[entity.y_pos][entity.x_pos] = entity
