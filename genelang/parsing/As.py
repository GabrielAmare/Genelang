from .Process import Process
from genelang.lexing import TokenList
from genelang.results import AsResult


class As(Process):
    def __init__(self, key, process):
        self.key = key
        self.process = process

    def build(self, parser, tokens: TokenList, at_position: int) -> AsResult:
        process_result = self.process.build(parser, tokens, at_position)
        return AsResult(self, at_position, process_result)

    @classmethod
    def ast2py(cls, ast: dict, parser: callable):
        return cls(key=ast['key'], process=parser(ast['process']))