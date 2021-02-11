from .Branch import Branch
from genelang.lexing import TokenList
from genelang.results import WhileResult


class While(Branch):
    def build(self, parser, tokens: TokenList, at_position: int) -> WhileResult:
        while_result = WhileResult(self, at_position)

        while True:
            branch_result = super().build(parser, tokens, at_position)

            if branch_result.error:
                break

            if branch_result.empty:
                break

            while_result.append(branch_result)

            at_position = branch_result.to_position

        return while_result
