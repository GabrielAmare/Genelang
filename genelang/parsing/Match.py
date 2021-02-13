from typing import Union

from .Process import Process
from genelang.lexing import TokenList
from genelang.results import MatchResult, CallResult
from genelang.Identifier import Identifier


class Match(Process):
    def __init__(self, *identifiers):
        self.identifiers = identifiers

    def __repr__(self):
        return f"{self.__class__.__name__}(" + ", ".join(map(repr, self.identifiers)) + ")"

    @classmethod
    def ast2py(cls, ast: dict, parser: callable):
        return cls(*map(parser, ast.get('identifiers', [])))

    def build(self, parser, tokens: TokenList, at_position: int) -> Union[MatchResult, CallResult]:
        token = None
        valid = False

        for identifier in self.identifiers:
            if 0 <= at_position < len(tokens):
                token = tokens[at_position]
                valid = identifier.match(token.pattern.name)
                if valid:
                    break

            if not token or not valid:
                for process in parser.get_builders(identifier):
                    result = process.build(parser, tokens, at_position)
                    if result.valid:
                        return CallResult(self, at_position, result)

                process = parser.get_builder(identifier.name)
                if process is not None:
                    result = process.build(parser, tokens, at_position)
                    return CallResult(self, at_position, result)

        return MatchResult(
            process=self,
            at_position=at_position,
            token=token,
            valid=valid
        )
