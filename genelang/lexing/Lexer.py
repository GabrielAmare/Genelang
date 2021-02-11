from .TokenList import TokenList
from .Pattern import Pattern


class Lexer:
    def __init__(self, *patterns):
        self.patterns = patterns

    def __repr__(self):
        return "Lexer(" + ", ".join(map(repr, self.patterns)) + ")"

    def i_tokenize(self, text: str):
        at_index, at_position = 0, 0
        length = len(text)
        while at_index < length:
            for pattern in self.patterns:
                if token := pattern.read(text, at_index=at_index, at_position=at_position):
                    if not pattern.ignore:
                        at_position = token.to_position
                        yield token

                    at_index = token.to_index
                    break
            else:
                raise Exception(f"Untokenizable text {repr(text[at_index:])}!")

    def tokenize(self, text: str):
        return TokenList(self.i_tokenize(text))

    @classmethod
    def ast2py(cls, ast: dict, parser: callable):
        return cls(*map(parser, ast['patterns']))
