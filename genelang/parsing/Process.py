from genelang.bricks import Brick
from genelang.lexing import TokenList
from genelang.results import Result


class Process(Brick):
    def build(self, parser, tokens: TokenList, at_position: int) -> Result:
        raise NotImplementedError
