from .Process import Process
from genelang.lexing import TokenList
from genelang.results import MatchResult


class Match(Process):
    def __init__(self, name: str):
        self.name = name

    def build(self, parser, tokens: TokenList, at_position: int) -> MatchResult:
        if 0 <= at_position < len(tokens):
            token = tokens[at_position]
            valid = token.pattern.name == self.name
        else:
            token = None
            valid = False
        return MatchResult(
            process=self,
            at_position=at_position,
            token=token,
            valid=valid
        )
