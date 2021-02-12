from genelang.parsing import Process, Branch, Match
from genelang.lexing import TokenList
from genelang.results import Result


class Binary(Process):
    def __init__(self, name: str, left, right):
        self.name = name
        self.left = left
        self.right = right

        self.process = Branch(
            self.left,
            Match(self.name),
            self.right
        )

    def __repr__(self):
        return f"Binary({repr(self.name)}, {repr(self.left)}, {repr(self.right)})"

    def build(self, parser, tokens: TokenList, at_position: int) -> Result:
        return self.process.build(parser, tokens, at_position)

    @classmethod
    def ast2py(cls, ast: dict, parser: callable):
        return cls(ast['name'], parser(ast['left']), parser(ast['right']))