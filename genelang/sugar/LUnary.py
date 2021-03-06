from genelang.parsing import Process, Branch, Match
from genelang.lexing import TokenList
from genelang.results import Result


class LUnary(Process):
    def __init__(self, name: str, *items):
        self.name = name
        self.items = items

        self.process = Branch(
            Match(self.name),
            *self.items
        )

    def __repr__(self):
        return f"LUnary({repr(self.name)}, " + ", ".join(map(repr, self.items)) + ")"

    def build(self, parser, tokens: TokenList, at_position: int) -> Result:
        return self.process.build(parser, tokens, at_position)

    @classmethod
    def ast2py(cls, ast: dict, parser: callable):
        return cls(ast['name'], *map(parser, ast['items']))