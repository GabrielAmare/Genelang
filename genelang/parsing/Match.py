from typing import Union

from ._Name import _Name
from genelang.lexing import TokenList
from genelang.results import MatchResult, CallResult


class Match(_Name):
    def build(self, parser, tokens: TokenList, at_position: int) -> Union[MatchResult, CallResult]:
        token = None
        valid = False

        if 0 <= at_position < len(tokens):
            token = tokens[at_position]
            valid = token.pattern.name == self.name

        if not token or not valid:
            process = parser.get_builder(self.name)

            if process is not None:
                result = process.build(parser, tokens, at_position)
                return CallResult(self, at_position, result)

        return MatchResult(
            process=self,
            at_position=at_position,
            token=token,
            valid=valid
        )
