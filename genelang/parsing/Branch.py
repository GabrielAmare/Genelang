from .Process import Process
from genelang.lexing import TokenList
from genelang.results import BranchResult


class Branch(Process):
    def __init__(self, *instructions):
        assert all(isinstance(instruction, Process) for instruction in instructions)
        self.instructions = instructions

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

    @classmethod
    def ast2py(cls, ast: dict, parser: callable):
        return cls(*map(parser, ast['instructions']))