from genelang.parsing import Process, Branch, Match
from genelang.lexing import TokenList
from genelang.results import Result


class Binary(Process):
    def __init__(self, key: str, left, right):
        self.key = key
        self.left = left
        self.right = right

        self.process = Branch(
            self.left,
            Match(self.key),
            self.right
        )

    def __repr__(self):
        return f"Binary({repr(self.key)}, {repr(self.left)}, {repr(self.right)})"

    def build(self, parser, tokens: TokenList, at_position: int) -> Result:
        return self.process.build(parser, tokens, at_position)

    @classmethod
    def ast2py(cls, ast: dict, parser: callable):
        return cls(ast['key'], parser(ast['left']), parser(ast['right']))