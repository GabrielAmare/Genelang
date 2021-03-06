from genelang.parsing import Process, Branch, Match
from genelang.lexing import TokenList
from genelang.results import Result


class Bloc(Process):
    def __init__(self, left: str, right: str, *items):
        self.left = left
        self.right = right
        self.items = items

        self.process = Branch(
            Match(self.left),
            *self.items,
            Match(self.right)
        )

    def __repr__(self):
        return f"Bloc({repr(self.left)}, {repr(self.right)}, " + ", ".join(map(repr, self.items)) + ")"

    def build(self, parser, tokens: TokenList, at_position: int) -> Result:
        return self.process.build(parser, tokens, at_position)

    @classmethod
    def ast2py(cls, ast: dict, parser: callable):
        return cls(ast['left'], ast['right'], *map(parser, ast['items']))
