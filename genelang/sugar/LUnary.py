from genelang.parsing import Process, Branch, Match
from genelang.lexing import TokenList
from genelang.results import Result


class LUnary(Process):
    def __init__(self, key: str, *instructions):
        self.key = key
        self.instructions = instructions

        self.process = Branch(
            Match(self.key),
            *self.instructions
        )

    def __repr__(self):
        return f"LUnary({repr(self.key)}, " + ", ".join(map(repr, self.instructions)) + ")"

    def build(self, parser, tokens: TokenList, at_position: int) -> Result:
        return self.process.build(parser, tokens, at_position)

    @classmethod
    def ast2py(cls, ast: dict, parser: callable):
        return cls(ast['key'], *map(parser, ast['instructions']))