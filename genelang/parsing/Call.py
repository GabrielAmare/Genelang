from .Process import Process
from genelang.lexing import TokenList
from genelang.results import CallResult


class Call(Process):
    def __init__(self, name):
        self.name = name

    def build(self, parser, tokens: TokenList, at_position: int) -> CallResult:
        process = parser.get_builder(self.name)
        if process is None:
            raise Exception(f"The process {self.name} doesn't exists !")
        result = process.build(parser, tokens, at_position)
        return CallResult(self, at_position, result)

    @classmethod
    def ast2py(cls, ast: dict, parser: callable):
        return cls(name=ast['name'])
