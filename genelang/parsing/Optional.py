from .Process import Process
from .Branch import Branch
from genelang.lexing import TokenList
from genelang.results import OptionalResult


class Optional(Process):
    def __init__(self, *instructions):
        self.branch = Branch(*instructions)

    def build(self, parser, tokens: TokenList, at_position: int) -> OptionalResult:
        branch_result = self.branch.build(parser, tokens, at_position)
        return OptionalResult(self, at_position, branch_result)
