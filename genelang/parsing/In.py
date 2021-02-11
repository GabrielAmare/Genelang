from ._Name_Process import _Name_Process
from genelang.lexing import TokenList
from genelang.results import InResult


class In(_Name_Process):
    def build(self, parser, tokens: TokenList, at_position: int) -> InResult:
        process_result = self.process.build(parser, tokens, at_position)
        return InResult(self, at_position, process_result)
