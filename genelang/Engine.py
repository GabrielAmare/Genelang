import sys
from genelang.lexing import Lexer, TokenList
from .Parser import Parser


class Engine:
    def __init__(self, lexer: Lexer, parser: Parser):
        self.lexer = lexer
        self.parser = parser

    def read(self, filepath):
        with open(filepath, mode="r", encoding="utf-8") as file:
            content = file.read()

        tokens = self.lexer.tokenize(content)
        result = self.parser.build(tokens)

        unparsed = len(tokens[result.to_position:])

        if unparsed:
            prefixes = [">>" if result.to_position == token.at_position else "  " for token in tokens]
            content = repr(tokens)
            print("\n".join(prefix+line for prefix, line in zip(prefixes, content.split('\n'))), file=sys.stderr)

        data, pile = {}, []
        result.build(data, pile)

        return pile[-1]

    @classmethod
    def ast2py(cls, ast: dict, parser: callable):
        return cls(
            lexer=parser(ast['lexer']),
            parser=parser(ast['parser'])
        )