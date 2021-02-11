from .Branch import Branch
from genelang.lexing import TokenList
from genelang.results import OptionalResult


class Optional(Branch):
    def build(self, parser, tokens: TokenList, at_position: int) -> OptionalResult:
        branch_result = super().build(parser, tokens, at_position)
        return OptionalResult(self, at_position, branch_result)
