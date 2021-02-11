from .ProcessList import ProcessList
from genelang.lexing import TokenList
from genelang.results import BranchResult


class Branch(ProcessList):
    def build(self, parser, tokens: TokenList, at_position: int) -> BranchResult:
        branch_result = BranchResult(self, at_position)

        for instruction in self.instructions:
            instruction_result = instruction.build(parser, tokens, at_position)
            branch_result.append(instruction_result)
            if instruction_result.error:
                break
            else:
                at_position = instruction_result.to_position

        return branch_result
