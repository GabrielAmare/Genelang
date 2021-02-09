from genelang.parsing import Process, Branch, Match
from genelang.lexing import TokenList
from genelang.results import Result


class Bloc(Process):
    def __init__(self, left: str, right: str, *instructions):
        self.left = left
        self.right = right
        self.instructions = instructions

        self.process = Branch(
            Match(self.left),
            *self.instructions,
            Match(self.right)
        )

    def build(self, parser, tokens: TokenList, at_position: int) -> Result:
        return self.process.build(parser, tokens, at_position)
