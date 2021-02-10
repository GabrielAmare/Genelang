from .Process import Process
from genelang.lexing import TokenList
from genelang.results import NamedProcessResult


class NamedProcess(Process):
    def __init__(self, name, process):
        self.name = name
        self.process = process

    def build(self, parser, tokens: TokenList, at_position: int) -> NamedProcessResult:
        process_result = self.process.build(parser, tokens, at_position)
        return NamedProcessResult(self, at_position, process_result)

    @classmethod
    def ast2py(cls, ast: dict, parser: callable):
        return cls(name=ast['name'], process=parser(ast['process']))
