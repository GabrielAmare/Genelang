from typing import Tuple

from .Brick import Brick


class OP(Brick):
    items: Tuple[Brick]
    types: Tuple[object]
    symbols: Tuple[object]

    def __init__(self, *items: Brick):
        assert len(items) == len(self.__class__.types)
        self.items = items

    @classmethod
    def ast2py(cls, ast: dict, parser):
        return cls(*map(parser, ast['items']))

    def __repr__(self):
        return f"{self.__class__.__name__}(" + ", ".join(map(repr, self.items)) + ")"
