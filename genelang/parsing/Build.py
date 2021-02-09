from .Process import Process
from genelang.lexing import TokenList
from genelang.results import BuildResult


class Build(Process):
    def __init__(self, name, process):
        self.name = name
        self.process = process

    def build(self, parser, tokens: TokenList, at_position: int) -> BuildResult:
        process_result = self.process.build(parser, tokens, at_position)
        return BuildResult(self, at_position, process_result)
