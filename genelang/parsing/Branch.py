from .ProcessList import ProcessList
from genelang.lexing import TokenList
from genelang.results import BranchResult


class Branch(ProcessList):
    def build(self, parser, tokens: TokenList, at_position: int) -> BranchResult:
        branch_result = BranchResult(self, at_position)

        for item in self.items:
            item_result = item.build(parser, tokens, at_position)
            branch_result.append(item_result)
            if item_result.error:
                break
            else:
                at_position = item_result.to_position

        return branch_result
