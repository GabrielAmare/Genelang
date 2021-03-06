from .Process import Process
from genelang.lexing import TokenList
from genelang.results import BuildResult
from genelang.Identifier import Identifier


class Build(Process):
    def __init__(self, identifier, process):
        if isinstance(identifier, str):
            identifier = Identifier(identifier)
        self.identifier = identifier
        self.process = process

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.identifier)}, {repr(self.process)})"

    @classmethod
    def ast2py(cls, ast: dict, parser: callable):
        return cls(identifier=parser(ast['identifier']), process=parser(ast['process']))

    def build(self, parser, tokens: TokenList, at_position: int) -> BuildResult:
        process_result = self.process.build(parser, tokens, at_position)
        return BuildResult(self, at_position, process_result)
