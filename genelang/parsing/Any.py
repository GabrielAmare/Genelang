from .Process import Process
from genelang.lexing import TokenList
from genelang.results import AnyResult


class Any(Process):
    def __init__(self, *instructions):
        self.instructions = instructions

    def build(self, parser, tokens: TokenList, at_position: int) -> AnyResult:
        for instruction in self.instructions:
            instruction_result = instruction.build(parser, tokens, at_position)
            if instruction_result.valid:
                break
        else:
            instruction_result = None

        return AnyResult(self, at_position, instruction_result)

    @classmethod
    def ast2py(cls, ast: dict, parser: callable):
        return cls(*map(parser, ast['instructions']))