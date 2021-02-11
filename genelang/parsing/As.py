from ._Name_Process import _Name_Process
from genelang.lexing import TokenList
from genelang.results import AsResult


class As(_Name_Process):
    def build(self, parser, tokens: TokenList, at_position: int) -> AsResult:
        process_result = self.process.build(parser, tokens, at_position)
        return AsResult(self, at_position, process_result)
