from genelang.lexing import TokenList
from genelang.results import Result


class Process:
    def build(self, parser, tokens: TokenList, at_position: int) -> Result:
        raise NotImplementedError
