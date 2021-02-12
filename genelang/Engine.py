import sys
from genelang.lexing import Lexer
from .Parser import Parser


class Engine:
    def __init__(self, lexer: Lexer, parser: Parser):
        self.lexer = lexer
        self.parser = parser

    def __repr__(self):
        return f"Engine({self.lexer}, {self.parser})"

    def read_text(self, text: str, base=None):
        tokens = self.lexer.tokenize(text)
        result = self.parser.build(tokens, base=base)

        unparsed = len(tokens[result.to_position:])

        if unparsed:
            prefixes = [">>" if result.to_position == token.at_position else "  " for token in tokens]
            content = repr(tokens)
            print("\n".join(prefix + line for prefix, line in zip(prefixes, content.split('\n'))), file=sys.stderr)

        data, pile = {}, []
        result.build(data, pile)

        return pile[-1]

    def read_file(self, filepath: str):
        with open(filepath, mode="r", encoding="utf-8") as file:
            text = file.read()

        return self.read_text(text)

    @classmethod
    def ast2py(cls, ast: dict, parser: callable):
        return cls(
            lexer=parser(ast['lexer']),
            parser=parser(ast['parser'])
        )
