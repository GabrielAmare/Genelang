from typing import Tuple

from .Brick import Brick


class BrickList(Brick):
    items: Tuple[Brick]

    def __init__(self, *items: Brick):
        self.items = items

    @classmethod
    def ast2py(cls, ast: dict, parser):
        return cls(*map(parser, ast['items']))

    def __repr__(self):
        return f"{self.__class__.__name__}(" + ", ".join(map(repr, self.items)) + ")"
