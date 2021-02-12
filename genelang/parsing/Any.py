from .ProcessList import ProcessList
from genelang.lexing import TokenList
from genelang.results import AnyResult


class Any(ProcessList):
    def build(self, parser, tokens: TokenList, at_position: int) -> AnyResult:
        for item in self.items:
            item_result = item.build(parser, tokens, at_position)
            if item_result.valid:
                break
        else:
            item_result = None

        return AnyResult(self, at_position, item_result)
