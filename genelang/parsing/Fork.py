from .ProcessList import ProcessList
from genelang.lexing import TokenList
from genelang.results import ForkResult


class Fork(ProcessList):
    def build(self, parser, tokens: TokenList, at_position: int) -> ForkResult:
        for branch in self.items:
            branch_result = branch.build(parser, tokens, at_position)
            if branch_result.valid:
                break
        else:
            branch_result = None

        return ForkResult(self, at_position, branch_result)
