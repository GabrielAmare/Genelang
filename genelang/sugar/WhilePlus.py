from genelang.parsing import Process, Branch, While
from genelang.lexing import TokenList
from genelang.results import Result


class WhilePlus(Process):
    def __init__(self, *items):
        self.items = items

        self.process = Branch(
            *self.items,
            While(*self.items)
        )

    def __repr__(self):
        return f"WhilePlus(" + ", ".join(map(repr, self.items)) + ")"

    def build(self, parser, tokens: TokenList, at_position: int) -> Result:
        return self.process.build(parser, tokens, at_position)

    @classmethod
    def ast2py(cls, ast: dict, parser: callable):
        return cls(*map(parser, ast['items']))
