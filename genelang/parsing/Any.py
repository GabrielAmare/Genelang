from .ProcessList import ProcessList
from genelang.lexing import TokenList
from genelang.results import AnyResult


class Any(ProcessList):
    def build(self, parser, tokens: TokenList, at_position: int) -> AnyResult:
        for instruction in self.instructions:
            instruction_result = instruction.build(parser, tokens, at_position)
            if instruction_result.valid:
                break
        else:
            instruction_result = None

        return AnyResult(self, at_position, instruction_result)
