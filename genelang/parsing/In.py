from .Process import Process
from genelang.lexing import TokenList
from genelang.results import InResult


class In(Process):
    def __init__(self, key, process):
        self.key = key
        self.process = process

    def build(self, parser, tokens: TokenList, at_position: int) -> InResult:
        process_result = self.process.build(parser, tokens, at_position)
        return InResult(self, at_position, process_result)
